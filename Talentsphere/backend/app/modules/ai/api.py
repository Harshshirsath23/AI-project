from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import uuid

from app.database.session import get_async_db
from app.modules.auth.dependencies import (
    get_current_organization, get_current_user, require_permission
)
from app.modules.ai.schemas import (
    AIAgentCreate, AIAgentResponse, AIToolCreate, AIToolResponse,
    KnowledgeDocumentCreate, KnowledgeDocumentResponse,
    AIExecutionCreate, AIExecutionResponse, HITLRequest, HITLResponse,
    AIWorkflowCreate, AIWorkflowResponse, PromptTemplateCreate,
    RetrievalRequest, RetrievalResponse, UsageStatsResponse
)
from app.modules.ai.sourcing.schemas import (
    SourcingExecutionRequest, SourcingRecommendation
)
from app.modules.ai.service import (
    AgentService, ToolService, KnowledgeService,
    ExecutionService, WorkflowService, GuardrailService
)

router = APIRouter(prefix="/ai", tags=["AI Intelligence"])


# ==================== Agent Endpoints ====================

@router.post("/agents", summary="Create AI Agent", dependencies=[Depends(require_permission("ai:manage"))])
async def create_agent(
    agent_data: AIAgentCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new AI agent"""
    service = AgentService(db)
    return await service.create_agent(org_id, agent_data)

@router.get("/agents/{agent_id}", response_model=AIAgentResponse, summary="Get Agent by ID", dependencies=[Depends(require_permission("ai:read"))])
async def get_agent(
    agent_id: uuid.UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """Get a specific agent by ID"""
    service = AgentService(db)
    return await service.get_agent(agent_id)


# ==================== Tool Endpoints ====================

@router.post("/tools", summary="Create AI Tool", dependencies=[Depends(require_permission("ai:manage"))])
async def create_tool(
    tool_data: AIToolCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new AI tool"""
    service = ToolService(db)
    return await service.create_tool(tool_data)

@router.get("/tools/{tool_name}", response_model=AIToolResponse, summary="Get Tool by Name", dependencies=[Depends(require_permission("ai:read"))])
async def get_tool(
    tool_name: str,
    db: AsyncSession = Depends(get_async_db)
):
    """Get a specific tool by name"""
    service = ToolService(db)
    return await service.get_tool(tool_name)


# ==================== Knowledge Endpoints ====================

@router.post("/knowledge/documents", summary="Create Knowledge Document", dependencies=[Depends(require_permission("ai:manage"))])
async def create_document(
    document_data: KnowledgeDocumentCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a knowledge document"""
    service = KnowledgeService(db)
    return await service.create_document(org_id, document_data)

@router.get("/knowledge/documents/{doc_id}", response_model=KnowledgeDocumentResponse, summary="Get Document by ID", dependencies=[Depends(require_permission("ai:read"))])
async def get_document(
    doc_id: uuid.UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """Get a specific document by ID"""
    service = KnowledgeService(db)
    return await service.get_document(doc_id)

@router.post("/knowledge/retrieve", response_model=RetrievalResponse, summary="Retrieve Knowledge", dependencies=[Depends(require_permission("ai:read"))])
async def retrieve_knowledge(
    retrieval_request: RetrievalRequest,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Retrieve knowledge using RAG"""
    service = KnowledgeService(db)
    return await service.retrieve_knowledge(org_id, retrieval_request)


# ==================== Milestone 12: Enhanced Sourcing Engine Endpoints ====================

@router.post("/sourcing/execute", summary="Execute Enhanced Intelligent Candidate Sourcing Workflow", dependencies=[Depends(require_permission("ai:execute"))])
async def execute_sourcing_workflow(
    request: SourcingExecutionRequest,
    org_id: uuid.UUID = Depends(get_current_organization),
    user_id: uuid.UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Initiate autonomous candidate sourcing and discovery for a job with 14-agent orchestration.
    
    Workflow includes:
    - Job Enhancement: Role classification, JD optimization, keyword extraction, salary band analysis, location analysis
    - Candidate Sourcing: Discovery, intelligence analysis, matching, compliance checks
    - Ranking & Recommendation: Candidate ranking, recommendation generation
    - Publishing: Optional job board publishing
    """
    from app.modules.ai.engine import AgentRuntime
    from app.modules.ai.repository import AgentRepository
    agent_repo = AgentRepository(db)
    agents = await agent_repo.get_agents_by_org(org_id)
    agent_id = agents[0].id if agents else uuid.uuid4()

    input_payload = {
        "job_id": str(request.job_id),
        "workflow_type": "sourcing"
    }
    if request.weights:
        input_payload["weights"] = request.weights.model_dump()
    if request.publish_to_boards:
        input_payload["publish_to_boards"] = request.publish_to_boards
    if request.target_boards:
        input_payload["target_boards"] = request.target_boards

    runtime = AgentRuntime(db)
    return await runtime.execute(
        organization_id=org_id,
        user_id=user_id,
        agent_id=agent_id,
        input_data=input_payload,
        user_permissions=["candidate:read", "candidate:write", "recruitment:read", "ai:execute"]
    )

@router.post("/sourcing/optimize-jd", summary="Optimize Job Description", dependencies=[Depends(require_permission("ai:execute"))])
async def optimize_job_description(
    job_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Optimize job description for SEO, clarity, and candidate attraction."""
    from app.modules.ai.sourcing.agents import JDOptimizerAgent
    from app.modules.ai.engine.tools import ToolExecutionFramework
    
    tool_framework = ToolExecutionFramework(db)
    jd_optimizer = JDOptimizerAgent()
    
    # Get job data
    job_res = await tool_framework.execute_tool(
        tool_name="get_job",
        org_id=org_id,
        user_permissions=["recruitment:read"],
        tool_input={"job_id": str(job_id)}
    )
    
    job_data = job_res.get("result", {})
    optimized_jd = await jd_optimizer.optimize_jd(job_data)
    
    return optimized_jd

@router.post("/sourcing/extract-keywords", summary="Extract Job Keywords", dependencies=[Depends(require_permission("ai:execute"))])
async def extract_job_keywords(
    job_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Extract and categorize keywords from job description for search optimization."""
    from app.modules.ai.sourcing.agents import KeywordExtractorAgent
    from app.modules.ai.engine.tools import ToolExecutionFramework
    
    tool_framework = ToolExecutionFramework(db)
    keyword_extractor = KeywordExtractorAgent()
    
    # Get job data
    job_res = await tool_framework.execute_tool(
        tool_name="get_job",
        org_id=org_id,
        user_permissions=["recruitment:read"],
        tool_input={"job_id": str(job_id)}
    )
    
    job_data = job_res.get("result", {})
    keywords = await keyword_extractor.extract_keywords(job_data)
    
    return keywords

@router.post("/sourcing/salary-band", summary="Get Salary Band Recommendation", dependencies=[Depends(require_permission("ai:execute"))])
async def get_salary_band_recommendation(
    job_id: uuid.UUID,
    location: Optional[str] = None,
    experience_level: Optional[str] = None,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Generate salary band recommendations based on market data."""
    from app.modules.ai.sourcing.agents import SalaryBandAgent
    from app.modules.ai.engine.tools import ToolExecutionFramework
    
    tool_framework = ToolExecutionFramework(db)
    salary_agent = SalaryBandAgent()
    
    # Get job data
    job_res = await tool_framework.execute_tool(
        tool_name="get_job",
        org_id=org_id,
        user_permissions=["recruitment:read"],
        tool_input={"job_id": str(job_id)}
    )
    
    job_data = job_res.get("result", {})
    salary_band = await salary_agent.recommend_salary_band(job_data, location, experience_level)
    
    return salary_band

@router.post("/sourcing/location-analysis", summary="Get Location Analysis", dependencies=[Depends(require_permission("ai:execute"))])
async def get_location_analysis(
    job_id: uuid.UUID,
    location_requirements: Optional[dict] = None,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Analyze location requirements and provide talent market insights."""
    from app.modules.ai.sourcing.agents import LocationAnalyzerAgent
    from app.modules.ai.engine.tools import ToolExecutionFramework
    
    tool_framework = ToolExecutionFramework(db)
    location_agent = LocationAnalyzerAgent()
    
    # Get job data
    job_res = await tool_framework.execute_tool(
        tool_name="get_job",
        org_id=org_id,
        user_permissions=["recruitment:read"],
        tool_input={"job_id": str(job_id)}
    )
    
    job_data = job_res.get("result", {})
    location_analysis = await location_agent.analyze_location(job_data, location_requirements)
    
    return location_analysis

@router.post("/sourcing/classify-role", summary="Classify Job Role", dependencies=[Depends(require_permission("ai:execute"))])
async def classify_job_role(
    job_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Classify job role into standard categories and families."""
    from app.modules.ai.sourcing.agents import RoleClassifierAgent
    from app.modules.ai.engine.tools import ToolExecutionFramework
    
    tool_framework = ToolExecutionFramework(db)
    role_classifier = RoleClassifierAgent()
    
    # Get job data
    job_res = await tool_framework.execute_tool(
        tool_name="get_job",
        org_id=org_id,
        user_permissions=["recruitment:read"],
        tool_input={"job_id": str(job_id)}
    )
    
    job_data = job_res.get("result", {})
    classification = await role_classifier.classify_role(job_data)
    
    return classification

@router.post("/sourcing/publish-job", summary="Publish Job to Boards", dependencies=[Depends(require_permission("ai:execute"))])
async def publish_job_to_boards(
    job_id: uuid.UUID,
    target_boards: Optional[List[str]] = None,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Publish job posting to multiple job boards simultaneously."""
    from app.modules.ai.sourcing.agents import JobBoardPublisherAgent
    from app.modules.ai.engine.tools import ToolExecutionFramework
    
    tool_framework = ToolExecutionFramework(db)
    publisher = JobBoardPublisherAgent(tool_framework)
    
    # Get job data
    job_res = await tool_framework.execute_tool(
        tool_name="get_job",
        org_id=org_id,
        user_permissions=["recruitment:read"],
        tool_input={"job_id": str(job_id)}
    )
    
    job_data = job_res.get("result", {})
    job_data["job_id"] = str(job_id)
    
    publishing_results = await publisher.publish_to_boards(job_data, target_boards)
    
    return publishing_results

@router.get("/sourcing/executions/{execution_id}", summary="Get Sourcing Execution Details", dependencies=[Depends(require_permission("ai:read"))])
async def get_sourcing_execution(
    execution_id: uuid.UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """Get candidate sourcing execution status and details."""
    service = ExecutionService(db)
    execution = await service.execution_repo.get_execution_by_id(execution_id)
    if not execution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sourcing execution not found")
    return execution

@router.get("/sourcing/executions/{execution_id}/recommendations", response_model=SourcingRecommendation, summary="Get Candidate Sourcing Recommendation Report", dependencies=[Depends(require_permission("ai:read"))])
async def get_sourcing_recommendations(
    execution_id: uuid.UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """Get final recruiter-facing structured candidate recommendations."""
    service = ExecutionService(db)
    execution = await service.execution_repo.get_execution_by_id(execution_id)
    if not execution or not execution.output_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendations not available or execution not completed")
    return SourcingRecommendation(**execution.output_data)

@router.post("/sourcing/executions/{execution_id}/resume", summary="Resume Paused Sourcing Execution", dependencies=[Depends(require_permission("ai:execute"))])
async def resume_sourcing_execution(
    execution_id: uuid.UUID,
    hitl_response: HITLResponse,
    db: AsyncSession = Depends(get_async_db)
):
    """Resume candidate sourcing workflow post-recruiter approval decision."""
    from app.modules.ai.engine import AgentRuntime
    runtime = AgentRuntime(db)
    return await runtime.resume(execution_id, hitl_response)


# ==================== Agentic Execution Engine Endpoints ====================

@router.post("/execute", summary="Execute Agent or Workflow via AgentRuntime", dependencies=[Depends(require_permission("ai:execute"))])
async def execute_agent_runtime(
    request: AIExecutionCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    user_id: uuid.UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Execute a registered agent via the AgentRuntime gateway."""
    from app.modules.ai.engine import AgentRuntime
    runtime = AgentRuntime(db)
    return await runtime.execute(
        organization_id=org_id,
        user_id=user_id,
        agent_id=request.agent_id,
        input_data=request.input_data,
        workflow_id=request.workflow_id,
        user_permissions=["candidate:read", "candidate:write", "recruitment:read", "ai:execute"]
    )

@router.post("/executions", summary="Create AI Execution", dependencies=[Depends(require_permission("ai:execute"))])
async def create_execution(
    execution_data: AIExecutionCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Create and queue an AI execution"""
    from app.core.observability import update_trace_context
    update_trace_context(organization_id=org_id, agent_id=execution_data.agent_id, workflow_id=execution_data.workflow_id)
    service = ExecutionService(db)
    return await service.create_execution(org_id, execution_data)

@router.get("/executions/{execution_id}", response_model=AIExecutionResponse, summary="Get Execution by ID", dependencies=[Depends(require_permission("ai:read"))])
async def get_execution(
    execution_id: uuid.UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """Get a specific execution by ID"""
    service = ExecutionService(db)
    return await service.execution_repo.get_execution_by_id(execution_id)

@router.post("/executions/{execution_id}/resume", summary="Resume Paused HITL Execution", dependencies=[Depends(require_permission("ai:execute"))])
async def resume_execution(
    execution_id: uuid.UUID,
    hitl_response: HITLResponse,
    db: AsyncSession = Depends(get_async_db)
):
    """Resume execution following human decision approval"""
    from app.modules.ai.engine import AgentRuntime
    runtime = AgentRuntime(db)
    return await runtime.resume(execution_id, hitl_response)

@router.post("/executions/{execution_id}/cancel", summary="Cancel Running Execution", dependencies=[Depends(require_permission("ai:execute"))])
async def cancel_execution(
    execution_id: uuid.UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """Cancel an active or queued execution"""
    service = ExecutionService(db)
    await service.execution_repo.update_execution_status(execution_id, "FAILED", error_message="Cancelled by user")
    return {"status": "success", "execution_id": str(execution_id), "message": "Execution cancelled successfully."}

@router.get("/executions/{execution_id}/events", summary="Get Execution Events History", dependencies=[Depends(require_permission("ai:read"))])
async def get_execution_events(
    execution_id: uuid.UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """Get step history events for an execution"""
    service = ExecutionService(db)
    execution = await service.execution_repo.get_execution_by_id(execution_id)
    if not execution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Execution not found")
    
    events = [
        {"step": "queued", "timestamp": execution.started_at or execution.created_at, "status": "QUEUED"},
        {"step": "running", "timestamp": execution.started_at, "status": "RUNNING"},
    ]
    if execution.status == "WAITING_HITL":
        events.append({"step": "hitl_interruption", "timestamp": execution.updated_at, "status": "WAITING_HITL"})
    elif execution.status == "COMPLETED":
        events.append({"step": "completed", "timestamp": execution.completed_at, "status": "COMPLETED"})
    elif execution.status == "FAILED":
        events.append({"step": "failed", "timestamp": execution.completed_at, "status": "FAILED", "error": execution.error_message})

    return {
        "execution_id": str(execution_id),
        "status": execution.status,
        "langsmith_trace_id": execution.langsmith_trace_id,
        "events": events
    }

@router.post("/executions/{execution_id}/hitl", summary="Request HITL", dependencies=[Depends(require_permission("ai:execute"))])
async def request_hitl(
    execution_id: uuid.UUID,
    hitl_request: HITLRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """Request human-in-the-loop intervention"""
    service = ExecutionService(db)
    return await service.request_hitl(execution_id, hitl_request)

@router.post("/hitl/{hitl_id}/respond", summary="Respond to HITL", dependencies=[Depends(require_permission("ai:execute"))])
async def respond_hitl(
    hitl_id: uuid.UUID,
    hitl_response: HITLResponse,
    db: AsyncSession = Depends(get_async_db)
):
    """Respond to HITL request"""
    service = ExecutionService(db)
    return await service.respond_hitl(hitl_id, hitl_response)


# ==================== Workflow Endpoints ====================

@router.post("/workflows", summary="Create Workflow", dependencies=[Depends(require_permission("ai:manage"))])
async def create_workflow(
    workflow_data: AIWorkflowCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new workflow"""
    service = WorkflowService(db)
    return await service.create_workflow(org_id, workflow_data)

@router.get("/workflows/{workflow_id}", response_model=AIWorkflowResponse, summary="Get Workflow by ID", dependencies=[Depends(require_permission("ai:read"))])
async def get_workflow(
    workflow_id: uuid.UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """Get a specific workflow by ID"""
    service = WorkflowService(db)
    return await service.get_workflow(workflow_id)


# ==================== Guardrail Endpoints ====================

@router.post("/guardrails/validate-input", summary="Validate Input", dependencies=[Depends(require_permission("ai:execute"))])
async def validate_input(
    input_data: dict,
    db: AsyncSession = Depends(get_async_db)
):
    """Validate input against guardrails"""
    service = GuardrailService(db)
    return await service.validate_input(input_data)

@router.post("/guardrails/validate-output", summary="Validate Output", dependencies=[Depends(require_permission("ai:execute"))])
async def validate_output(
    output_data: dict,
    output_schema: Optional[dict] = None,
    db: AsyncSession = Depends(get_async_db)
):
    """Validate output against guardrails"""
    service = GuardrailService(db)
    return await service.validate_output(output_data, output_schema)


# ==================== Master Supervisor Endpoints (Multi-Domain Orchestration) ====================

class SupervisorRequest(BaseModel):
    """Request model for Master Supervisor"""
    user_input: str = Field(..., description="Natural language user request")
    request_data: Optional[Dict[str, Any]] = Field(None, description="Structured request data")


@router.post("/supervisor/execute", summary="Execute Master Supervisor Multi-Domain Orchestration", dependencies=[Depends(require_permission("ai:execute"))])
async def execute_supervisor(
    request: SupervisorRequest,
    org_id: uuid.UUID = Depends(get_current_organization),
    user_id: uuid.UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Execute Master Supervisor for intelligent multi-domain workflow orchestration.
    
    The Master Supervisor:
    1. Classifies user intent from natural language input
    2. Routes to appropriate domain subgraph (Sourcing, Screening, Interviews, Offers)
    3. Executes the selected workflow with full observability
    4. Manages HITL (Human-in-the-Loop) approval gates if needed
    5. Returns comprehensive execution results with recommendations
    
    Example requests:
    - "Find Python engineers in San Francisco with 5+ years experience"
    - "Extract resume data from uploaded files and score candidates"
    - "Schedule interviews with top 5 candidates"
    - "Generate offers for selected candidates"
    """
    from app.modules.ai.engine.supervisor import MasterSupervisor
    
    supervisor = MasterSupervisor(db)
    
    result = await supervisor.execute(
        organization_id=org_id,
        user_id=user_id,
        user_input=request.user_input,
        request_data=request.request_data or {}
    )
    
    return result


@router.post("/supervisor/intents/classify", summary="Classify User Intent", dependencies=[Depends(require_permission("ai:execute"))])
async def classify_user_intent(
    user_input: str,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Classify user intent for workflow routing.
    
    Returns:
    - domain: Classified workflow domain
    - intent: Specific user intent
    - confidence: Classification confidence (0-1)
    - requires_hitl: Whether human approval is needed
    - reasoning: Explanation for classification
    """
    from app.modules.ai.engine.supervisor import MasterSupervisor
    
    supervisor = MasterSupervisor(db)
    
    # Use internal intent classifier
    from app.modules.ai.engine.state import AgentExecutionStateDict
    state: AgentExecutionStateDict = {
        "organization_id": str(org_id),
        "user_id": "system",
        "agent_id": "intent-classifier",
        "execution_id": str(uuid.uuid4()),
        "request": {"user_input": user_input},
        "user_input": user_input,
        "intermediate_results": {},
        "final_output": {},
        "status": "PENDING",
        "errors": []
    }
    
    # Classify intent
    from app.modules.ai.engine.supervisor import MasterSupervisorState
    supervisor_state = MasterSupervisorState(
        organization_id=str(org_id),
        user_id="system",
        execution_id=str(uuid.uuid4()),
        user_input=user_input,
        original_request={"user_input": user_input}
    )
    
    supervisor_state = await supervisor._node_intent_classifier(supervisor_state)
    
    if supervisor_state.intent_classification:
        return supervisor_state.intent_classification.model_dump()
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to classify user intent"
        )


@router.get("/supervisor/domains", summary="List Available Workflow Domains", dependencies=[Depends(require_permission("ai:read"))])
async def list_workflow_domains():
    """
    List all available workflow domains that Master Supervisor can route to.
    
    Returns:
    - SOURCING: Candidate discovery & JD optimization
    - SCREENING: Resume parsing & candidate matching
    - INTERVIEWS: Interview scheduling & assessment
    - OFFERS: Offer generation & onboarding
    - REPORTING: Analytics & dashboards
    - KNOWLEDGE: RAG & knowledge base queries
    - COMPLIANCE: Audit & policy checks
    """
    from app.modules.ai.engine.supervisor import WorkflowDomain
    
    return {
        "domains": [
            {
                "name": domain.value,
                "description": {
                    WorkflowDomain.SOURCING: "Intelligent candidate discovery and job description optimization",
                    WorkflowDomain.SCREENING: "Resume parsing, candidate matching, and filtering",
                    WorkflowDomain.INTERVIEWS: "Interview scheduling, assessment, and evaluation",
                    WorkflowDomain.OFFERS: "Offer letter generation, negotiation, and onboarding",
                    WorkflowDomain.REPORTING: "Analytics, dashboards, and business intelligence",
                    WorkflowDomain.KNOWLEDGE: "RAG-based knowledge base retrieval and search",
                    WorkflowDomain.COMPLIANCE: "Audit trails, fairness checks, and policy compliance"
                }.get(domain, "")
            }
            for domain in WorkflowDomain
        ]
    }