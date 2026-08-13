"""Integration tests for health probes and metrics endpoints."""

import pytest


@pytest.mark.asyncio
async def test_liveness_probe(client):
    """Verify /health/live returns HTTP 200 and alive status."""
    response = await client.get("/api/v1/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_metrics_endpoint(client):
    """Verify /metrics returns Prometheus format text response."""
    response = await client.get("/api/v1/metrics")
    assert response.status_code == 200
    assert "api_requests_total" in response.text
