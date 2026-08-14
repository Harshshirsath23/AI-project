from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from datetime import datetime, timedelta

from app.core.observability import (
    get_current_trace_context, update_trace_context,
    trace_agent, trace_workflow, trace_tool, trace_rag, trace_hitl, trace_span
)
from app.modules.ai.models import (
    AIAgent, AIAgentVersion, AITool, PromptTemplate,
    KnowledgeDocument, DocumentChunk, AIExecution, HITLState,
    AIWorkflow, AIUsage
)
from app.modules.ai.schemas import (
    AIAgentCreate, AIAgentResponse, AIToolCreate, AIToolResponse,
    KnowledgeDocumentCreate, KnowledgeDocumentResponse,
    AIExecutionCreate, AIExecutionResponse, HITLRequest, HITLResponse,
    AIWorkflowCreate, AIWorkflowResponse, PromptTemplateCreate,
    RetrievalRequest, RetrievalResponse, UsageStatsResponse
)
from app.modules.ai.enums import (
    AgentStatus, ExecutionStatus, HITLRequirement, ModelProvider
)
from app.modules.ai.validators import (
    AgentValidator, ExecutionValidator, ToolValidator,
    KnowledgeValidator, GuardrailValidator
)
from app.modules.ai.exceptions import (
    AgentNotFoundException, ToolNotFoundException, KnowledgeDocumentNotFoundException,
    ExecutionNotFoundException, HITLException, ToolAuthorizationException
)
from app.modules.ai.repository import (
    AgentRepository, ToolRepository, KnowledgeRepository,
    ExecutionRepository, HITLRepository, WorkflowRepository, UsageRepository
)


class AgentService:
    """Service for AI agent management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.agent_repo = AgentRepository(db)
    
    async def create_agent(
        self, 
        org_id: uuid.UUID, 
        agent_data: AIAgentCreate
    ) -> Dict[str, Any]:
        """Create AI agent"""
        agent_dict = agent_data.model_dump()
        agent_dict["organization_id"] = org_id if not agent_data.is_global else None
        agent_dict["status"] = AgentStatus.DRAFT
        agent_dict["current_version"] = 1
        agent_dict["config_data"] = agent_dict.pop("configuration", None)
        
        agent = await self.agent_repo.create_agent(agent_dict)
        
        # Create initial version
        version_data = {
            "agent_id": agent.id,
            "version": 1,
            "system_prompt": (agent_dict.get("config_data") or {}).get("system_prompt", ""),
            "config_data": agent_dict.get("config_data"),
            "model_name": agent_data.model_name,
            "changelog": "Initial version"
        }
        await self.agent_repo.create_agent_version(version_data)
        
        return {
            "status": "success",
            "agent_id": str(agent.id),
            "message": "Agent created successfully"
        }
    
    async def get_agent(self, agent_id: uuid.UUID) -> Optional[AIAgent]:
        """Get agent by ID"""
        agent = await self.agent_repo.get_agent_by_id(agent_id)
        if not agent:
            raise AgentNotFoundException(str(agent_id))
        return agent


class ToolService:
    """Service for AI tool management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.tool_repo = ToolRepository(db)
    
    async def create_tool(self, tool_data: AIToolCreate) -> Dict[str, Any]:
        """Create AI tool"""
        tool_dict = tool_data.model_dump()
        tool = await self.tool_repo.create_tool(tool_dict)
        
        return {
            "status": "success",
            "tool_id": str(tool.id),
            "message": "Tool created successfully"
        }
    
    async def get_tool(self, tool_name: str) -> Optional[AITool]:
        """Get tool by name"""
        tool = await self.tool_repo.get_tool_by_name(tool_name)
        if not tool:
            raise ToolNotFoundException(tool_name)
        return tool
    
    async def validate_tool_access(
        self, 
        tool_name: str, 
        user_permissions: List[str]
    ) -> Dict[str, Any]:
        """Validate tool access"""
        tool = await self.get_tool(tool_name)
        
        return ToolValidator.validate_tool_authorization(
            tool.required_permissions or [],
            user_permissions,
            tool.hitl_requirement,
            tool.risk_level
        )


class KnowledgeService:
    """Service for knowledge management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.knowledge_repo = KnowledgeRepository(db)
    
    async def create_document(
        self, 
        org_id: uuid.UUID, 
        document_data: KnowledgeDocumentCreate
    ) -> Dict[str, Any]:
        """Create knowledge document"""
        KnowledgeValidator.validate_document_content(document_data.content)
        
        document_dict = document_data.model_dump()
        document_dict["organization_id"] = org_id
        document = await self.knowledge_repo.create_document(document_dict)
        
        # Trigger embedding pipeline (placeholder)
        # In production, this would queue an embedding job
        
        return {
            "status": "success",
            "document_id": str(document.id),
            "message": "Document created successfully"
        }
    
    async def get_document(self, doc_id: uuid.UUID) -> Optional[KnowledgeDocument]:
        """Get document by ID"""
        document = await self.knowledge_repo.get_document_by_id(doc_id)
        if not document:
            raise KnowledgeDocumentNotFoundException(str(doc_id))
        return document
    
    async def retrieve_knowledge(
        self, 
        org_id: uuid.UUID, 
        retrieval_request: RetrievalRequest
    ) -> RetrievalResponse:
        """Retrieve knowledge using pgvector (placeholder)"""
        KnowledgeValidator.validate_retrieval_query(retrieval_request.query)
        update_trace_context(organization_id=org_id)
        
        async with trace_rag(query=retrieval_request.query, top_k=retrieval_request.top_k) as span:
            response = RetrievalResponse(
                documents=[],
                scores=[],
                total_count=0
            )
            span.end(outputs={"documents_retrieved": response.total_count, "scores": response.scores})
            return response


class ExecutionService:
    """Service for AI execution tracking with LangSmith observability correlation"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.execution_repo = ExecutionRepository(db)
        self.hitl_repo = HITLRepository(db)
        self.usage_repo = UsageRepository(db)
        self.agent_repo = AgentRepository(db)
    
    async def create_execution(
        self, 
        org_id: uuid.UUID, 
        execution_data: AIExecutionCreate
    ) -> Dict[str, Any]:
        """Create AI execution and correlate with LangSmith trace ID"""
        ExecutionValidator.validate_execution_input(execution_data.input_data)
        
        agent = None
        try:
            agent = await self.agent_repo.get_agent_by_id(execution_data.agent_id)
        except Exception:
            agent = None

        model_provider = getattr(agent, "model_provider", ModelProvider.OPENAI) if (agent and hasattr(agent, "model_provider")) else ModelProvider.OPENAI
        model_name = getattr(agent, "model_name", "gpt-4") if (agent and hasattr(agent, "model_name")) else "gpt-4"
        agent_version = getattr(agent, "current_version", 1) if (agent and hasattr(agent, "current_version")) else 1

        ctx = update_trace_context(
            organization_id=org_id,
            agent_id=execution_data.agent_id,
            agent_version=agent_version,
            workflow_id=execution_data.workflow_id
        )

        execution_dict = execution_data.model_dump()
        execution_dict["organization_id"] = org_id
        execution_dict["status"] = ExecutionStatus.QUEUED
        execution_dict["execution_id"] = str(uuid.uuid4())
        execution_dict["model_provider"] = model_provider
        execution_dict["model_name"] = model_name
        execution_dict["agent_version"] = agent_version
        execution_dict["langsmith_trace_id"] = ctx.trace_id
        
        execution = await self.execution_repo.create_execution(execution_dict)
        update_trace_context(execution_id=execution.id)
        
        return {
            "status": "success",
            "execution_id": str(execution.id),
            "langsmith_trace_id": ctx.trace_id,
            "message": "Execution queued successfully"
        }
    
    async def start_execution(self, execution_id: uuid.UUID) -> None:
        """Start execution"""
        ctx = get_current_trace_context()
        await self.execution_repo.update_execution_status(
            execution_id, 
            ExecutionStatus.RUNNING,
            langsmith_trace_id=ctx.trace_id
        )
    
    async def complete_execution(
        self, 
        execution_id: uuid.UUID, 
        output_data: dict,
        tokens_in: int,
        tokens_out: int,
        latency_ms: int
    ) -> None:
        """Complete execution"""
        ctx = get_current_trace_context()
        await self.execution_repo.update_execution_status(
            execution_id,
            ExecutionStatus.COMPLETED,
            output_data=output_data,
            langsmith_trace_id=ctx.trace_id
        )
        
        # Track usage in PostgreSQL for business accounting
        execution = await self.execution_repo.get_execution_by_id(execution_id)
        if execution:
            usage_data = {
                "organization_id": execution.organization_id,
                "agent_id": execution.agent_id,
                "workflow_id": execution.workflow_id,
                "execution_date": datetime.now(),
                "model_provider": execution.model_provider,
                "model_name": execution.model_name,
                "tokens_in": tokens_in,
                "tokens_out": tokens_out,
                "total_tokens": tokens_in + tokens_out,
                "latency_ms": latency_ms,
                "estimated_cost": (tokens_in + tokens_out) * 0.0001  # Placeholder pricing
            }
            await self.usage_repo.create_usage_record(usage_data)
    
    async def request_hitl(
        self, 
        execution_id: uuid.UUID, 
        hitl_request: HITLRequest
    ) -> Dict[str, Any]:
        """Request HITL intervention and record telemetry trace"""
        execution = await self.execution_repo.get_execution_by_id(execution_id)
        if not execution:
            raise ExecutionNotFoundException(str(execution_id))
        
        # Update execution status
        await self.execution_repo.update_execution_status(
            execution_id,
            ExecutionStatus.WAITING_HITL
        )
        
        # Create HITL state
        hitl_data = {
            "execution_id": execution_id,
            "agent_id": execution.agent_id,
            "request_data": hitl_request.request_data,
            "requested_by": uuid.uuid4(),  # Would be actual user ID
            "requested_at": datetime.now(),
            "timeout_at": datetime.now() + timedelta(minutes=hitl_request.timeout_minutes)
        }
        hitl = await self.hitl_repo.create_hitl_state(hitl_data)
        
        update_trace_context(
            hitl_id=hitl.id,
            execution_id=execution_id,
            agent_id=execution.agent_id,
            organization_id=execution.organization_id
        )

        hitl_reason = str(hitl_request.request_data.get("reason", "Human intervention requested")) if isinstance(hitl_request.request_data, dict) else "Human intervention requested"

        # Emit HITL telemetry event span asynchronously
        async with trace_hitl(
            execution_id=str(execution_id),
            agent_id=str(execution.agent_id),
            hitl_reason=hitl_reason,
            risk_level="High"
        ) as span:
            span.end(outputs={"status": "WAITING_HITL", "hitl_id": str(hitl.id)})
        
        return {
            "status": "success",
            "hitl_id": str(hitl.id),
            "message": "HITL request created"
        }
    
    async def respond_hitl(
        self, 
        hitl_id: uuid.UUID, 
        hitl_response: HITLResponse
    ) -> Dict[str, Any]:
        """Respond to HITL request and update observability trace"""
        await self.hitl_repo.update_hitl_decision(
            hitl_id,
            hitl_response.decision,
            hitl_response.decision_reason,
            hitl_response.modified_data
        )

        update_trace_context(
            hitl_id=hitl_id,
            hitl_decision=str(hitl_response.decision)
        )
        
        return {
            "status": "success",
            "message": "HITL response recorded"
        }



class WorkflowService:
    """Service for workflow management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.workflow_repo = WorkflowRepository(db)
    
    async def create_workflow(
        self, 
        org_id: uuid.UUID, 
        workflow_data: AIWorkflowCreate
    ) -> Dict[str, Any]:
        """Create workflow"""
        workflow_dict = workflow_data.model_dump()
        workflow_dict["organization_id"] = org_id
        workflow = await self.workflow_repo.create_workflow(workflow_dict)
        
        return {
            "status": "success",
            "workflow_id": str(workflow.id),
            "message": "Workflow created successfully"
        }
    
    async def get_workflow(self, workflow_id: uuid.UUID) -> Optional[AIWorkflow]:
        """Get workflow by ID"""
        return await self.workflow_repo.get_workflow_by_id(workflow_id)


class GuardrailService:
    """Service for AI guardrails"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def validate_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate input against guardrails"""
        GuardrailValidator.validate_input_for_injection(input_data)
        
        return {
            "status": "success",
            "passed": True
        }
    
    async def validate_output(
        self, 
        output_data: Dict[str, Any], 
        output_schema: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Validate output against guardrails"""
        if output_schema:
            GuardrailValidator.validate_output_structure(output_data, output_schema)
        
        return {
            "status": "success",
            "passed": True
        }