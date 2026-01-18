"""
S3 Storage Manager
Handles general S3/MinIO operations
"""
import logging
from typing import List, Optional
from datetime import datetime, timedelta

from a_configs.minio_client import get_minio
from a_configs.logging_config import get_logger

logger = get_logger(__name__)


class S3Storage:
    """Manage S3/MinIO storage operations"""

    def __init__(self):
        self.client = get_minio()

    def upload_raw_file(
        self,
        bucket: str,
        file_path: str,
        file_data: bytes,
        metadata: dict = None
    ) -> str:
        """
        Upload raw file to S3

        Args:
            bucket: Bucket name
            file_path: S3 object key
            file_data: File data as bytes
            metadata: Optional metadata dictionary

        Returns:
            str: S3 URI of uploaded file
        """
        from io import BytesIO

        try:
            buffer = BytesIO(file_data)
            
            self.client.put_object(
                bucket,
                file_path,
                buffer,
                length=len(file_data),
                metadata=metadata
            )
            
            s3_uri = f"s3://{bucket}/{file_path}"
            logger.info(f"Uploaded file to S3: {s3_uri}")
            return s3_uri

        except Exception as e:
            logger.error(f"Failed to upload file to S3: {e}")
            raise

    def download_file(self, bucket: str, object_key: str) -> bytes:
        """
        Download file from S3

        Args:
            bucket: Bucket name
            object_key: S3 object key

        Returns:
            bytes: File data
        """
        try:
            response = self.client.get_object(bucket, object_key)
            data = response.read()
            
            response.close()
            response.release_conn()
            
            logger.info(f"Downloaded file from S3: s3://{bucket}/{object_key}")
            return data

        except Exception as e:
            logger.error(f"Failed to download file from S3: {e}")
            raise

    def list_files(
        self,
        bucket: str,
        prefix: str = "",
        recursive: bool = True
    ) -> List[str]:
        """
        List files in S3 bucket

        Args:
            bucket: Bucket name
            prefix: Optional prefix filter
            recursive: Whether to list recursively

        Returns:
            List[str]: List of object keys
        """
        try:
            objects = self.client.list_objects(
                bucket,
                prefix=prefix,
                recursive=recursive
            )
            
            object_keys = [obj.object_name for obj in objects]
            logger.info(f"Listed {len(object_keys)} files from s3://{bucket}/{prefix}")
            return object_keys

        except Exception as e:
            logger.error(f"Failed to list files from S3: {e}")
            raise

    def delete_file(self, bucket: str, object_key: str):
        """
        Delete file from S3

        Args:
            bucket: Bucket name
            object_key: S3 object key
        """
        try:
            self.client.remove_object(bucket, object_key)
            logger.info(f"Deleted file from S3: s3://{bucket}/{object_key}")

        except Exception as e:
            logger.error(f"Failed to delete file from S3: {e}")
            raise

    def get_presigned_url(
        self,
        bucket: str,
        object_key: str,
        expires_in: int = 3600
    ) -> str:
        """
        Generate presigned URL for temporary access

        Args:
            bucket: Bucket name
            object_key: S3 object key
            expires_in: Expiration time in seconds (default 1 hour)

        Returns:
            str: Presigned URL
        """
        try:
            url = self.client.presigned_get_object(
                bucket,
                object_key,
                expires=timedelta(seconds=expires_in)
            )
            
            logger.info(f"Generated presigned URL for s3://{bucket}/{object_key}")
            return url

        except Exception as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            raise
