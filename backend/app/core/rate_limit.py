"""
Rate limiting middleware using Redis.
"""
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import time
import redis.asyncio as redis
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using Redis.

    Implements a sliding window rate limiter with Redis.
    """

    def __init__(self, app, redis_client: redis.Redis = None):
        super().__init__(app)
        self.redis_client = redis_client
        self.enabled = settings.RATE_LIMIT_ENABLED

    async def dispatch(self, request: Request, call_next: Callable):
        """Process request with rate limiting."""
        if not self.enabled or not self.redis_client:
            return await call_next(request)

        # Skip rate limiting for health check endpoints
        if request.url.path in ["/health", "/ready"]:
            return await call_next(request)

        # Get client identifier (IP address or API key)
        client_id = self._get_client_identifier(request)

        # Check rate limit
        try:
            is_allowed = await self._check_rate_limit(client_id)
            if not is_allowed:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded. Please try again later.",
                    headers={
                        "X-RateLimit-Limit": str(settings.RATE_LIMIT_PER_MINUTE),
                        "X-RateLimit-Reset": str(int(time.time()) + 60)
                    }
                )
        except redis.RedisError as e:
            # Log error but don't block request if Redis is down
            logger.error(f"Redis error in rate limiter: {e}")

        # Process request
        response = await call_next(request)

        # Add rate limit headers
        try:
            remaining = await self._get_remaining_requests(client_id)
            response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_PER_MINUTE)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 60)
        except redis.RedisError:
            pass

        return response

    def _get_client_identifier(self, request: Request) -> str:
        """Get unique client identifier for rate limiting."""
        # Try to get API key from header
        api_key = request.headers.get("X-API-Key")
        if api_key:
            return f"api_key:{api_key[:16]}"  # Use first 16 chars to avoid long keys

        # Fall back to IP address
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            ip = forwarded_for.split(",")[0].strip()
        else:
            ip = request.client.host if request.client else "unknown"

        return f"ip:{ip}"

    async def _check_rate_limit(self, client_id: str) -> bool:
        """
        Check if client is within rate limit using sliding window.

        Returns:
            True if request is allowed, False if rate limit exceeded
        """
        if not self.redis_client:
            return True

        now = time.time()
        window_start = now - 60  # 1 minute window

        key = f"rate_limit:{client_id}"

        # Use Redis pipeline for atomic operations
        pipe = self.redis_client.pipeline()

        # Remove old entries outside the window
        pipe.zremrangebyscore(key, 0, window_start)

        # Count requests in current window
        pipe.zcard(key)

        # Add current request
        pipe.zadd(key, {str(now): now})

        # Set expiration
        pipe.expire(key, 60)

        results = await pipe.execute()

        # Get count before adding current request
        current_count = results[1]

        # Check if limit exceeded
        return current_count < settings.RATE_LIMIT_PER_MINUTE

    async def _get_remaining_requests(self, client_id: str) -> int:
        """Get remaining requests for client in current window."""
        if not self.redis_client:
            return settings.RATE_LIMIT_PER_MINUTE

        now = time.time()
        window_start = now - 60

        key = f"rate_limit:{client_id}"

        try:
            # Count requests in current window
            count = await self.redis_client.zcount(key, window_start, now)
            remaining = max(0, settings.RATE_LIMIT_PER_MINUTE - count)
            return remaining
        except redis.RedisError:
            return settings.RATE_LIMIT_PER_MINUTE
