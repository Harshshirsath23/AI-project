import time
import structlog
import uuid
from typing import Any, Dict, List, Optional, Callable, AsyncGenerator
from contextlib import asynccontextmanager

from langsmith.run_trees import RunTree

from app.core.config import settings
from app.core.observability.langsmith import get_langsmith_client
from app.core.observability.context import get_current_trace_context, update_trace_context, TraceContext
from app.core.observability.metadata import build_trace_metadata, build_trace_tags
from app.core.observability.privacy import sanitize_payload, sanitize_error_message

logger = structlog.get_logger(__name__)


class TraceSpan:
    """Wrapper around LangSmith RunTree for hierarchical tracing."""

    def __init__(
        self,
        name: str,
        run_type: str = "chain",
        inputs: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        parent_span: Optional["TraceSpan"] = None
    ):
        self.name = name
        self.run_type = run_type
        self.inputs = sanitize_payload(
            inputs or {}, 
            capture_content=settings.LANGSMITH_CAPTURE_INPUTS
        )
        self.metadata = build_trace_metadata(metadata)
        self.tags = build_trace_tags(tags)
        self.parent_span = parent_span
        self.run_tree: Optional[RunTree] = None
        self.start_time = time.time()
        try:
            self._init_run_tree()
        except Exception as exc:
            logger.warning("TraceSpan initialization suppressed telemetry failure", span_name=self.name, error=str(exc))
            self.run_tree = None

    def _init_run_tree(self) -> None:
        client = get_langsmith_client()
        if not client:
            return

        try:
            parent_rt = self.parent_span.run_tree if self.parent_span else None
            
            # Get current trace context for correlation
            ctx = get_current_trace_context()
            
            # Enhance metadata with execution correlation
            enhanced_metadata = self.metadata.copy()
            if ctx.execution_id:
                enhanced_metadata["execution_id"] = str(ctx.execution_id)
            if ctx.organization_id:
                enhanced_metadata["organization_id"] = str(ctx.organization_id)
            if ctx.agent_id:
                enhanced_metadata["agent_id"] = str(ctx.agent_id)
            if ctx.workflow_id:
                enhanced_metadata["workflow_id"] = str(ctx.workflow_id)
            
            self.run_tree = RunTree(
                name=self.name,
                run_type=self.run_type,
                inputs=self.inputs if isinstance(self.inputs, dict) else {"input": self.inputs},
                metadata=enhanced_metadata,
                tags=self.tags,
                project_name=settings.LANGSMITH_PROJECT,
                client=client,
                id=self.run_id,
                parent_run=parent_rt
            )
            self.run_tree.post()
            
            # Update trace context with trace_id / parent_run_id
            update_trace_context(
                trace_id=str(self.run_tree.id),
                parent_run_id=str(self.run_tree.id)
            )
        except Exception as exc:
            logger.warning("Failed to post run to LangSmith", span_name=self.name, error=str(exc))
            self.run_tree = None

    def end(
        self, 
        outputs: Optional[Dict[str, Any]] = None, 
        error: Optional[Exception | str] = None,
        extra_metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """End span and post telemetry to LangSmith asynchronously."""
        if not self.run_tree:
            return

        try:
            end_time = time.time()
            latency_ms = int((end_time - self.start_time) * 1000)
            
            if extra_metadata:
                self.run_tree.metadata.update(extra_metadata)
            
            self.run_tree.metadata["latency_ms"] = latency_ms

            if error:
                error_msg = sanitize_error_message(error)
                self.run_tree.end(
                    outputs=None,
                    error=error_msg
                )
            else:
                sanitized_outputs = sanitize_payload(
                    outputs or {}, 
                    capture_content=settings.LANGSMITH_CAPTURE_OUTPUTS
                )
                self.run_tree.end(
                    outputs=sanitized_outputs if isinstance(sanitized_outputs, dict) else {"output": sanitized_outputs}
                )

            # Post update non-blockingly
            self.run_tree.patch()
        except Exception as exc:
            logger.warning("Failed to patch run in LangSmith", span_name=self.name, error=str(exc))


@asynccontextmanager
async def trace_span(
    name: str,
    run_type: str = "chain",
    inputs: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    tags: Optional[List[str]] = None,
    parent_span: Optional[TraceSpan] = None
) -> AsyncGenerator[TraceSpan, None]:
    """
    Async context manager for tracing execution blocks.
    Guarantees that telemetry failure will NEVER break application execution.
    """
    span = TraceSpan(
        name=name,
        run_type=run_type,
        inputs=inputs,
        metadata=metadata,
        tags=tags,
        parent_span=parent_span
    )
    try:
        yield span
    except Exception as exc:
        span.end(error=exc)
        raise
    else:
        # Caller will call span.end(...) if they wish to supply output, otherwise auto-ended
        pass


@asynccontextmanager
async def trace_agent(
    agent_name: str,
    agent_id: Optional[str] = None,
    agent_version: Optional[int] = None,
    inputs: Optional[Dict[str, Any]] = None
) -> AsyncGenerator[TraceSpan, None]:
    """Trace AI Agent execution block."""
    meta = {}
    if agent_id:
        meta["agent_id"] = str(agent_id)
    if agent_version is not None:
        meta["agent_version"] = agent_version

    update_trace_context(agent_id=agent_id, agent_version=agent_version)

    async with trace_span(
        name=f"Agent: {agent_name}",
        run_type="agent",
        inputs=inputs,
        metadata=meta,
        tags=["component:agent", f"agent_name:{agent_name}"]
    ) as span:
        yield span


@asynccontextmanager
async def trace_workflow(
    workflow_name: str,
    workflow_id: Optional[str] = None,
    workflow_version: Optional[int] = None,
    inputs: Optional[Dict[str, Any]] = None
) -> AsyncGenerator[TraceSpan, None]:
    """Trace LangGraph/AI Workflow execution block."""
    meta = {}
    if workflow_id:
        meta["workflow_id"] = str(workflow_id)
    if workflow_version is not None:
        meta["workflow_version"] = workflow_version

    update_trace_context(workflow_id=workflow_id, workflow_version=workflow_version)

    async with trace_span(
        name=f"Workflow: {workflow_name}",
        run_type="chain",
        inputs=inputs,
        metadata=meta,
        tags=["component:workflow", f"workflow_name:{workflow_name}"]
    ) as span:
        yield span


@asynccontextmanager
async def trace_tool(
    tool_name: str,
    inputs: Optional[Dict[str, Any]] = None,
    risk_level: Optional[str] = None,
    required_permissions: Optional[List[str]] = None,
    hitl_required: bool = False
) -> AsyncGenerator[TraceSpan, None]:
    """Trace AI Tool invocation."""
    meta: Dict[str, Any] = {
        "tool_name": tool_name,
        "risk_level": risk_level,
        "hitl_required": hitl_required,
    }
    if required_permissions:
        meta["required_permissions"] = required_permissions

    async with trace_span(
        name=f"Tool: {tool_name}",
        run_type="tool",
        inputs=inputs,
        metadata=meta,
        tags=["component:tool", f"tool:{tool_name}"]
    ) as span:
        yield span


@asynccontextmanager
async def trace_rag(
    query: str,
    retrieval_strategy: str = "pgvector_hybrid",
    top_k: int = 5
) -> AsyncGenerator[TraceSpan, None]:
    """Trace RAG Retrieval step."""
    inputs = {
        "query": query,
        "retrieval_strategy": retrieval_strategy,
        "top_k": top_k
    }

    async with trace_span(
        name="RAG: Document Retrieval",
        run_type="retriever",
        inputs=inputs,
        metadata={"retrieval_strategy": retrieval_strategy, "top_k": top_k},
        tags=["component:rag", f"strategy:{retrieval_strategy}"]
    ) as span:
        yield span


@asynccontextmanager
async def trace_hitl(
    execution_id: str,
    agent_id: str,
    hitl_reason: str,
    risk_level: str
) -> AsyncGenerator[TraceSpan, None]:
    """Trace Human-in-the-Loop Interruption Event."""
    inputs = {
        "execution_id": str(execution_id),
        "agent_id": str(agent_id),
        "hitl_reason": hitl_reason,
        "risk_level": risk_level,
        "status": "WAITING_HITL"
    }

    meta = {
        "hitl_required": True,
        "hitl_triggered": True,
        "hitl_reason": hitl_reason,
        "risk_level": risk_level
    }

    async with trace_span(
        name="HITL: Human Intervention Requested",
        run_type="chain",
        inputs=inputs,
        metadata=meta,
        tags=["component:hitl", "event:wait_human"]
    ) as span:
        yield span
