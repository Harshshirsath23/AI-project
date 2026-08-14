from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.modules.auth.api import router as auth_router
from app.modules.organizations.api import router as org_router
from app.modules.candidates.api import router as candidates_router
from app.modules.recruitment.api import router as recruitment_router
from app.modules.interviews.api import router as interviews_router
from app.modules.offers.api import router as offers_router
from app.modules.communication.api import router as communication_router
from app.modules.ai.api import router as ai_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise Multi-Tenant AI Platform Backend",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.modules.platform.api import router as platform_router
from app.modules.organizations.org_admin_api import router as org_admin_router
from app.modules.ai.copilot.api import router as copilot_router

# Include Router Modules
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(platform_router, prefix=f"{settings.API_V1_STR}/platform")
app.include_router(org_admin_router, prefix=settings.API_V1_STR)
app.include_router(org_router, prefix=f"{settings.API_V1_STR}/organizations")
app.include_router(candidates_router, prefix=f"{settings.API_V1_STR}/candidates")
app.include_router(recruitment_router, prefix=f"{settings.API_V1_STR}/recruitment")
app.include_router(interviews_router, prefix=f"{settings.API_V1_STR}/interviews")
app.include_router(offers_router, prefix=f"{settings.API_V1_STR}/offers")
app.include_router(communication_router, prefix=f"{settings.API_V1_STR}/communication")
app.include_router(ai_router, prefix=f"{settings.API_V1_STR}/ai")
app.include_router(copilot_router, prefix=f"{settings.API_V1_STR}/ai")

@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs"
    }
