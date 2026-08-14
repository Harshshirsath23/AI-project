from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.core.observability.context import get_current_trace_context, TraceContext


def build_trace_metadata(
    extra_metadata: Optional[Dict[str, Any]] = None,
    context: Optional[TraceContext] = None
) -> Dict[str, Any]:
    """
    Construct standardized metadata for a LangSmith run/span.
    Includes tenant isolation ID, agent, workflow, model, and system environment info.
    """
    ctx = context or get_current_trace_context()
    
    metadata: Dict[str, Any] = {
        "platform": settings.PROJECT_NAME,
        "platform_version": settings.VERSION,
        "environment": settings.LANGSMITH_ENVIRONMENT,
    }

    if ctx.organization_id:
        metadata["organization_id"] = ctx.organization_id
    if ctx.user_id:
        metadata["user_id"] = ctx.user_id
    if ctx.agent_id:
        metadata["agent_id"] = ctx.agent_id
    if ctx.agent_version is not None:
        metadata["agent_version"] = ctx.agent_version
    if ctx.workflow_id:
        metadata["workflow_id"] = ctx.workflow_id
    if ctx.workflow_version is not None:
        metadata["workflow_version"] = ctx.workflow_version
    if ctx.execution_id:
        metadata["execution_id"] = ctx.execution_id
    if ctx.hitl_id:
        metadata["hitl_id"] = ctx.hitl_id
    if ctx.feature_name:
        metadata["feature_name"] = ctx.feature_name
    if ctx.request_type:
        metadata["request_type"] = ctx.request_type

    if ctx.custom_metadata:
        metadata.update(ctx.custom_metadata)

    if extra_metadata:
        metadata.update(extra_metadata)

    return metadata


def build_trace_tags(
    extra_tags: Optional[List[str]] = None,
    context: Optional[TraceContext] = None
) -> List[str]:
    """
    Construct standardized tags for filtering and grouping runs in LangSmith.
    """
    ctx = context or get_current_trace_context()
    tags: List[str] = [f"env:{settings.LANGSMITH_ENVIRONMENT}"]

    if ctx.organization_id:
        tags.append(f"org:{ctx.organization_id}")
    if ctx.agent_id:
        tags.append(f"agent:{ctx.agent_id}")
    if ctx.workflow_id:
        tags.append(f"workflow:{ctx.workflow_id}")
    if ctx.feature_name:
        tags.append(f"feature:{ctx.feature_name}")

    if extra_tags:
        for t in extra_tags:
            if t not in tags:
                tags.append(t)

    return tags
