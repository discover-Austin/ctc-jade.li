"""
Redis cache connection and management.
"""
import redis.asyncio as redis
from typing import Optional
import logging
import json

from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis client wrapper with connection pooling."""

    def __init__(self):
        self.client: Optional[redis.Redis] = None
        self.pool: Optional[redis.ConnectionPool] = None

    async def connect(self) -> bool:
        """Initialize Redis connection pool."""
        try:
            self.pool = redis.ConnectionPool.from_url(
                settings.REDIS_URL,
                max_connections=settings.REDIS_MAX_CONNECTIONS,
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True
            )
            self.client = redis.Redis(connection_pool=self.pool)

            # Test connection
            await self.client.ping()
            logger.info("Redis connection established successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            return False

    async def disconnect(self):
        """Close Redis connection pool."""
        if self.client:
            try:
                await self.client.close()
                await self.pool.disconnect()
                logger.info("Redis connection closed successfully")
            except Exception as e:
                logger.error(f"Error closing Redis connection: {e}")

    async def check_connection(self) -> bool:
        """Check Redis connectivity."""
        if not self.client:
            return False

        try:
            await self.client.ping()
            return True
        except Exception as e:
            logger.error(f"Redis connection check failed: {e}")
            return False

    async def get(self, key: str) -> Optional[str]:
        """Get value from cache."""
        if not self.client:
            return None

        try:
            return await self.client.get(key)
        except Exception as e:
            logger.error(f"Redis GET error: {e}")
            return None

    async def set(
        self,
        key: str,
        value: str,
        expire: Optional[int] = None
    ) -> bool:
        """Set value in cache with optional expiration."""
        if not self.client:
            return False

        try:
            if expire is None:
                expire = settings.CACHE_TTL

            await self.client.set(key, value, ex=expire)
            return True
        except Exception as e:
            logger.error(f"Redis SET error: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if not self.client:
            return False

        try:
            await self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Redis DELETE error: {e}")
            return False

    async def get_json(self, key: str) -> Optional[dict]:
        """Get JSON value from cache."""
        value = await self.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON in cache key: {key}")
                return None
        return None

    async def set_json(
        self,
        key: str,
        value: dict,
        expire: Optional[int] = None
    ) -> bool:
        """Set JSON value in cache."""
        try:
            json_str = json.dumps(value)
            return await self.set(key, json_str, expire)
        except (TypeError, ValueError) as e:
            logger.error(f"Error serializing JSON: {e}")
            return False


# Global Redis client instance
redis_client = RedisClient()


async def get_redis() -> Optional[redis.Redis]:
    """Dependency to get Redis client."""
    if redis_client.client:
        return redis_client.client
    return None
