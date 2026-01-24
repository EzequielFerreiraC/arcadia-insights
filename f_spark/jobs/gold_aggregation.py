"""
Gold Layer Aggregation Job
Creates analytics-ready aggregates from Silver data
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, countDistinct, avg, sum as spark_sum,
    round as spark_round, year, month
)


def create_spark_session(app_name: str = "GoldAggregation") -> SparkSession:
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


def aggregate_player_stats():
    """
    Aggregate player statistics from Silver layer
    Creates player_stats table in Gold layer
    """
    spark = create_spark_session("GoldAggregation-PlayerStats")

    # Read Silver data
    saves_df = spark.read.parquet("s3a://silver/saves/")
    choices_df = spark.read.parquet("s3a://silver/choices/")

    # Aggregate by player
    player_stats = (
        saves_df
        .groupBy("player_id")
        .agg(
            count("save_id").alias("total_saves"),
            spark_sum("file_size_bytes").alias("total_file_size_bytes")
        )
    )

    choice_stats = (
        choices_df
        .groupBy("player_id")
        .agg(
            spark_sum("total_choices").alias("total_choices")
        )
    )

    # Join stats
    combined_stats = (
        player_stats
        .join(choice_stats, "player_id", "left")
        .fillna(0, subset=["total_choices"])
        .select(
            "player_id",
            "total_saves",
            "total_choices",
            spark_round(col("total_file_size_bytes") / 1024 / 1024, 2).alias("total_size_mb")
        )
    )

    # Write to Gold layer
    (
        combined_stats
        .write
        .format("parquet")
        .mode("overwrite")
        .option("compression", "snappy")
        .save("s3a://gold/player_stats/")
    )

    print(f"Player stats aggregated. Total players: {combined_stats.count()}")
    spark.stop()


def aggregate_choice_statistics():
    """
    Aggregate choice statistics
    Creates choice_statistics table in Gold layer
    """
    spark = create_spark_session("GoldAggregation-ChoiceStats")

    # NOTE: This is a simplified version
    # In production, would read actual choice details from Silver
    
    choices_df = spark.read.parquet("s3a://silver/choices/")

    # Monthly choice statistics
    monthly_stats = (
        choices_df
        .withColumn("year", year(col("ingested_at")))
        .withColumn("month", month(col("ingested_at")))
        .groupBy("year", "month")
        .agg(
            count("save_id").alias("total_saves_with_choices"),
            spark_sum("total_choices").alias("total_choices"),
            countDistinct("player_id").alias("unique_players"),
            spark_round(avg("total_choices"), 2).alias("avg_choices_per_save")
        )
        .orderBy("year", "month")
    )

    (
        monthly_stats
        .write
        .format("parquet")
        .mode("overwrite")
        .partitionBy("year", "month")
        .option("compression", "snappy")
        .save("s3a://gold/choice_statistics/")
    )

    print(f"Choice statistics aggregated. Total months: {monthly_stats.count()}")
    spark.stop()


def aggregate_daily_metrics():
    """
    Aggregate daily platform metrics
    Creates daily_metrics table in Gold layer
    """
    spark = create_spark_session("GoldAggregation-DailyMetrics")

    saves_df = spark.read.parquet("s3a://silver/saves/")

    daily_metrics = (
        saves_df
        .groupBy("year", "month", "day")
        .agg(
            count("save_id").alias("saves_uploaded"),
            countDistinct("player_id").alias("active_players"),
            spark_sum("file_size_bytes").alias("total_bytes_uploaded")
        )
        .withColumn("avg_bytes_per_save", 
                   spark_round(col("total_bytes_uploaded") / col("saves_uploaded"), 2))
        .orderBy("year", "month", "day")
    )

    (
        daily_metrics
        .write
        .format("parquet")
        .mode("overwrite")
        .partitionBy("year", "month")
        .option("compression", "snappy")
        .save("s3a://gold/daily_metrics/")
    )

    print(f"Daily metrics aggregated. Total days: {daily_metrics.count()}")
    spark.stop()


if __name__ == "__main__":
    import sys
    
    aggregate_type = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    if aggregate_type in ["all", "player_stats"]:
        aggregate_player_stats()
    
    if aggregate_type in ["all", "choice_statistics"]:
        aggregate_choice_statistics()
    
    if aggregate_type in ["all", "daily_metrics"]:
        aggregate_daily_metrics()
    
    print("Gold layer aggregation complete!")
