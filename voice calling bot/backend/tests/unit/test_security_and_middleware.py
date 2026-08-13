"""Unit tests for encryption service and security middleware."""

import pytest
from app.security.encryption import EncryptionService


def test_encryption_decryption_roundtrip():
    """Verify encryption and decryption roundtrip integrity."""
    service = EncryptionService()
    secret_text = "super_secret_twilio_auth_token_12345"

    encrypted = service.encrypt(secret_text)
    assert encrypted is not None
    assert encrypted != secret_text

    decrypted = service.decrypt(encrypted)
    assert decrypted == secret_text


def test_encryption_none_handling():
    """Verify safe handling of None values."""
    service = EncryptionService()
    assert service.encrypt(None) is None
    assert service.decrypt(None) is None


@pytest.mark.asyncio
async def test_correlation_id_middleware(client):
    """Verify X-Correlation-ID header is generated and returned."""
    response = await client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert "X-Correlation-ID" in response.headers


@pytest.mark.asyncio
async def test_security_headers_middleware(client):
    """Verify OWASP security headers present on responses."""
    response = await client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-XSS-Protection"] == "1; mode=block"
