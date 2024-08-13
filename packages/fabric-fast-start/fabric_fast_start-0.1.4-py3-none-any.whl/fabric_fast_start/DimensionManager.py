import logging
from datetime import datetime
from decimal import Decimal
from typing import Any, List, Optional  # noqa: UP035

from delta import DeltaTable
from pyspark.sql import DataFrame, Row, SparkSession
from pyspark.sql.functions import col, current_timestamp, lit, row_number, when
from pyspark.sql.types import BooleanType, DateType, DecimalType, IntegerType, StringType, TimestampType
from pyspark.sql.window import Window


class DimensionManager:
    def __init__(self, spark: SparkSession, table_name: str, table_path: str, updated_by: str = "System", debug: bool = False):
        self.spark = spark
        self.table_name = table_name
        self.table_path = table_path
        self.updated_by = updated_by
        self.logger = self._setup_logger(debug)

    def _setup_logger(self, debug: bool) -> logging.Logger:
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.DEBUG if debug else logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def create_dimension(
        self, source_data: DataFrame, primary_keys: List[str], include_unknown: bool = True, update_columns: Optional[List[str]] = None, keep_old_rows: bool = True  # type: ignore # noqa
    ) -> None:
        try:
            self.logger.info(f"Creating dimension table: {self.table_name}")

            # Add SK column to source_data
            source_data = source_data.withColumn("SK", lit(None).cast(IntegerType()))

            # Add update columns if specified
            if update_columns:
                source_data = self._add_update_columns(source_data, update_columns)

            # Add Unknown row if specified
            if include_unknown:
                source_data = self._add_unknown_row(source_data)

            # Generate surrogate keys
            source_data = self._generate_surrogate_keys(source_data, primary_keys)

            # Write data to Delta table
            if self._table_exists():
                self._update_dimension(source_data, primary_keys, keep_old_rows)
            else:
                self._create_new_dimension(source_data)

            self.logger.info(f"Dimension table {self.table_name} created/updated successfully")
        except Exception as e:
            self.logger.error(f"Error creating dimension table: {str(e)}")
            raise

    def _add_update_columns(self, df: DataFrame, update_columns: List[str]) -> DataFrame:  # type: ignore # noqa
        for column in update_columns:
            if column == "_updated_at":
                df = df.withColumn("_updated_at", current_timestamp())
            elif column == "_updated_by":
                df = df.withColumn("_updated_by", lit(self.updated_by))
            elif column == "_is_active":
                df = df.withColumn("_is_active", lit(True))
        return df

    def _add_unknown_row(self, df: DataFrame) -> DataFrame:
        unknown_data = {col_name: self._unknown_value(df.schema[col_name].dataType) for col_name in df.columns}
        unknown_data["SK"] = -1

        # Ensure _updated_at, _updated_by, and _is_active columns are present and have the correct types
        if "_updated_at" in df.columns:
            unknown_data["_updated_at"] = self._unknown_value(TimestampType())
        if "_updated_by" in df.columns:
            unknown_data["_updated_by"] = self.updated_by
        if "_is_active" in df.columns:
            unknown_data["_is_active"] = True

        unknown_row = self.spark.createDataFrame([Row(**unknown_data)], df.schema)
        return df.union(unknown_row)

    def _unknown_value(self, data_type: Any) -> Any:
        if isinstance(data_type, StringType):
            return "Unknown"
        elif isinstance(data_type, DecimalType):
            return Decimal("0.000000")
        elif isinstance(data_type, IntegerType):
            return 0
        elif isinstance(data_type, DateType):
            return datetime.strptime("1970-01-01", "%Y-%m-%d").date()
        elif isinstance(data_type, TimestampType):
            return datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        elif isinstance(data_type, BooleanType):
            return False
        return "N/A"

    def _generate_surrogate_keys(self, df: DataFrame, primary_keys: List[str]) -> DataFrame:  # type: ignore # noqa
        self.logger.debug("Generating surrogate keys")
        if self._table_exists():
            existing_df = self.spark.read.format("delta").load(self.table_path)
            max_sk = existing_df.agg({"SK": "max"}).collect()[0][0]
            if max_sk is None:
                max_sk = 0

            existing_df = existing_df.select(*primary_keys, col("SK").alias("existing_SK"))

            df = (
                df.alias("new")
                .join(existing_df.alias("existing"), primary_keys, "left_outer")
                .select(*[col("new." + col_name) for col_name in df.columns if col_name != "SK"], col("existing.existing_SK"))
            )

            window = Window.orderBy(lit(1))
            df = df.withColumn("row_num", row_number().over(window))
            df = df.withColumn("SK", when(col("existing_SK").isNull(), col("row_num") + max_sk).otherwise(col("existing_SK")))
            df = df.drop("row_num", "existing_SK")
        else:
            window = Window.orderBy(lit(1))
            df = df.withColumn("row_num", row_number().over(window))
            df = df.withColumn("SK", when(col("SK") == -1, lit(-1)).otherwise(col("row_num")))
            df = df.drop("row_num")

        self.logger.debug("Surrogate keys generated successfully")
        return df

    def _table_exists(self) -> bool:
        return DeltaTable.isDeltaTable(self.spark, self.table_path)

    def _update_dimension(self, source_data: DataFrame, primary_keys: List[str], keep_old_rows: bool) -> None:  # type: ignore # noqa
        self.logger.debug(f"Updating existing dimension table: {self.table_name}")
        delta_table = DeltaTable.forPath(self.spark, self.table_path)

        merge_condition = " AND ".join([f"target.{pk} = source.{pk}" for pk in primary_keys])

        # Use col for column references and current_timestamp() directly
        update_set = {col_name: col(f"source.{col_name}") for col_name in source_data.columns if col_name not in primary_keys and col_name != "SK"}
        if "_updated_at" in source_data.columns:
            update_set["_updated_at"] = current_timestamp()
        if "_updated_by" in source_data.columns:
            update_set["_updated_by"] = lit("System")

        merge_builder = (
            delta_table.alias("target")
            .merge(source_data.alias("source"), merge_condition)
            .whenMatchedUpdate(set=update_set)  # type: ignore[arg-type]
            .whenNotMatchedInsert(values={col_name: col(f"source.{col_name}") for col_name in source_data.columns})
        )

        if not keep_old_rows:
            merge_builder = merge_builder.whenNotMatchedBySourceDelete()

        merge_builder.execute()

        self.logger.debug(f"Dimension table {self.table_name} updated successfully")

    def _create_new_dimension(self, source_data: DataFrame) -> None:
        self.logger.debug(f"Creating new dimension table: {self.table_name}")
        source_data.write.format("delta").mode("overwrite").save(self.table_path)
        self.logger.debug(f"New dimension table created at: {self.table_path}")
