"""Health check and telemetry endpoints."""

from datetime import UTC, datetime
from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis

from app.config.settings import get_settings
from app.core.logging import get_logger
from app.database.connection import get_async_db
from app.database.redis import get_redis
from app.observability.health_checks import HealthChecker
from app.observability.metrics import metrics_endpoint_handler

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
async def health_check(
    db: AsyncSession = Depends(get_async_db),
    redis_client: redis.Redis = Depends(get_redis),
) -> HealthResponse:
    """Comprehensive system health check endpoint."""
    db_res = await HealthChecker.check_database(db)
    redis_res = await HealthChecker.check_redis(redis_client)

    db_status = "connected" if db_res["status"] == "healthy" else "disconnected"
    redis_status = "connected" if redis_res["status"] == "healthy" else "disconnected"

    overall_status = "healthy" if db_status == "connected" and redis_status == "connected" else "degraded"

    return HealthResponse(
        status=overall_status,
        timestamp=datetime.now(UTC),
        version=settings.app_version,
        environment=settings.app_env,
        database=db_status,
        redis=redis_status,
    )


@router.get("/health/live")
async def liveness_probe():
    """Kubernetes / Load Balancer liveness probe endpoint."""
    return {"status": "alive", "timestamp": datetime.now(UTC).isoformat()}


@router.get("/health/ready")
async def readiness_probe(
    db: AsyncSession = Depends(get_async_db),
    redis_client: redis.Redis = Depends(get_redis),
):
    """Kubernetes / Load Balancer readiness probe endpoint."""
    db_check = await HealthChecker.check_database(db)
    redis_check = await HealthChecker.check_redis(redis_client)
    celery_check = await HealthChecker.check_celery()

    checks = {
        "database": db_check,
        "redis": redis_check,
        "celery": celery_check,
    }

    all_healthy = all(c.get("status") == "healthy" for c in checks.values())

    return {
        "status": "ready" if all_healthy else "not_ready",
        "timestamp": datetime.now(UTC).isoformat(),
        "checks": checks,
    }


@router.get("/metrics")
async def prometheus_metrics():
    """Prometheus telemetry metrics endpoint."""
    return metrics_endpoint_handler()
