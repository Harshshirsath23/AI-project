"""Circuit breaker pattern for external API resilience (LLM, Telephony, DB)."""

import time
from enum import Enum
from typing import Callable, Any, Optional
from app.core.logging import get_logger

logger = get_logger(__name__)


class CircuitBreakerState(Enum):
    CLOSED = "CLOSED"      # Normal operation
    OPEN = "OPEN"          # Breaker tripped, calls redirected to fallback
    HALF_OPEN = "HALF_OPEN"# Testing provider recovery


class CircuitBreaker:
    """Circuit breaker preventing cascading failures when external APIs trip."""

    def __init__(
        self,
        name: str = "default_breaker",
        fail_max: int = 5,
        reset_timeout: float = 60.0,
    ):
        self.name = name
        self.fail_max = fail_max
        self.reset_timeout = reset_timeout

        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.last_state_change: float = time.time()

    def _check_state_transition(self):
        """Check if OPEN state reset timeout has elapsed to enter HALF_OPEN state."""
        now = time.time()
        if self.state == CircuitBreakerState.OPEN:
            if now - self.last_state_change >= self.reset_timeout:
                logger.info("Circuit breaker entering HALF_OPEN test state", breaker=self.name)
                self.state = CircuitBreakerState.HALF_OPEN
                self.last_state_change = now

    async def call_async(self, func: Callable, fallback_func: Callable, *args, **kwargs) -> Any:
        """Execute async function wrapped in circuit breaker."""
        self._check_state_transition()

        if self.state == CircuitBreakerState.OPEN:
            logger.warning(
                "Circuit breaker is OPEN. Fast-failing to fallback response.",
                breaker=self.name,
            )
            if fallback_func:
                return await fallback_func(*args, **kwargs)
            return None

        try:
            result = await func(*args, **kwargs)
            # Successful call resets breaker
            if self.state == CircuitBreakerState.HALF_OPEN:
                logger.info("Circuit breaker recovered to CLOSED", breaker=self.name)
                self.state = CircuitBreakerState.CLOSED
                self.failure_count = 0
                self.last_state_change = time.time()
            return result

        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            logger.error(
                "Circuit breaker recorded failure",
                breaker=self.name,
                count=self.failure_count,
                error=str(e),
            )

            if self.failure_count >= self.fail_max and self.state != CircuitBreakerState.OPEN:
                logger.error("Circuit breaker TRIPPED to OPEN state", breaker=self.name)
                self.state = CircuitBreakerState.OPEN
                self.last_state_change = time.time()

            if fallback_func:
                return await fallback_func(*args, **kwargs)
            raise e


# Global instances
llm_circuit_breaker = CircuitBreaker(name="llm_gemini", fail_max=5, reset_timeout=30.0)
telephony_circuit_breaker = CircuitBreaker(name="telephony_twilio", fail_max=5, reset_timeout=30.0)
