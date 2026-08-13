"""Prometheus metrics definitions and metrics middleware."""

import time
from fastapi import Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# API Metrics
api_requests_total = Counter(
    "api_requests_total",
    "Total number of HTTP API requests",
    ["method", "endpoint", "status"],
)

api_request_duration_seconds = Histogram(
    "api_request_duration_seconds",
    "HTTP API request duration in seconds",
    ["method", "endpoint"],
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)

# Call Metrics
calls_processed_total = Counter(
    "calls_processed_total",
    "Total AI voice calls processed",
    ["status"],  # completed, failed, busy, no_answer
)

call_duration_seconds = Histogram(
    "call_duration_seconds",
    "Call duration in seconds",
    buckets=(10, 30, 60, 120, 300, 600, 1800),
)

active_calls = Gauge(
    "active_calls_count",
    "Number of currently active calls",
)

# Queue & Agent Metrics
celery_tasks_queued = Gauge(
    "celery_tasks_queued_count",
    "Current Celery queue depth",
    ["queue_name"],
)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware collecting HTTP request telemetry for Prometheus."""

    EXCLUDED_PATHS = {"/metrics", "/api/v1/health", "/api/v1/health/live", "/api/v1/health/ready"}

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if path in self.EXCLUDED_PATHS:
            return await call_next(request)

        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        status = str(response.status_code)
        method = request.method

        api_requests_total.labels(method=method, endpoint=path, status=status).inc()
        api_request_duration_seconds.labels(method=method, endpoint=path).observe(duration)

        return response


def metrics_endpoint_handler() -> Response:
    """FastAPI endpoint handler serving Prometheus metrics."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
