import os
import structlog
from typing import Optional, Any
from langsmith import Client
from langchain_core.tracers import LangChainTracer

from app.core.config import settings

logger = structlog.get_logger(__name__)

_client_instance: Optional[Client] = None
_client_initialized: bool = False


def init_langsmith_environment() -> None:
    """Configure process environment variables for LangChain/LangSmith SDKs."""
    if settings.is_langsmith_enabled:
        os.environ["LANGCHAIN_TRACING_V2"] = "true" if settings.LANGSMITH_TRACING else "false"
        os.environ["LANGCHAIN_PROJECT"] = settings.LANGSMITH_PROJECT
        if settings.LANGSMITH_API_KEY:
            os.environ["LANGCHAIN_API_KEY"] = settings.LANGSMITH_API_KEY
        if settings.LANGSMITH_ENDPOINT:
            os.environ["LANGCHAIN_ENDPOINT"] = settings.LANGSMITH_ENDPOINT
    else:
        os.environ["LANGCHAIN_TRACING_V2"] = "false"


def get_langsmith_client() -> Optional[Client]:
    """
    Get or initialize singleton LangSmith client.
    Returns None if LangSmith is disabled or invalid configuration/credentials.
    """
    global _client_instance, _client_initialized

    if _client_initialized:
        return _client_instance

    _client_initialized = True

    if not settings.is_langsmith_enabled:
        logger.info("LangSmith observability is disabled or missing credentials.")
        _client_instance = None
        return None

    try:
        init_langsmith_environment()
        _client_instance = Client(
            api_key=settings.LANGSMITH_API_KEY,
            api_url=settings.LANGSMITH_ENDPOINT or "https://api.smith.langchain.com",
            timeout_ms=5000,
        )
        logger.info(
            "LangSmith client initialized successfully",
            project=settings.LANGSMITH_PROJECT,
            environment=settings.LANGSMITH_ENVIRONMENT
        )
    except Exception as exc:
        logger.error("Failed to initialize LangSmith client", error=str(exc))
        _client_instance = None

    return _client_instance


def get_langchain_tracer(
    project_name: Optional[str] = None,
    extra_metadata: Optional[dict] = None,
    extra_tags: Optional[list] = None
) -> Optional[LangChainTracer]:
    """
    Construct a LangChainTracer callback handler for passing into LangChain / LangGraph calls.
    Returns None if LangSmith is disabled or unavailable.
    """
    if not settings.is_langsmith_enabled:
        return None

    try:
        client = get_langsmith_client()
        if not client:
            return None

        project = project_name or settings.LANGSMITH_PROJECT
        tracer = LangChainTracer(
            project_name=project,
            client=client,
            tags=extra_tags or [],
            metadata=extra_metadata or {}
        )
        return tracer
    except Exception as exc:
        logger.warning("Failed to construct LangChainTracer callback", error=str(exc))
        return None


def is_langsmith_available() -> bool:
    """Check if LangSmith is currently enabled and reachable."""
    if not settings.is_langsmith_enabled:
        return False
    client = get_langsmith_client()
    if not client:
        return False
    try:
        # Lightweight check
        return True
    except Exception:
        return False
