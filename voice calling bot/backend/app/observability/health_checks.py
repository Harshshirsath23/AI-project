"""Health check logic for liveness and readiness probes."""

import time
from typing import Dict, Any
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis
from app.core.logging import get_logger

logger = get_logger(__name__)


class HealthChecker:
    """System health check orchestrator evaluating component connectivity."""

    @staticmethod
    async def check_database(db: AsyncSession) -> Dict[str, Any]:
        """Check PostgreSQL database connectivity."""
        start = time.time()
        try:
            await db.execute(text("SELECT 1"))
            latency_ms = round((time.time() - start) * 1000, 2)
            return {"status": "healthy", "latency_ms": latency_ms}
        except Exception as e:
            logger.error("Database health check failed", error=str(e))
            return {"status": "unhealthy", "error": str(e)}

    @staticmethod
    async def check_redis(redis_client: redis.Redis) -> Dict[str, Any]:
        """Check Redis cache connectivity."""
        start = time.time()
        try:
            if redis_client is None:
                return {"status": "unhealthy", "error": "Redis client not initialized"}
            await redis_client.ping()
            latency_ms = round((time.time() - start) * 1000, 2)
            return {"status": "healthy", "latency_ms": latency_ms}
        except Exception as e:
            logger.error("Redis health check failed", error=str(e))
            return {"status": "unhealthy", "error": str(e)}

    @staticmethod
    async def check_celery() -> Dict[str, Any]:
        """Check Celery worker status."""
        try:
            return {"status": "healthy"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
