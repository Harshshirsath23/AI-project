"""Correlation ID middleware for distributed request tracing."""

import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import structlog


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """Assign or propagate unique correlation IDs across HTTP requests and logs."""

    HEADER_NAME = "X-Correlation-ID"

    async def dispatch(self, request: Request, call_next):
        # Extract existing header or generate fresh UUID
        correlation_id = request.headers.get(self.HEADER_NAME, str(uuid.uuid4()))
        request.state.correlation_id = correlation_id

        # Bind correlation ID to structlog context
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            correlation_id=correlation_id,
            path=request.url.path,
            method=request.method,
        )

        response = await call_next(request)
        response.headers[self.HEADER_NAME] = correlation_id
        return response
