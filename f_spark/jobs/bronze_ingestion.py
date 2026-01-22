"""
Bronze Layer Ingestion Job
Reads raw data from Kafka and writes to Bronze layer (MinIO)
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType


def create_spark_session(app_name: str = "BronzeIngestion") -> SparkSession:
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
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .getOrCreate()
    )


def ingest_saves_to_bronze():
    """
    Ingest save upload events from Kafka to Bronze layer
    Structured streaming job
    """
    spark = create_spark_session("BronzeIngestion-Saves")

    # Define schema for Kafka messages
    save_schema = StructType([
        StructField("event_type", StringType(), True),
        StructField("save_id", StringType(), True),
        StructField("player_id", StringType(), True),
        StructField("filename", StringType(), True),
        StructField("file_size_bytes", IntegerType(), True),
        StructField("checksum", StringType(), True),
        StructField("s3_path", StringType(), True),
        StructField("timestamp", TimestampType(), True)
    ])

    # Read from Kafka
    kafka_df = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "kafka:29092")
        .option("subscribe", "saves.uploaded")
        .option("startingOffsets", "earliest")
        .load()
    )

    # Parse JSON value
    parsed_df = (
        kafka_df
        .selectExpr("CAST(value AS STRING) as json_value")
        .select(from_json(col("json_value"), save_schema).alias("data"))
        .select("data.*")
        .withColumn("ingested_at", current_timestamp())
    )

    # Write to Bronze layer (Parquet in MinIO)
    query = (
        parsed_df.writeStream
        .format("parquet")
        .option("path", "s3a://bronze/saves/")
        .option("checkpointLocation", "s3a://bronze/checkpoints/saves/")
        .partitionBy("ingested_at")
        .trigger(processingTime="5 minutes")
        .start()
    )

    query.awaitTermination()


def ingest_choices_to_bronze():
    """
    Ingest choice extraction events from Kafka to Bronze layer
    """
    spark = create_spark_session("BronzeIngestion-Choices")

    # Define schema for choice events
    choice_schema = StructType([
        StructField("event_type", StringType(), True),
        StructField("save_id", StringType(), True),
        StructField("player_id", StringType(), True),
        StructField("total_choices", IntegerType(), True),
        StructField("timestamp", TimestampType(), True)
    ])

    kafka_df = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "kafka:29092")
        .option("subscribe", "choices.extracted")
        .option("startingOffsets", "earliest")
        .load()
    )

    parsed_df = (
        kafka_df
        .selectExpr("CAST(value AS STRING) as json_value")
        .select(from_json(col("json_value"), choice_schema).alias("data"))
        .select("data.*")
        .withColumn("ingested_at", current_timestamp())
    )

    query = (
        parsed_df.writeStream
        .format("parquet")
        .option("path", "s3a://bronze/choices/")
        .option("checkpointLocation", "s3a://bronze/checkpoints/choices/")
        .partitionBy("ingested_at")
        .trigger(processingTime="5 minutes")
        .start()
    )

    query.awaitTermination()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python bronze_ingestion.py [saves|choices]")
        sys.exit(1)
    
    job_type = sys.argv[1]
    
    if job_type == "saves":
        ingest_saves_to_bronze()
    elif job_type == "choices":
        ingest_choices_to_bronze()
    else:
        print(f"Unknown job type: {job_type}")
        sys.exit(1)
