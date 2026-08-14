import functools
import inspect
import structlog
from typing import Callable, Any, Optional

from app.core.observability.tracing import (
    trace_span, trace_agent, trace_workflow, trace_tool, trace_rag, trace_hitl
)
from app.core.observability.privacy import sanitize_error_message

logger = structlog.get_logger(__name__)


def traceable_agent(
    agent_name_fn_or_str: Any = None,
    agent_id_param: Optional[str] = None,
    agent_name: Optional[str] = None,
    name: Optional[str] = None
) -> Callable:
    """
    Decorator for AI Agent functions or methods.
    Automatically captures input args, output result, agent metadata, and errors safely.
    """
    effective_name = agent_name or name
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            resolved_agent_name = (
                effective_name if effective_name
                else (agent_name_fn_or_str if isinstance(agent_name_fn_or_str, str) else func.__name__)
            )
            agent_id = kwargs.get(agent_id_param) if agent_id_param else None

            # Extract inputs safely
            inputs = {
                k: str(v) for k, v in kwargs.items() 
                if not k.startswith("_") and k not in ("db", "session")
            }

            async with trace_agent(
                agent_name=resolved_agent_name, 
                agent_id=agent_id, 
                inputs=inputs
            ) as span:
                try:
                    result = await func(*args, **kwargs)
                    span.end(outputs={"result": result})
                    return result
                except Exception as exc:
                    span.end(error=exc)
                    raise

        return wrapper

    if callable(agent_name_fn_or_str):
        f = agent_name_fn_or_str
        agent_name_fn_or_str = None
        return decorator(f)
    return decorator


def traceable_workflow(workflow_name: Optional[str] = None) -> Callable:
    """
    Decorator for workflow/LangGraph execution handlers.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            w_name = workflow_name or func.__name__
            inputs = {
                k: str(v) for k, v in kwargs.items() 
                if not k.startswith("_") and k not in ("db", "session")
            }

            async with trace_workflow(workflow_name=w_name, inputs=inputs) as span:
                try:
                    result = await func(*args, **kwargs)
                    span.end(outputs={"result": result})
                    return result
                except Exception as exc:
                    span.end(error=exc)
                    raise

        return wrapper
    return decorator


def traceable_tool(
    tool_name: Optional[str] = None,
    risk_level: str = "Low",
    hitl_required: bool = False
) -> Callable:
    """
    Decorator for tool execution implementations.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            t_name = tool_name or func.__name__
            inputs = {
                k: str(v) for k, v in kwargs.items() 
                if not k.startswith("_") and k not in ("db", "session")
            }

            async with trace_tool(
                tool_name=t_name, 
                inputs=inputs, 
                risk_level=risk_level, 
                hitl_required=hitl_required
            ) as span:
                try:
                    result = await func(*args, **kwargs)
                    span.end(outputs={"result": result})
                    return result
                except Exception as exc:
                    span.end(error=exc)
                    raise

        return wrapper
    return decorator


def traceable_rag(strategy: str = "pgvector_hybrid") -> Callable:
    """
    Decorator for RAG knowledge retrieval calls.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            query = str(kwargs.get("query") or (args[0] if args else ""))

            async with trace_rag(query=query, retrieval_strategy=strategy) as span:
                try:
                    result = await func(*args, **kwargs)
                    span.end(outputs={"retrieved_count": len(getattr(result, "documents", [])) if hasattr(result, "documents") else 0})
                    return result
                except Exception as exc:
                    span.end(error=exc)
                    raise

        return wrapper
    return decorator
