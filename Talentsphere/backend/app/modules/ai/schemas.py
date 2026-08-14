from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

from app.modules.ai.enums import (
    AgentStatus, AgentType, ExecutionStatus, ToolRisk,
    HITLRequirement, PromptStatus, DocumentType, EmbeddingStatus,
    WorkflowStatus, HITLDecision, GuardrailType, ModelProvider
)


# ==================== Agent Schemas ====================

class AIAgentCreate(BaseModel):
    agent_name: str = Field(..., description="Agent name")
    agent_type: str = Field(..., description="Agent type")
    description: Optional[str] = Field(None, description="Agent description")
    model_provider: str = Field(..., description="Model provider")
    model_name: str = Field(..., description="Model name")
    allowed_tools: Optional[List[str]] = Field(None, description="Allowed tools")
    required_permissions: Optional[List[str]] = Field(None, description="Required permissions")
    config_data: Optional[Dict[str, Any]] = Field(None, description="Agent configuration")
    is_global: bool = Field(default=False, description="Whether agent is global")

class AIAgentResponse(BaseModel):
    id: uuid.UUID
    organization_id: Optional[uuid.UUID]
    agent_name: str
    agent_type: str
    description: Optional[str]
    current_version: int
    status: str
    model_provider: str
    model_name: str
    allowed_tools: Optional[List[str]]
    required_permissions: Optional[List[str]]
    config_data: Optional[Dict[str, Any]]
    is_global: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AIAgentVersionCreate(BaseModel):
    version: int = Field(..., description="Version number")
    system_prompt: str = Field(..., description="System prompt")
    configuration: Optional[Dict[str, Any]] = Field(None, description="Configuration")
    model_name: str = Field(..., description="Model name")
    changelog: Optional[str] = Field(None, description="Version changelog")


# ==================== Tool Schemas ====================

class AIToolCreate(BaseModel):
    tool_name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    tool_path: str = Field(..., description="Python module path")
    required_permissions: Optional[List[str]] = Field(None, description="Required permissions")
    hitl_requirement: str = Field(default="Not_Required", description="HITL requirement")
    risk_level: str = Field(default="Low", description="Risk level")
    input_schema: Optional[Dict[str, Any]] = Field(None, description="Input schema")
    output_schema: Optional[Dict[str, Any]] = Field(None, description="Output schema")

class AIToolResponse(BaseModel):
    id: uuid.UUID
    tool_name: str
    description: str
    tool_path: str
    required_permissions: Optional[List[str]]
    hitl_requirement: str
    risk_level: str
    input_schema: Optional[Dict[str, Any]]
    output_schema: Optional[Dict[str, Any]]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Knowledge Schemas ====================

class KnowledgeDocumentCreate(BaseModel):
    document_type: str = Field(..., description="Document type")
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Document content")
    source_url: Optional[str] = Field(None, description="Source URL")
    meta_data: Optional[Dict[str, Any]] = Field(None, description="Document metadata")
    tags: Optional[List[str]] = Field(None, description="Document tags")
    is_public: bool = Field(default=False, description="Whether document is public")

class KnowledgeDocumentResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    document_type: str
    title: str
    content: str
    source_url: Optional[str]
    meta_data: Optional[Dict[str, Any]]
    tags: Optional[List[str]]
    embedding_status: str
    chunk_count: int
    is_public: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RetrievalRequest(BaseModel):
    query: str = Field(..., description="Search query")
    top_k: int = Field(default=5, description="Number of results")
    document_type: Optional[str] = Field(None, description="Filter by document type")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")


class RetrievalResponse(BaseModel):
    documents: List[Dict[str, Any]]
    scores: List[float]
    total_count: int


# ==================== Execution Schemas ====================

class AIExecutionCreate(BaseModel):
    agent_id: uuid.UUID = Field(..., description="Agent ID")
    workflow_id: Optional[uuid.UUID] = Field(None, description="Workflow ID")
    input_data: Dict[str, Any] = Field(..., description="Input data")

class AIExecutionResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    agent_id: uuid.UUID
    agent_version: int
    workflow_id: Optional[uuid.UUID]
    execution_id: str
    status: str
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]]
    error_message: Optional[str]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    model_provider: str
    model_name: str
    tokens_in: Optional[int]
    tokens_out: Optional[int]
    total_tokens: Optional[int]
    latency_ms: Optional[int]
    estimated_cost: Optional[float]
    human_intervention: bool
    hitl_count: int
    langsmith_trace_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== HITL Schemas ====================

class HITLRequest(BaseModel):
    execution_id: uuid.UUID = Field(..., description="Execution ID")
    request_data: Dict[str, Any] = Field(..., description="Request data")
    timeout_minutes: int = Field(default=60, description="Timeout in minutes")

class HITLResponse(BaseModel):
    decision: str = Field(..., description="Decision")
    decision_reason: Optional[str] = Field(None, description="Decision reason")
    modified_data: Optional[Dict[str, Any]] = Field(None, description="Modified data")


# ==================== Workflow Schemas ====================

class AIWorkflowCreate(BaseModel):
    workflow_name: str = Field(..., description="Workflow name")
    workflow_type: str = Field(..., description="Workflow type")
    description: Optional[str] = Field(None, description="Workflow description")
    definition: Dict[str, Any] = Field(..., description="Workflow definition")
    is_default: bool = Field(default=False, description="Whether this is default workflow")

class AIWorkflowResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    workflow_name: str
    workflow_type: str
    description: Optional[str]
    definition: Dict[str, Any]
    status: str
    version: int
    is_default: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Prompt Template Schemas ====================

class PromptTemplateCreate(BaseModel):
    template_name: str = Field(..., description="Template name")
    template_type: str = Field(..., description="Template type")
    system_prompt: str = Field(..., description="System prompt")
    variables: Optional[Dict[str, Any]] = Field(None, description="Variable schema")
    is_default: bool = Field(default=False, description="Whether this is default template")

class PromptTemplateResponse(BaseModel):
    id: uuid.UUID
    organization_id: Optional[uuid.UUID]
    template_name: str
    template_type: str
    system_prompt: str
    variables: Optional[Dict[str, Any]]
    status: str
    version: int
    is_default: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Usage Schemas ====================

class UsageStatsResponse(BaseModel):
    execution_count: int
    total_tokens: int
    total_cost: float
    avg_latency_ms: float
    by_agent: Dict[str, int]


# ==================== Agentic Output Schemas ====================

class CandidateMatchRecommendation(BaseModel):
    decision: str = Field(..., description="MATCH, NO_MATCH, or MAYBE")
    confidence: float = Field(..., description="Confidence score between 0.0 and 1.0")
    reasoning_summary: str = Field(..., description="Summary of reasoning")
    matching_skills: List[str] = Field(default_factory=list, description="List of matching skills")
    missing_skills: List[str] = Field(default_factory=list, description="List of missing skills")
    recommended_action: str = Field(..., description="MOVE_TO_SCREENING, REJECT, or REQUEST_MORE_INFO")
    evidence: List[str] = Field(default_factory=list, description="Supporting evidence bullet points")


class ExecutionRunRequest(BaseModel):
    agent_id: uuid.UUID = Field(..., description="Registered Agent UUID")
    workflow_id: Optional[uuid.UUID] = Field(None, description="Optional Workflow UUID")
    input_data: Dict[str, Any] = Field(..., description="Agent execution input payload")


class ExecutionResumeRequest(BaseModel):
    decision: str = Field(..., description="Approved, Rejected, or Modified")
    decision_reason: Optional[str] = Field(None, description="Reason for decision")
    modified_data: Optional[Dict[str, Any]] = Field(None, description="Optional modified payload")
    by_model: Dict[str, int]