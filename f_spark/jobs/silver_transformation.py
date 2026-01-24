"""
Silver Layer Transformation Job
Cleans, validates, and transforms Bronze data to Silver layer
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, year, month, dayofmonth
from datetime import datetime


def create_spark_session(app_name: str = "SilverTransformation") -> SparkSession:
    """Create Spark session with S3/MinIO configuration"""
    return (
        SparkSession.builder
        .appName(app_name)
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9002")
        .config("spark.hadoop.fs.s3a.access.key", "arcadia-admin")
        .config("spark.hadoop.fs.s3a.secret.key", "arcadia-secret-key-123")
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.sql.adaptive.enabled", "true")
        .getOrCreate()
    )


def transform_saves_to_silver(batch_date: str = None):
    """
    Transform Bronze saves to Silver layer
    - Data cleaning
    - Schema validation
    - Deduplication
    - Partitioning by date

    Args:
        batch_date: Date to process (YYYY-MM-DD), defaults to yesterday
    """
    spark = create_spark_session("SilverTransformation-Saves")

    if batch_date is None:
        from datetime import datetime, timedelta
        batch_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    print(f"Processing Bronze saves for date: {batch_date}")

    # Read from Bronze layer
    bronze_df = (
        spark.read
        .format("parquet")
        .load("s3a://bronze/saves/")
        .filter(to_date(col("ingested_at")) == batch_date)
    )

    # Data cleaning and transformation
    silver_df = (
        bronze_df
        # Remove duplicates based on save_id
        .dropDuplicates(["save_id"])
        # Filter out invalid records
        .filter(col("save_id").isNotNull())
        .filter(col("player_id").isNotNull())
        .filter(col("file_size_bytes") > 0)
        # Add partition columns
        .withColumn("date", to_date(col("ingested_at")))
        .withColumn("year", year(col("ingested_at")))
        .withColumn("month", month(col("ingested_at")))
        .withColumn("day", dayofmonth(col("ingested_at")))
        # Select and order columns
        .select(
            "save_id",
            "player_id",
            "filename",
            "file_size_bytes",
            "checksum",
            "s3_path",
            "ingested_at",
            "year",
            "month",
            "day"
        )
    )

    # Write to Silver layer (partitioned)
    (
        silver_df
        .write
        .format("parquet")
        .mode("overwrite")
        .partitionBy("year", "month", "day")
        .option("compression", "snappy")
        .save("s3a://silver/saves/")
    )

    print(f"Silver transformation complete. Records processed: {silver_df.count()}")
    spark.stop()


def transform_choices_to_silver(batch_date: str = None):
    """
    Transform Bronze choices to Silver layer
    - Flatten nested structures
    - Validate choice data
    - Enrich with additional attributes
    """
    spark = create_spark_session("SilverTransformation-Choices")

    if batch_date is None:
        from datetime import datetime, timedelta
        batch_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    print(f"Processing Bronze choices for date: {batch_date}")

    bronze_df = (
        spark.read
        .format("parquet")
        .load("s3a://bronze/choices/")
        .filter(to_date(col("ingested_at")) == batch_date)
    )

    silver_df = (
        bronze_df
        .dropDuplicates(["save_id", "player_id"])
        .filter(col("save_id").isNotNull())
        .filter(col("player_id").isNotNull())
        .filter(col("total_choices") > 0)
        .withColumn("date", to_date(col("ingested_at")))
        .withColumn("year", year(col("ingested_at")))
        .withColumn("month", month(col("ingested_at")))
        .withColumn("day", dayofmonth(col("ingested_at")))
        .select(
            "save_id",
            "player_id",
            "total_choices",
            "ingested_at",
            "year",
            "month",
            "day"
        )
    )

    (
        silver_df
        .write
        .format("parquet")
        .mode("overwrite")
        .partitionBy("year", "month", "day")
        .option("compression", "snappy")
        .save("s3a://silver/choices/")
    )

    print(f"Silver transformation complete. Records processed: {silver_df.count()}")
    spark.stop()


if __name__ == "__main__":
    import sys
    
    job_type = sys.argv[1] if len(sys.argv) > 1 else "saves"
    batch_date = sys.argv[2] if len(sys.argv) > 2 else None
    
    if job_type == "saves":
        transform_saves_to_silver(batch_date)
    elif job_type == "choices":
        transform_choices_to_silver(batch_date)
    else:
        print(f"Unknown job type: {job_type}")
        sys.exit(1)
