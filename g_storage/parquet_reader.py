"""
Parquet Reader for Data Lake
Handles reading Parquet files from MinIO/S3
"""
import logging
from typing import List, Dict, Any, Optional
import pandas as pd
import pyarrow.parquet as pq
from io import BytesIO

from a_configs.minio_client import get_minio
from a_configs.logging_config import get_logger

logger = get_logger(__name__)


class ParquetReader:
    """Read Parquet files from S3/MinIO"""

    def __init__(self):
        self.minio_client = get_minio()

    def read_from_bronze(
        self,
        prefix: str,
        limit: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Read raw data from Bronze layer

        Args:
            prefix: S3 prefix to read from
            limit: Maximum number of rows to return

        Returns:
            pd.DataFrame: Combined dataframe from all files
        """
        bucket = "bronze"
        
        try:
            # List all objects with the prefix
            objects = self.minio_client.list_objects(bucket, prefix=prefix, recursive=True)
            
            dataframes = []
            for obj in objects:
                if obj.object_name.endswith('.parquet'):
                    # Download object
                    response = self.minio_client.get_object(bucket, obj.object_name)
                    data = response.read()
                    
                    # Read Parquet from bytes
                    buffer = BytesIO(data)
                    df = pq.read_table(buffer).to_pandas()
                    dataframes.append(df)
                    
                    response.close()
                    response.release_conn()

            if not dataframes:
                logger.warning(f"No Parquet files found in Bronze: {prefix}")
                return pd.DataFrame()

            # Combine all dataframes
            combined_df = pd.concat(dataframes, ignore_index=True)
            
            if limit:
                combined_df = combined_df.head(limit)

            logger.info(f"Read {len(combined_df)} records from Bronze: {prefix}")
            return combined_df

        except Exception as e:
            logger.error(f"Failed to read from Bronze layer: {e}")
            raise

    def read_from_silver(
        self,
        table_name: str,
        filters: Optional[List[tuple]] = None,
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Read cleaned data from Silver layer

        Args:
            table_name: Table name to read
            filters: Optional filters (PyArrow format)
            columns: Optional columns to read

        Returns:
            pd.DataFrame: Data from Silver layer
        """
        bucket = "silver"
        prefix = table_name
        
        try:
            objects = self.minio_client.list_objects(bucket, prefix=prefix, recursive=True)
            
            dataframes = []
            for obj in objects:
                if obj.object_name.endswith('.parquet'):
                    response = self.minio_client.get_object(bucket, obj.object_name)
                    data = response.read()
                    
                    buffer = BytesIO(data)
                    table = pq.read_table(buffer, columns=columns, filters=filters)
                    df = table.to_pandas()
                    dataframes.append(df)
                    
                    response.close()
                    response.release_conn()

            if not dataframes:
                logger.warning(f"No Parquet files found in Silver: {table_name}")
                return pd.DataFrame()

            combined_df = pd.concat(dataframes, ignore_index=True)
            logger.info(f"Read {len(combined_df)} records from Silver: {table_name}")
            return combined_df

        except Exception as e:
            logger.error(f"Failed to read from Silver layer: {e}")
            raise

    def read_from_gold(self, aggregate_name: str) -> pd.DataFrame:
        """
        Read aggregated data from Gold layer

        Args:
            aggregate_name: Name of the aggregate

        Returns:
            pd.DataFrame: Aggregated data
        """
        bucket = "gold"
        prefix = aggregate_name
        
        try:
            objects = self.minio_client.list_objects(bucket, prefix=prefix, recursive=True)
            
            # Get the latest file (sorted by name which includes timestamp)
            parquet_files = [obj for obj in objects if obj.object_name.endswith('.parquet')]
            
            if not parquet_files:
                logger.warning(f"No Parquet files found in Gold: {aggregate_name}")
                return pd.DataFrame()

            # Sort by object name (which includes timestamp) and get the latest
            latest_file = sorted(parquet_files, key=lambda x: x.object_name)[-1]
            
            response = self.minio_client.get_object(bucket, latest_file.object_name)
            data = response.read()
            
            buffer = BytesIO(data)
            df = pq.read_table(buffer).to_pandas()
            
            response.close()
            response.release_conn()

            logger.info(f"Read {len(df)} records from Gold: {aggregate_name}")
            return df

        except Exception as e:
            logger.error(f"Failed to read from Gold layer: {e}")
            raise
