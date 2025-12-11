"""
Redis Cache Client
"""
import redis.asyncio as redis
from typing import Optional
from a_configs.settings import get_settings

settings = get_settings()


class RedisClient:
    """Async Redis client wrapper"""
    
    _instance: Optional[redis.Redis] = None
    
    @classmethod
    async def get_client(cls) -> redis.Redis:
        """Get or create Redis client instance"""
        if cls._instance is None:
            cls._instance = await redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
            )
        return cls._instance
    
    @classmethod
    async def close(cls):
        """Close Redis connection"""
        if cls._instance:
            await cls._instance.close()
            cls._instance = None


async def get_redis() -> redis.Redis:
    """Dependency for getting Redis client"""
    return await RedisClient.get_client()
