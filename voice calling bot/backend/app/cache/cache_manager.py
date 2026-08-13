"""Redis cache manager providing get/set, invalidation, and caching decorators."""

import json
from functools import wraps
from typing import Any, Callable, Optional, Union
import redis.asyncio as redis
from app.database.redis import get_redis_client
from app.core.logging import get_logger

logger = get_logger(__name__)


class CacheManager:
    """Redis cache orchestration manager."""

    DEFAULT_TTL = 3600  # 1 hour

    TTL_POLICIES = {
        "agent": 21600,  # 6 hours
        "organization": 3600,  # 1 hour
        "prompt": 86400,  # 24 hours
        "knowledge_base": 43200,  # 12 hours
    }

    def __init__(self, client: Optional[redis.Redis] = None):
        self._client = client

    @property
    def client(self) -> Optional[redis.Redis]:
        if self._client:
            return self._client
        try:
            return get_redis_client()
        except Exception:
            return None

    async def get(self, key: str) -> Optional[Any]:
        """Retrieve and deserialize item from cache."""
        cli = self.client
        if not cli:
            return None
        try:
            val = await cli.get(key)
            if val:
                return json.loads(val)
            return None
        except Exception as e:
            logger.error("Cache GET failed", key=key, error=str(e))
            return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Serialize and set item in cache with TTL."""
        cli = self.client
        if not cli:
            return False
        try:
            serialized = json.dumps(value, default=str)
            expiry = ttl if ttl is not None else self.DEFAULT_TTL
            await cli.set(key, serialized, ex=expiry)
            return True
        except Exception as e:
            logger.error("Cache SET failed", key=key, error=str(e))
            return False

    async def delete(self, key: str) -> bool:
        """Delete specific key from cache."""
        cli = self.client
        if not cli:
            return False
        try:
            await cli.delete(key)
            return True
        except Exception as e:
            logger.error("Cache DELETE failed", key=key, error=str(e))
            return False

    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern (e.g. 'agent:123:*')."""
        cli = self.client
        if not cli:
            return 0
        try:
            keys = []
            async for k in cli.scan_iter(match=pattern):
                keys.append(k)
            if keys:
                return await cli.delete(*keys)
            return 0
        except Exception as e:
            logger.error("Cache invalidate pattern failed", pattern=pattern, error=str(e))
            return 0


def cache_result(prefix: str, ttl: Optional[int] = None):
    """Decorator to cache async function results in Redis."""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            manager = CacheManager()
            # Build cache key from prefix and arguments
            arg_str = ":".join([str(a) for a in args[1:]] + [f"{k}={v}" for k, v in sorted(kwargs.items())])
            key = f"cache:{prefix}:{arg_str}" if arg_str else f"cache:{prefix}:default"

            cached = await manager.get(key)
            if cached is not None:
                return cached

            result = await func(*args, **kwargs)
            if result is not None:
                await manager.set(key, result, ttl=ttl)

            return result
        return wrapper
    return decorator
