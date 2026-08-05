import time
from contextlib import asynccontextmanager
from typing import Optional
from dataclasses import dataclass, field

from app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class AIMetrics:
    """Metrics for AI provider operations."""

    operation_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    total_duration: float = 0.0
    total_tokens: int = 0
    retry_count: int = 0


class AIObservability:
    """
    Observability layer for AI provider operations.
    
    This class provides structured logging and metrics collection for
    all AI operations. It tracks execution duration, success/failure rates,
    and other important metrics for monitoring and debugging.
    """

    def __init__(self):
        """Initialize the AI observability layer."""
        self._metrics: dict[str, AIMetrics] = {}

    def get_metrics(self, operation: str) -> AIMetrics:
        """
        Get metrics for a specific operation.
        
        Args:
            operation: Operation name (e.g., "stt_transcribe", "llm_chat")
        
        Returns:
            AIMetrics for the operation
        """
        if operation not in self._metrics:
            self._metrics[operation] = AIMetrics()
        return self._metrics[operation]

    def record_success(
        self,
        operation: str,
        provider: str,
        duration: float,
        tokens: int = 0,
        metadata: Optional[dict] = None,
    ) -> None:
        """
        Record a successful AI operation.
        
        Args:
            operation: Operation name
            provider: Provider name
            duration: Operation duration in seconds
            tokens: Number of tokens used (if applicable)
            metadata: Optional additional metadata
        """
        metrics = self.get_metrics(operation)
        metrics.operation_count += 1
        metrics.success_count += 1
        metrics.total_duration += duration
        metrics.total_tokens += tokens

        logger.info(
            "AI operation succeeded",
            operation=operation,
            provider=provider,
            duration=duration,
            tokens=tokens,
            metadata=metadata,
        )

    def record_failure(
        self,
        operation: str,
        provider: str,
        duration: float,
        error: str,
        error_type: str,
        metadata: Optional[dict] = None,
    ) -> None:
        """
        Record a failed AI operation.
        
        Args:
            operation: Operation name
            provider: Provider name
            duration: Operation duration in seconds
            error: Error message
            error_type: Type of error
            metadata: Optional additional metadata
        """
        metrics = self.get_metrics(operation)
        metrics.operation_count += 1
        metrics.failure_count += 1
        metrics.total_duration += duration

        logger.error(
            "AI operation failed",
            operation=operation,
            provider=provider,
            duration=duration,
            error=error,
            error_type=error_type,
            metadata=metadata,
        )

    def record_retry(
        self,
        operation: str,
        provider: str,
        attempt: int,
        max_attempts: int,
    ) -> None:
        """
        Record a retry attempt.
        
        Args:
            operation: Operation name
            provider: Provider name
            attempt: Current attempt number
            max_attempts: Maximum number of attempts
        """
        metrics = self.get_metrics(operation)
        metrics.retry_count += 1

        logger.warning(
            "AI operation retry",
            operation=operation,
            provider=provider,
            attempt=attempt,
            max_attempts=max_attempts,
        )

    def log_provider_selection(
        self,
        operation: str,
        provider: str,
        provider_id: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> None:
        """
        Log provider selection.
        
        Args:
            operation: Operation name
            provider: Provider name
            provider_id: Provider ID (if different from name)
            reason: Reason for selection (e.g., "default", "override")
        """
        logger.info(
            "Provider selected",
            operation=operation,
            provider=provider,
            provider_id=provider_id,
            reason=reason,
        )

    def log_streaming_start(
        self,
        operation: str,
        provider: str,
    ) -> None:
        """
        Log the start of a streaming operation.
        
        Args:
            operation: Operation name
            provider: Provider name
        """
        logger.info(
            "Streaming operation started",
            operation=operation,
            provider=provider,
        )

    def log_streaming_chunk(
        self,
        operation: str,
        provider: str,
        chunk_index: int,
        chunk_size: int,
    ) -> None:
        """
        Log a streaming chunk.
        
        Args:
            operation: Operation name
            provider: Provider name
            chunk_index: Chunk index
            chunk_size: Size of the chunk
        """
        logger.debug(
            "Streaming chunk received",
            operation=operation,
            provider=provider,
            chunk_index=chunk_index,
            chunk_size=chunk_size,
        )

    def log_streaming_end(
        self,
        operation: str,
        provider: str,
        total_chunks: int,
        duration: float,
    ) -> None:
        """
        Log the end of a streaming operation.
        
        Args:
            operation: Operation name
            provider: Provider name
            total_chunks: Total number of chunks received
            duration: Total duration in seconds
        """
        logger.info(
            "Streaming operation completed",
            operation=operation,
            provider=provider,
            total_chunks=total_chunks,
            duration=duration,
        )

    def log_streaming_error(
        self,
        operation: str,
        provider: str,
        error: str,
        chunks_received: int,
    ) -> None:
        """
        Log a streaming error.
        
        Args:
            operation: Operation name
            provider: Provider name
            error: Error message
            chunks_received: Number of chunks received before error
        """
        logger.error(
            "Streaming operation failed",
            operation=operation,
            provider=provider,
            error=error,
            chunks_received=chunks_received,
        )

    def get_all_metrics(self) -> dict[str, AIMetrics]:
        """
        Get all metrics.
        
        Returns:
            Dictionary of operation names to metrics
        """
        return self._metrics.copy()

    def reset_metrics(self, operation: Optional[str] = None) -> None:
        """
        Reset metrics.
        
        Args:
            operation: Optional operation to reset. If None, resets all.
        """
        if operation:
            if operation in self._metrics:
                self._metrics[operation] = AIMetrics()
        else:
            self._metrics.clear()


@asynccontextmanager
async def observe_ai_operation(
    observability: AIObservability,
    operation: str,
    provider: str,
    metadata: Optional[dict] = None,
):
    """
    Context manager for observing AI operations.
    
    This context manager automatically records success/failure and duration.
    
    Args:
        observability: AIObservability instance
        operation: Operation name
        provider: Provider name
        metadata: Optional metadata to include
    
    Yields:
        None
    
    Example:
        async with observe_ai_operation(obs, "stt_transcribe", "faster_whisper"):
            result = await provider.transcribe(request)
    """
    start_time = time.time()
    try:
        yield
        duration = time.time() - start_time
        observability.record_success(
            operation=operation,
            provider=provider,
            duration=duration,
            metadata=metadata,
        )
    except Exception as e:
        duration = time.time() - start_time
        observability.record_failure(
            operation=operation,
            provider=provider,
            duration=duration,
            error=str(e),
            error_type=type(e).__name__,
            metadata=metadata,
        )
        raise


# Global observability instance
_observability = AIObservability()


def get_observability() -> AIObservability:
    """
    Get the global observability instance.
    
    Returns:
        AIObservability: The global observability instance
    """
    return _observability
