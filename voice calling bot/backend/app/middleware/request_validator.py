"""Input request validation and payload sanity middleware."""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.core.logging import get_logger

logger = get_logger(__name__)


class RequestValidatorMiddleware(BaseHTTPMiddleware):
    """Validate incoming request content-types and payload sizes."""

    EXCLUDED_PATHS = ["/api/docs", "/api/redoc", "/api/openapi.json", "/api/v1/health"]
    MAX_PAYLOAD_SIZE = 15 * 1024 * 1024  # 15MB limit for audio/lead file uploads

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Skip validation for docs and health checks
        if any(path.startswith(p) for p in self.EXCLUDED_PATHS):
            return await call_next(request)

        # Content-Length check for mutating HTTP methods
        if request.method in ["POST", "PUT", "PATCH"]:
            content_length = request.headers.get("content-length")
            if content_length and int(content_length) > self.MAX_PAYLOAD_SIZE:
                logger.warning(
                    "Payload size exceeded",
                    path=path,
                    method=request.method,
                    content_length=content_length,
                )
                return JSONResponse(
                    status_code=413,
                    content={
                        "error": "Payload Too Large",
                        "message": f"Request body exceeds maximum allowed limit of {self.MAX_PAYLOAD_SIZE // (1024 * 1024)}MB.",
                    },
                )

        return await call_next(request)
