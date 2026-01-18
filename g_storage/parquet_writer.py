"""
Parquet Writer for Data Lake
Handles writing data to Parquet format in MinIO/S3
"""
import logging
from typing import List, Dict, Any
from datetime import datetime
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from io import BytesIO

from a_configs.minio_client import get_minio
from a_configs.logging_config import get_logger

logger = get_logger(__name__)


class ParquetWriter:
    """Write data to Parquet files in S3/MinIO"""

    def __init__(self):
        self.minio_client = get_minio()

    def write_to_bronze(
        self,
        data: List[Dict[str, Any]],
        prefix: str,
        partition_key: str = None
    ) -> str:
        """
        Write raw data to Bronze layer

        Args:
            data: List of dictionaries to write
            prefix: S3 prefix (e.g., 'saves', 'choices')
            partition_key: Optional partition key (e.g., 'date=2026-07-07')

        Returns:
            str: S3 path of written file
        """
        bucket = "bronze"
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
        if partition_key:
            s3_key = f"{prefix}/{partition_key}/{timestamp}.parquet"
        else:
            s3_key = f"{prefix}/{timestamp}.parquet"

        # Convert to DataFrame and then Parquet
        df = pd.DataFrame(data)
        table = pa.Table.from_pandas(df)

        # Write to buffer
        buffer = BytesIO()
        pq.write_table(table, buffer, compression='snappy')
        buffer.seek(0)

        # Upload to MinIO
        try:
            self.minio_client.put_object(
                bucket,
                s3_key,
                buffer,
                length=buffer.getbuffer().nbytes,
                content_type='application/octet-stream'
            )
            
            s3_path = f"s3://{bucket}/{s3_key}"
            logger.info(f"Wrote {len(data)} records to Bronze: {s3_path}")
            return s3_path

        except Exception as e:
            logger.error(f"Failed to write to Bronze layer: {e}")
            raise

    def write_to_silver(
        self,
        data: List[Dict[str, Any]],
        table_name: str,
        partition_columns: List[str] = None
    ) -> str:
        """
        Write cleaned data to Silver layer with partitioning

        Args:
            data: List of dictionaries to write
            table_name: Table name (e.g., 'choices', 'players')
            partition_columns: Columns to partition by (e.g., ['year', 'month'])

        Returns:
            str: S3 path of written file/directory
        """
        bucket = "silver"
        
        df = pd.DataFrame(data)
        table = pa.Table.from_pandas(df)

        if partition_columns:
            # Partitioned write
            base_path = f"s3://{bucket}/{table_name}"
            
            # Note: This is simplified - actual implementation would use
            # PyArrow Dataset API for proper partitioning
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            s3_key = f"{table_name}/{timestamp}.parquet"
        else:
            # Non-partitioned write
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            s3_key = f"{table_name}/{timestamp}.parquet"

        buffer = BytesIO()
        pq.write_table(table, buffer, compression='snappy')
        buffer.seek(0)

        try:
            self.minio_client.put_object(
                bucket,
                s3_key,
                buffer,
                length=buffer.getbuffer().nbytes,
                content_type='application/octet-stream'
            )
            
            s3_path = f"s3://{bucket}/{s3_key}"
            logger.info(f"Wrote {len(data)} records to Silver: {s3_path}")
            return s3_path

        except Exception as e:
            logger.error(f"Failed to write to Silver layer: {e}")
            raise

    def write_to_gold(
        self,
        data: List[Dict[str, Any]],
        aggregate_name: str
    ) -> str:
        """
        Write aggregated data to Gold layer

        Args:
            data: Aggregated data
            aggregate_name: Name of the aggregate (e.g., 'choice_statistics')

        Returns:
            str: S3 path of written file
        """
        bucket = "gold"
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        s3_key = f"{aggregate_name}/{timestamp}.parquet"

        df = pd.DataFrame(data)
        table = pa.Table.from_pandas(df)

        buffer = BytesIO()
        pq.write_table(table, buffer, compression='snappy')
        buffer.seek(0)

        try:
            self.minio_client.put_object(
                bucket,
                s3_key,
                buffer,
                length=buffer.getbuffer().nbytes,
                content_type='application/octet-stream'
            )
            
            s3_path = f"s3://{bucket}/{s3_key}"
            logger.info(f"Wrote {len(data)} records to Gold: {s3_path}")
            return s3_path

        except Exception as e:
            logger.error(f"Failed to write to Gold layer: {e}")
            raise
