import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType, StructField, StructType

from fabric_fast_start.DimensionManager import DimensionManager


@pytest.fixture(scope="module")
def spark():
    return (
        SparkSession.builder.master("local[2]")
        .appName("UnitTest")
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.2.0")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .getOrCreate()
    )


@pytest.fixture(scope="function")
def dimension_manager(spark, tmp_path):
    return DimensionManager(spark, "test_dimension", str(tmp_path / "test_dimension"), debug=True)


@pytest.fixture(scope="function")
def sample_data(spark):
    schema = StructType([StructField("id", IntegerType(), False), StructField("name", StringType(), False), StructField("department", StringType(), True)])
    data = [(1, "John Doe", "Sales"), (2, "Jane Smith", "Marketing"), (3, "Bob Johnson", "IT")]
    return spark.createDataFrame(data, schema)


def test_create_new_dimension_with_unknown(dimension_manager, sample_data):
    dimension_manager.create_dimension(
        source_data=sample_data, primary_keys=["id"], include_unknown=True, update_columns=["_updated_at", "_updated_by", "_is_active"], keep_old_rows=True
    )

    result = dimension_manager.spark.read.format("delta").load(dimension_manager.table_path)
    assert result.count() == 4  # 3 original rows + 1 Unknown row
    assert result.filter(result.SK == -1).count() == 1  # Unknown row
    assert "_updated_at" in result.columns
    assert "_updated_by" in result.columns
    assert "_is_active" in result.columns


def test_create_dimension_without_unknown(dimension_manager, sample_data):
    dimension_manager.create_dimension(source_data=sample_data, primary_keys=["id"], include_unknown=False, update_columns=None, keep_old_rows=True)

    result = dimension_manager.spark.read.format("delta").load(dimension_manager.table_path)
    assert result.count() == 3  # Only original rows
    assert result.filter(result.SK == -1).count() == 0  # No Unknown row
    assert "_updated_at" not in result.columns
    assert "_updated_by" not in result.columns
    assert "_is_active" not in result.columns


def test_update_dimension_keep_old_rows(dimension_manager, sample_data, spark):
    dimension_manager.create_dimension(source_data=sample_data, primary_keys=["id"], include_unknown=True, update_columns=["_updated_at"], keep_old_rows=True)

    # Update with new data
    new_data = [(2, "Jane Doe", "HR"), (4, "Alice Brown", "Finance")]  # Updated row  # New row
    new_df = spark.createDataFrame(new_data, sample_data.schema)

    dimension_manager.create_dimension(source_data=new_df, primary_keys=["id"], include_unknown=True, update_columns=["_updated_at"], keep_old_rows=True)

    result = dimension_manager.spark.read.format("delta").load(dimension_manager.table_path)
    assert result.count() == 5  # 3 original + 1 new + 1 Unknown
    assert result.filter(result.name == "Jane Doe").first().department == "HR"
    assert result.filter(result.name == "Alice Brown").count() == 1


def test_update_dimension_remove_old_rows(dimension_manager, sample_data, spark):
    dimension_manager.create_dimension(
        source_data=sample_data, primary_keys=["id"], include_unknown=True, update_columns=["_updated_at", "_is_active"], keep_old_rows=True
    )

    # Update with new data
    new_data = [(2, "Jane Doe", "HR"), (4, "Alice Brown", "Finance")]  # Updated row  # New row
    new_df = spark.createDataFrame(new_data, sample_data.schema)

    dimension_manager.create_dimension(
        source_data=new_df, primary_keys=["id"], include_unknown=True, update_columns=["_updated_at", "_is_active"], keep_old_rows=False
    )

    result = dimension_manager.spark.read.format("delta").load(dimension_manager.table_path)
    assert result.count() == 3  # 2 new/updated rows + 1 Unknown
    assert result.filter(result.name == "John Doe").count() == 0  # Old row removed
    assert result.filter(result.name == "Jane Doe").first().department == "HR"
    assert result.filter(result.name == "Alice Brown").count() == 1


def test_dimension_with_partial_update_columns(dimension_manager, sample_data):
    dimension_manager.create_dimension(
        source_data=sample_data, primary_keys=["id"], include_unknown=True, update_columns=["_updated_at", "_is_active"], keep_old_rows=True
    )

    result = dimension_manager.spark.read.format("delta").load(dimension_manager.table_path)
    assert "_updated_at" in result.columns
    assert "_updated_by" not in result.columns
    assert "_is_active" in result.columns


def test_dimension_with_custom_updated_by(spark, tmp_path, sample_data):
    custom_manager = DimensionManager(spark, "custom_dimension", str(tmp_path / "custom_dimension"), updated_by="TestUser", debug=True)
    custom_manager.create_dimension(
        source_data=sample_data, primary_keys=["id"], include_unknown=True, update_columns=["_updated_at", "_updated_by"], keep_old_rows=True
    )

    result = custom_manager.spark.read.format("delta").load(custom_manager.table_path)
    assert result.filter(result._updated_by == "TestUser").count() == result.count()


def test_error_handling(dimension_manager):
    with pytest.raises(Exception):
        dimension_manager.create_dimension(source_data=None, primary_keys=["id"], include_unknown=True, update_columns=["_updated_at"], keep_old_rows=True)
