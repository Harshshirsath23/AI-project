from sqlalchemy import Column, String, Integer, ForeignKey, Date, Float, TEXT, Boolean, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
from datetime import datetime
from app.core.models import Base, AuditMixin

from app.modules.ai.enums import (
    AgentStatus, AgentType, ExecutionStatus, ToolRisk,
    HITLRequirement, PromptStatus, DocumentType, EmbeddingStatus,
    WorkflowStatus, HITLDecision, GuardrailType, ModelProvider
)


# ==================== AI Agent Registry ====================

class AIAgent(AuditMixin, Base):
    __tablename__ = "ai_agents"
    organization_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("organizations.id"), nullable=True)  # None for global agents
    agent_name: Mapped[str] = mapped_column(String(150))
    agent_type: Mapped[str] = mapped_column(SQLEnum(AgentType))
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    current_version: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[str] = mapped_column(SQLEnum(AgentStatus), default=AgentStatus.DRAFT)
    model_provider: Mapped[str] = mapped_column(SQLEnum(ModelProvider))
    model_name: Mapped[str] = mapped_column(String(100))
    allowed_tools: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    required_permissions: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    config_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    is_global: Mapped[bool] = mapped_column(default=False)  # Global agents available to all orgs


class AIAgentVersion(AuditMixin, Base):
    __tablename__ = "ai_agent_versions"
    agent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_agents.id"))
    version: Mapped[int] = mapped_column(Integer)
    system_prompt: Mapped[str] = mapped_column(TEXT)
    config_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    model_name: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(SQLEnum(AgentStatus), default=AgentStatus.DRAFT)
    changelog: Mapped[str | None] = mapped_column(TEXT, nullable=True)


# ==================== AI Tool Registry ====================

class AITool(AuditMixin, Base):
    __tablename__ = "ai_tools"
    tool_name: Mapped[str] = mapped_column(String(150), unique=True)
    description: Mapped[str] = mapped_column(TEXT)
    tool_path: Mapped[str] = mapped_column(String(255))  # Python module path
    required_permissions: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    hitl_requirement: Mapped[str] = mapped_column(SQLEnum(HITLRequirement), default=HITLRequirement.NOT_REQUIRED)
    risk_level: Mapped[str] = mapped_column(SQLEnum(ToolRisk), default=ToolRisk.LOW)
    input_schema: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # Pydantic schema
    output_schema: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # Pydantic schema
    is_active: Mapped[bool] = mapped_column(default=True)


# ==================== Prompt Templates ====================

class PromptTemplate(AuditMixin, Base):
    __tablename__ = "prompt_templates"
    organization_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("organizations.id"), nullable=True)
    template_name: Mapped[str] = mapped_column(String(150))
    template_type: Mapped[str] = mapped_column(String(100))  # agent_type or custom
    system_prompt: Mapped[str] = mapped_column(TEXT)
    variables: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # Variable schema
    status: Mapped[str] = mapped_column(SQLEnum(PromptStatus), default=PromptStatus.DRAFT)
    version: Mapped[int] = mapped_column(Integer, default=1)
    is_default: Mapped[bool] = mapped_column(default=False)


# ==================== Knowledge Documents ====================

class KnowledgeDocument(AuditMixin, Base):
    __tablename__ = "knowledge_documents"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    document_type: Mapped[str] = mapped_column(SQLEnum(DocumentType))
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(TEXT)
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    meta_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    embedding_status: Mapped[str] = mapped_column(SQLEnum(EmbeddingStatus), default=EmbeddingStatus.PENDING)
    chunk_count: Mapped[int] = mapped_column(Integer, default=0)
    is_public: Mapped[bool] = mapped_column(default=False)  # Public docs available to all orgs


class DocumentChunk(AuditMixin, Base):
    __tablename__ = "document_chunks"
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("knowledge_documents.id"))
    chunk_index: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(TEXT)
    embedding: Mapped[list[float] | None] = mapped_column(ARRAY(Float), nullable=True)  # pgvector
    chunk_meta: Mapped[dict | None] = mapped_column(JSON, nullable=True)


# ==================== AI Execution Tracking ====================

class AIExecution(AuditMixin, Base):
    __tablename__ = "ai_executions"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    agent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_agents.id"))
    agent_version: Mapped[int] = mapped_column(Integer)
    workflow_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("ai_workflows.id"), nullable=True)
    execution_id: Mapped[str] = mapped_column(String(100), unique=True)  # External execution ID
    status: Mapped[str] = mapped_column(SQLEnum(ExecutionStatus), default=ExecutionStatus.QUEUED)
    input_data: Mapped[dict] = mapped_column(JSON)
    output_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error_message: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    model_provider: Mapped[str] = mapped_column(SQLEnum(ModelProvider))
    model_name: Mapped[str] = mapped_column(String(100))
    tokens_in: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tokens_out: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estimated_cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    human_intervention: Mapped[bool] = mapped_column(default=False)
    hitl_count: Mapped[int] = mapped_column(Integer, default=0)
    langsmith_trace_id: Mapped[str | None] = mapped_column(String(255), nullable=True)


# ==================== HITL State ====================

class HITLState(AuditMixin, Base):
    __tablename__ = "hitl_states"
    execution_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_executions.id"))
    agent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_agents.id"))
    status: Mapped[str] = mapped_column(String(50), default="Pending")  # Pending, Approved, Rejected, Modified
    request_data: Mapped[dict] = mapped_column(JSON)
    response_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    decision: Mapped[str | None] = mapped_column(SQLEnum(HITLDecision), nullable=True)
    decision_reason: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    requested_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))  # User ID
    responded_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    responded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    timeout_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


# ==================== AI Workflows ====================

class AIWorkflow(AuditMixin, Base):
    __tablename__ = "ai_workflows"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    workflow_name: Mapped[str] = mapped_column(String(150))
    workflow_type: Mapped[str] = mapped_column(String(100))  # screening, sourcing, etc.
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    definition: Mapped[dict] = mapped_column(JSON)  # Workflow graph definition
    status: Mapped[str] = mapped_column(SQLEnum(WorkflowStatus), default=WorkflowStatus.DRAFT)
    version: Mapped[int] = mapped_column(Integer, default=1)
    is_default: Mapped[bool] = mapped_column(default=False)


class WorkflowStep(AuditMixin, Base):
    __tablename__ = "workflow_steps"
    workflow_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_workflows.id"))
    step_name: Mapped[str] = mapped_column(String(150))
    agent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_agents.id"))
    step_order: Mapped[int] = mapped_column(Integer)
    step_config: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    hitl_required: Mapped[bool] = mapped_column(default=False)
    conditions: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # Conditional execution


# ==================== AI Usage Tracking ====================

class AIUsage(AuditMixin, Base):
    __tablename__ = "ai_usage"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    agent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_agents.id"))
    workflow_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("ai_workflows.id"), nullable=True)
    execution_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    model_provider: Mapped[str] = mapped_column(SQLEnum(ModelProvider))
    model_name: Mapped[str] = mapped_column(String(100))
    tokens_in: Mapped[int] = mapped_column(Integer)
    tokens_out: Mapped[int] = mapped_column(Integer)
    total_tokens: Mapped[int] = mapped_column(Integer)
    latency_ms: Mapped[int] = mapped_column(Integer)
    estimated_cost: Mapped[float] = mapped_column(Float)
    execution_count: Mapped[int] = mapped_column(Integer, default=1)


# ==================== AI Guardrails ====================

class AIGuardrail(AuditMixin, Base):
    __tablename__ = "ai_guardrails"
    organization_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("organizations.id"), nullable=True)
    guardrail_type: Mapped[str] = mapped_column(SQLEnum(GuardrailType))
    name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(TEXT)
    configuration: Mapped[dict] = mapped_column(JSON)
    is_active: Mapped[bool] = mapped_column(default=True)
    severity: Mapped[str] = mapped_column(String(50), default="Medium")  # Low, Medium, High, Critical