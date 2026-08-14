"""
TalentSphere AI Observability, Tracing, Debugging, and Evaluation Layer (LangSmith Integration)
"""

from app.core.observability.langsmith import (
    get_langsmith_client,
    get_langchain_tracer,
    is_langsmith_available
)
from app.core.observability.context import (
    TraceContext,
    get_current_trace_context,
    set_current_trace_context,
    update_trace_context,
    clear_trace_context
)
from app.core.observability.privacy import (
    sanitize_payload,
    sanitize_string,
    sanitize_error_message
)
from app.core.observability.metadata import (
    build_trace_metadata,
    build_trace_tags
)
from app.core.observability.tracing import (
    TraceSpan,
    trace_span,
    trace_agent,
    trace_workflow,
    trace_tool,
    trace_rag,
    trace_hitl
)
from app.core.observability.decorators import (
    traceable_agent,
    traceable_workflow,
    traceable_tool,
    traceable_rag
)
from app.core.observability.evaluation import (
    EvaluationMetric,
    EvaluationScore,
    EvaluationManager
)

__all__ = [
    "get_langsmith_client",
    "get_langchain_tracer",
    "is_langsmith_available",
    "TraceContext",
    "get_current_trace_context",
    "set_current_trace_context",
    "update_trace_context",
    "clear_trace_context",
    "sanitize_payload",
    "sanitize_string",
    "sanitize_error_message",
    "build_trace_metadata",
    "build_trace_tags",
    "TraceSpan",
    "trace_span",
    "trace_agent",
    "trace_workflow",
    "trace_tool",
    "trace_rag",
    "trace_hitl",
    "traceable_agent",
    "traceable_workflow",
    "traceable_tool",
    "traceable_rag",
    "EvaluationMetric",
    "EvaluationScore",
    "EvaluationManager"
]
