"""
Application Settings - Environment Configuration
"""
from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_ENV: str = "development"
    API_RELOAD: bool = True
    
    # Database - PostgreSQL (OLTP)
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "arcadia"
    POSTGRES_PASSWORD: str = "arcadia123"
    POSTGRES_DB: str = "arcadia_db"
    
    @property
    def POSTGRES_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Database - ClickHouse (OLAP)
    CLICKHOUSE_HOST: str = "localhost"
    CLICKHOUSE_PORT: int = 8123
    CLICKHOUSE_USER: str = "default"
    CLICKHOUSE_PASSWORD: str = ""
    CLICKHOUSE_DB: str = "arcadia"
    
    # Redis Cache
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "arcadia123"
    REDIS_DB: int = 0
    
    @property
    def REDIS_URL(self) -> str:
        return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # MinIO / S3
    MINIO_ENDPOINT: str = "localhost:9002"
    MINIO_ACCESS_KEY: str = "arcadia-admin"
    MINIO_SECRET_KEY: str = "arcadia-secret-key-123"
    MINIO_SECURE: bool = False
    MINIO_BUCKET_BRONZE: str = "bronze"
    MINIO_BUCKET_SILVER: str = "silver"
    MINIO_BUCKET_GOLD: str = "gold"
    
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC_SAVES_UPLOADED: str = "saves.uploaded"
    KAFKA_TOPIC_CHOICES_EXTRACTED: str = "choices.extracted"
    KAFKA_TOPIC_EVENTS_DOMAIN: str = "events.domain"

    # Pipeline
    # "inline" → API extracts choices synchronously on upload (works with just Postgres).
    # "kafka"  → API only publishes saves.uploaded; the worker extracts choices.
    PIPELINE_MODE: str = "inline"
    # Attempt to store raw saves in MinIO (Bronze). Off by default so inline dev
    # does not block when MinIO is unavailable.
    STORAGE_ENABLED: bool = False
    # Publish domain events to Kafka. Off by default for the same reason.
    EVENTS_ENABLED: bool = False
    
    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
    
    @property
    def CORS_ORIGINS_LIST(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
