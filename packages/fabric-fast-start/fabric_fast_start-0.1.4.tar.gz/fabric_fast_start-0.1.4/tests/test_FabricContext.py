import unittest
from typing import Optional

from pyspark.sql import SparkSession

from fabric_fast_start.FabricContext import FabricContext


class TestFabricContext(unittest.TestCase):
    spark: Optional[SparkSession] = None  # noqa: UP007

    @classmethod
    def setUpClass(cls):
        cls.spark = (
            SparkSession.builder.master("local[2]")
            .appName("UnitTest")
            .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.2.0")
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
            .getOrCreate()
        )

    @classmethod
    def tearDownClass(cls):
        if cls.spark:
            cls.spark.stop()

    def test_spark_session_initialized(self):
        fabric_context = FabricContext(self.spark)
        self.assertIsNotNone(fabric_context.spark)

    def test_spark_session_initialized_with_default(self):
        fabric_context = FabricContext(None)
        self.assertIsNotNone(fabric_context.spark)

    def test_logger_initialized(self):
        fabric_context = FabricContext(self.spark)
        self.assertIsNotNone(fabric_context.logger)


if __name__ == "__main__":
    unittest.main()
