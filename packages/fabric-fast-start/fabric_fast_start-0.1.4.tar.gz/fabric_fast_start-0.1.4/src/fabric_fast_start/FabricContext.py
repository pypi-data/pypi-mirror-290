import logging
from typing import Optional

from pyspark.sql import SparkSession

from fabric_fast_start.Logger import Logger


class FabricContext:
    def __init__(self, spark: Optional[SparkSession] = None, debug: bool = False):  # noqa: UP007
        self._spark = (
            spark
            if spark is not None
            else SparkSession.builder.master("local[2]")
            .appName("UnitTest")
            .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.2.0")
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
            .getOrCreate()
        )
        self._logger = Logger.setup_logger(self.__class__.__name__, logging.DEBUG if debug else logging.INFO)

    def stop(self):
        self.spark.stop()
        self.logger.info("Spark session stopped successfully.")

    @property
    def spark(self):
        return self._spark

    @property
    def logger(self):
        return self._logger
