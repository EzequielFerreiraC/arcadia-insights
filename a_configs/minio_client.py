"""
MinIO / S3 Client Configuration
"""
from minio import Minio
from typing import Optional
from a_configs.settings import get_settings

settings = get_settings()


class MinIOClient:
    """MinIO client wrapper"""
    
    _instance: Optional[Minio] = None
    
    @classmethod
    def get_client(cls) -> Minio:
        """Get or create MinIO client instance"""
        if cls._instance is None:
            cls._instance = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=settings.MINIO_SECURE,
            )
            
            # Create buckets if they don't exist
            for bucket in [
                settings.MINIO_BUCKET_BRONZE,
                settings.MINIO_BUCKET_SILVER,
                settings.MINIO_BUCKET_GOLD,
            ]:
                if not cls._instance.bucket_exists(bucket):
                    cls._instance.make_bucket(bucket)
        
        return cls._instance


def get_minio() -> Minio:
    """Dependency for getting MinIO client"""
    return MinIOClient.get_client()
