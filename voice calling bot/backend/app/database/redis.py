import redis.asyncio as redis
from redis.asyncio import Redis

from app.config.settings import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

settings = get_settings()

# Redis connection pool
redis_pool = redis.ConnectionPool.from_url(
    settings.redis_url,
    max_connections=settings.redis_max_connections,
    decode_responses=True,
)


async def get_redis() -> Redis:
    """Dependency for getting Redis client."""
    return redis.Redis(connection_pool=redis_pool)


def get_redis_client() -> Redis:
    """Get synchronous/instance access to Redis client using connection pool."""
    return redis.Redis(connection_pool=redis_pool)



async def init_redis() -> None:
    """Initialize Redis connection."""
    try:
        client = redis.Redis(connection_pool=redis_pool)
        await client.ping()
        logger.info("Redis connection established successfully")
    except Exception as e:
        logger.warning("Failed to establish Redis connection", error=str(e))
        if settings.is_production:
            raise


async def close_redis() -> None:
    """Close Redis connection."""
    await redis_pool.disconnect()
    logger.info("Redis connection closed")
