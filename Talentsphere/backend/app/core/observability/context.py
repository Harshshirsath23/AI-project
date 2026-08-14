from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import uuid


@dataclass
class TraceContext:
    """Holds active AI execution context for LangSmith tracing."""
    organization_id: Optional[str] = None
    user_id: Optional[str] = None
    agent_id: Optional[str] = None
    agent_version: Optional[int] = None
    workflow_id: Optional[str] = None
    workflow_version: Optional[int] = None
    execution_id: Optional[str] = None
    hitl_id: Optional[str] = None
    parent_run_id: Optional[str] = None
    trace_id: Optional[str] = None
    feature_name: Optional[str] = None
    request_type: Optional[str] = None
    custom_metadata: Dict[str, Any] = field(default_factory=dict)


_trace_context: ContextVar[Optional[TraceContext]] = ContextVar("trace_context", default=None)


def get_current_trace_context() -> TraceContext:
    """Retrieve the current async trace context, initializing one if missing."""
    ctx = _trace_context.get()
    if ctx is None:
        ctx = TraceContext()
        _trace_context.set(ctx)
    return ctx


def set_current_trace_context(context: TraceContext) -> None:
    """Set the active trace context for the current async task."""
    _trace_context.set(context)


def update_trace_context(
    organization_id: Optional[str | uuid.UUID] = None,
    user_id: Optional[str | uuid.UUID] = None,
    agent_id: Optional[str | uuid.UUID] = None,
    agent_version: Optional[int] = None,
    workflow_id: Optional[str | uuid.UUID] = None,
    workflow_version: Optional[int] = None,
    execution_id: Optional[str | uuid.UUID] = None,
    hitl_id: Optional[str | uuid.UUID] = None,
    parent_run_id: Optional[str] = None,
    trace_id: Optional[str] = None,
    feature_name: Optional[str] = None,
    request_type: Optional[str] = None,
    **kwargs: Any
) -> TraceContext:
    """Update fields in the active trace context and return updated context."""
    ctx = get_current_trace_context()
    
    if organization_id is not None:
        ctx.organization_id = str(organization_id)
    if user_id is not None:
        ctx.user_id = str(user_id)
    if agent_id is not None:
        ctx.agent_id = str(agent_id)
    if agent_version is not None:
        ctx.agent_version = agent_version
    if workflow_id is not None:
        ctx.workflow_id = str(workflow_id)
    if workflow_version is not None:
        ctx.workflow_version = workflow_version
    if execution_id is not None:
        ctx.execution_id = str(execution_id)
    if hitl_id is not None:
        ctx.hitl_id = str(hitl_id)
    if parent_run_id is not None:
        ctx.parent_run_id = parent_run_id
    if trace_id is not None:
        ctx.trace_id = trace_id
    if feature_name is not None:
        ctx.feature_name = feature_name
    if request_type is not None:
        ctx.request_type = request_type
        
    if kwargs:
        ctx.custom_metadata.update(kwargs)

    return ctx


def clear_trace_context() -> None:
    """Reset the current trace context."""
    _trace_context.set(None)
