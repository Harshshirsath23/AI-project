from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.agents import router as agents_router
from app.api.phone_numbers import router as phone_numbers_router
from app.api.leads import router as leads_router
from app.api.knowledge_base import router as knowledge_base_router
from app.api.voices import router as voices_router
from app.api.analytics import router as analytics_router
from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.invitations import router as invitations_router
from app.api.organization_members import router as organization_members_router
from app.api.organizations import router as organizations_router
from app.api.users import router as users_router
from app.api.calls import router as calls_router
from app.api.campaigns import router as campaigns_router
from app.api.settings import router as settings_router
from app.api.playground import router as playground_router
from app.api.webhooks import router as webhooks_router

from app.config.settings import get_settings
from app.core.logging import configure_logging, get_logger
from app.database.connection import close_db, init_db
from app.database.redis import close_redis, init_redis

logger = get_logger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting application", version=settings.app_version, environment=settings.app_env)
    configure_logging()
    await init_db()
    await init_redis()
    logger.info("Application startup complete")

    yield

    # Shutdown
    logger.info("Shutting down application")
    await close_db()
    await close_redis()
    logger.info("Application shutdown complete")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Enterprise AI Calling Platform - Production-ready multi-tenant AI voice agent system",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Middleware: add Bypass-Tunnel-Reminder header so localtunnel doesn't intercept Twilio requests
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.requests import Request as StarletteRequest

    class LocalTunnelBypassMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: StarletteRequest, call_next):
            response = await call_next(request)
            response.headers["Bypass-Tunnel-Reminder"] = "anyvalue"
            return response

    app.add_middleware(LocalTunnelBypassMiddleware)

    # Include routers
    app.include_router(health_router, prefix=settings.api_prefix, tags=["health"])
    app.include_router(auth_router, prefix=settings.api_prefix)
    app.include_router(users_router, prefix=settings.api_prefix)
    app.include_router(organizations_router, prefix=settings.api_prefix)
    app.include_router(organization_members_router, prefix=settings.api_prefix)
    app.include_router(invitations_router, prefix=settings.api_prefix)
    app.include_router(agents_router, prefix=f"{settings.api_prefix}/agents", tags=["agents"])
    app.include_router(phone_numbers_router, prefix=f"{settings.api_prefix}/phone-numbers", tags=["phone-numbers"])
    app.include_router(leads_router, prefix=f"{settings.api_prefix}/leads", tags=["leads"])
    app.include_router(knowledge_base_router, prefix=f"{settings.api_prefix}/knowledge-base", tags=["knowledge-base"])
    app.include_router(voices_router, prefix=f"{settings.api_prefix}/voices", tags=["voices"])
    app.include_router(analytics_router, prefix=f"{settings.api_prefix}/analytics", tags=["analytics"])
    app.include_router(settings_router, prefix=f"{settings.api_prefix}/settings", tags=["settings"])
    app.include_router(playground_router, prefix=f"{settings.api_prefix}/playground", tags=["playground"])

    app.include_router(calls_router, prefix=f"{settings.api_prefix}/calls", tags=["calls"])


    app.include_router(campaigns_router, prefix=f"{settings.api_prefix}/campaigns", tags=["campaigns"])
    app.include_router(webhooks_router, prefix=f"{settings.api_prefix}/webhooks", tags=["webhooks"])
    app.include_router(webhooks_router, prefix="/webhooks", tags=["webhooks"])

    return app




app = create_app()
