from typing import TypedDict, Dict, Any, List, Optional, Annotated
import operator
from pydantic import BaseModel, Field
import uuid


class AgentExecutionStateDict(TypedDict, total=False):
    """LangGraph TypedDict state representation."""
    execution_id: str
    organization_id: str
    user_id: str
    agent_id: str
    agent_version: int
    workflow_id: Optional[str]
    request: Dict[str, Any]
    context: Dict[str, Any]
    messages: Annotated[List[Dict[str, Any]], operator.add]
    tool_calls: Annotated[List[Dict[str, Any]], operator.add]
    tool_results: Annotated[List[Dict[str, Any]], operator.add]
    intermediate_results: Dict[str, Any]
    validation_results: Dict[str, Any]
    hitl_request: Optional[Dict[str, Any]]
    human_decision: Optional[Dict[str, Any]]
    final_output: Optional[Dict[str, Any]]
    errors: Annotated[List[str], operator.add]
    status: str
    metadata: Dict[str, Any]


class AgentExecutionStateModel(BaseModel):
    """Pydantic model representation for AgentExecutionState validation and serialization."""
    execution_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: str
    user_id: str
    agent_id: str
    agent_version: int = 1
    workflow_id: Optional[str] = None
    request: Dict[str, Any] = Field(default_factory=dict)
    context: Dict[str, Any] = Field(default_factory=dict)
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    tool_results: List[Dict[str, Any]] = Field(default_factory=list)
    intermediate_results: Dict[str, Any] = Field(default_factory=dict)
    validation_results: Dict[str, Any] = Field(default_factory=dict)
    hitl_request: Optional[Dict[str, Any]] = None
    human_decision: Optional[Dict[str, Any]] = None
    final_output: Optional[Dict[str, Any]] = None
    errors: List[str] = Field(default_factory=list)
    status: str = "QUEUED"
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize state to standard dictionary."""
        return self.model_dump()


def create_initial_agent_state(
    organization_id: str | uuid.UUID,
    user_id: str | uuid.UUID,
    agent_id: str | uuid.UUID,
    agent_version: int = 1,
    workflow_id: Optional[str | uuid.UUID] = None,
    request_data: Optional[Dict[str, Any]] = None,
    context_data: Optional[Dict[str, Any]] = None,
    execution_id: Optional[str | uuid.UUID] = None
) -> AgentExecutionStateDict:
    """Construct a clean, initial AgentExecutionState dict for graph execution."""
    return AgentExecutionStateDict(
        execution_id=str(execution_id or uuid.uuid4()),
        organization_id=str(organization_id),
        user_id=str(user_id),
        agent_id=str(agent_id),
        agent_version=agent_version,
        workflow_id=str(workflow_id) if workflow_id else None,
        request=request_data or {},
        context=context_data or {},
        messages=[],
        tool_calls=[],
        tool_results=[],
        intermediate_results={},
        validation_results={},
        hitl_request=None,
        human_decision=None,
        final_output=None,
        errors=[],
        status="QUEUED",
        metadata={}
    )
