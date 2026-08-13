"""Rate limiting middleware using Redis token bucket / sliding window algorithm."""

from typing import Optional, Tuple
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import redis.asyncio as redis
from app.core.logging import get_logger

logger = get_logger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware backed by Redis."""

    EXCLUDED_PATHS = {
        "/api/docs",
        "/api/redoc",
        "/api/openapi.json",
        "/api/v1/health",
        "/api/v1/health/live",
        "/api/v1/health/ready",
        "/metrics",
    }

    def __init__(
        self,
        app,
        redis_client: Optional[redis.Redis] = None,
        default_limit: int = 100,
        default_window: int = 60,
    ):
        super().__init__(app)
        self.redis = redis_client
        self.default_limit = default_limit
        self.default_window = default_window
        self.rate_limits = {
            "default": (100, 60),  # 100 requests per 60s
            "auth": (10, 60),  # 10 requests per 60s (login/register)
            "ai_heavy": (20, 60),  # 20 heavy compute/AI calls per 60s
        }

    def _get_category(self, path: str) -> Tuple[str, int, int]:
        if "/auth/" in path:
            cat = "auth"
        elif "/playground/" in path or "/analytics/" in path:
            cat = "ai_heavy"
        else:
            cat = "default"

        limit, window = self.rate_limits.get(cat, (self.default_limit, self.default_window))
        return cat, limit, window

    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for excluded routes or if Redis isn't active
        path = request.url.path
        if any(path.startswith(p) for p in self.EXCLUDED_PATHS) or self.redis is None:
            return await call_next(request)

        # Get client identity (Authenticated user ID or Client IP)
        user_id = getattr(request.state, "user_id", None)
        client_ip = request.client.host if request.client else "127.0.0.1"
        identifier = f"user:{user_id}" if user_id else f"ip:{client_ip}"

        category, limit, window = self._get_category(path)
        key = f"ratelimit:{identifier}:{category}"

        try:
            current = await self.redis.incr(key)
            if current == 1:
                await self.redis.expire(key, window)

            ttl = await self.redis.ttl(key)
            ttl = ttl if ttl > 0 else window

            if current > limit:
                logger.warning(
                    "Rate limit exceeded",
                    identifier=identifier,
                    category=category,
                    current=current,
                    limit=limit,
                )
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "Too Many Requests",
                        "message": f"Rate limit exceeded. Try again in {ttl} seconds.",
                        "category": category,
                        "retry_after": ttl,
                    },
                    headers={
                        "Retry-After": str(ttl),
                        "X-RateLimit-Limit": str(limit),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(ttl),
                    },
                )
        except Exception as e:
            # Fallback gracefully if Redis operation errors out
            logger.error("Rate limiter Redis failure", error=str(e))
            return await call_next(request)

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(limit)
        try:
            response.headers["X-RateLimit-Remaining"] = str(max(0, limit - current))
            response.headers["X-RateLimit-Reset"] = str(ttl)
        except UnboundLocalError:
            pass
        return response
