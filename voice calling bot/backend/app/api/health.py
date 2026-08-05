from datetime import UTC, datetime

from fastapi import APIRouter
from pydantic import BaseModel

from app.config.settings import get_settings
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)
settings = get_settings()


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    timestamp: datetime
    version: str
    environment: str
    database: str
    redis: str


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint to verify system status."""
    try:
        # Check database connection
        from sqlalchemy import text
        from app.database.connection import engine

        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        database_status = "connected"
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        database_status = "disconnected"

    try:
        # Check Redis connection
        from app.database.redis import redis_pool

        import redis.asyncio as redis

        client = redis.Redis(connection_pool=redis_pool)
        await client.ping()
        redis_status = "connected"
    except Exception as e:
        logger.error("Redis health check failed", error=str(e))
        redis_status = "disconnected"

    overall_status = "healthy" if database_status == "connected" and redis_status == "connected" else "degraded"

    return HealthResponse(
        status=overall_status,
        timestamp=datetime.now(UTC),
        version=settings.app_version,
        environment=settings.app_env,
        database=database_status,
        redis=redis_status,
    )
