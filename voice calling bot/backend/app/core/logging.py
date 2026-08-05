import logging
import sys
from typing import Any

import structlog
from structlog.types import Processor

from app.config.settings import get_settings


def configure_logging() -> None:
    """Configure structured logging for the application."""
    settings = get_settings()

    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    # Configure structlog
    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
    ]

    if settings.log_format == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> Any:
    """Get a structured logger instance."""
    return structlog.get_logger(name)
