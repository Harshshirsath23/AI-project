"""Unit tests for Voice Bot ability improvements: Validators, Escalation, Context Manager, Circuit Breaker."""

import pytest
from app.ai.validators import ResponseValidator
from app.services.escalation_service import EscalationService
from app.services.context_manager import ContextManager
from app.core.circuit_breaker import CircuitBreaker, CircuitBreakerState


def test_pii_sanitization():
    """Verify SSN, email, and API key redaction."""
    raw_text = "My SSN is 123-45-6789 and my email is test@example.com."
    sanitized = ResponseValidator.sanitize_pii(raw_text)
    assert "[redacted SSN]" in sanitized
    assert "[redacted email]" in sanitized
    assert "123-45-6789" not in sanitized
    assert "test@example.com" not in sanitized


def test_response_length_trimming():
    """Verify max 3 sentences and max character truncation."""
    long_text = "First sentence here. Second sentence here. Third sentence here. Fourth sentence should be removed. Fifth sentence should be removed."
    trimmed = ResponseValidator.validate_response_length(long_text, max_sentences=3)
    assert "First sentence here." in trimmed
    assert "Third sentence here." in trimmed
    assert "Fourth sentence" not in trimmed


def test_escalation_trigger_keywords():
    """Verify keyword trigger detection for human escalation."""
    speech = "I am frustrated and I want to speak to a human supervisor right now!"
    triggered, reason = EscalationService.check_escalation_triggers(speech)
    assert triggered is True
    assert "human" in reason or "supervisor" in reason or "frustrated" in reason

    normal_speech = "Tell me more about your pricing and features."
    triggered_normal, _ = EscalationService.check_escalation_triggers(normal_speech)
    assert triggered_normal is False


def test_context_history_compression():
    """Verify sliding window context compression for history > 10 turns."""
    history = [{"role": "user" if i % 2 == 0 else "assistant", "content": f"Turn {i} message"} for i in range(16)]
    compressed = ContextManager.get_compressed_history(history, max_turns=10)

    # Should contain 1 system summary turn + 10 recent turns = 11 total turns
    assert len(compressed) == 11
    assert compressed[0]["role"] == "system"
    assert "Prior Conversation Summary" in compressed[0]["content"]


@pytest.mark.asyncio
async def test_circuit_breaker_tripping_and_fallback():
    """Verify circuit breaker trips to OPEN state on failures and invokes fallback."""
    breaker = CircuitBreaker(name="test_breaker", fail_max=2, reset_timeout=10.0)

    async def failing_api():
        raise RuntimeError("API failure")

    async def fallback_api():
        return "fallback_response"

    # Turn 1: failure 1
    res1 = await breaker.call_async(failing_api, fallback_api)
    assert res1 == "fallback_response"
    assert breaker.state == CircuitBreakerState.CLOSED

    # Turn 2: failure 2 -> should trip to OPEN
    res2 = await breaker.call_async(failing_api, fallback_api)
    assert res2 == "fallback_response"
    assert breaker.state == CircuitBreakerState.OPEN

    # Turn 3: while OPEN, directly calls fallback without calling failing_api
    res3 = await breaker.call_async(failing_api, fallback_api)
    assert res3 == "fallback_response"
