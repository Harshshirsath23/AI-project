"""
Master Supervisor Agent with LangGraph Integration

Orchestrates multi-domain subgraph routing for TalentSphere AI platform:
- Intelligent intent classification from user input
- Dynamic subgraph router to Sourcing, Screening, Interview, Offer domains
- State machine coordination across multi-agent workflows
- Human-in-the-Loop pause/resume capability
- Comprehensive error handling and fallback strategies
"""

import uuid
import json
import structlog
from typing import Dict, Any, Optional, List, Literal
from enum import Enum
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage

from app.modules.ai.engine.state import AgentExecutionStateDict
from app.modules.ai.engine.llm import LLMService, LLMProvider
from app.modules.ai.engine.tools import ToolExecutionFramework
from app.modules.ai.engine.hitl import HITLGateManager
from app.modules.ai.workflows.sourcing_workflow import IntelligentSourcingWorkflow
from app.core.observability import trace_agent, trace_workflow, trace_span

logger = structlog.get_logger(__name__)


class WorkflowDomain(str, Enum):
    """Available workflow domains in TalentSphere"""
    SOURCING = "sourcing"  # Candidate discovery & JD optimization
    SCREENING = "screening"  # Resume parsing & matching
    INTERVIEWS = "interviews"  # Interview scheduling & assessment
    OFFERS = "offers"  # Offer generation & onboarding
    REPORTING = "reporting"  # Analytics & reporting
    KNOWLEDGE = "knowledge"  # RAG & knowledge base operations
    COMPLIANCE = "compliance"  # Audit & compliance checks


class IntentClassification(BaseModel):
    """Result of intent classification from user input"""
    domain: WorkflowDomain = Field(..., description="Target workflow domain")
    intent: str = Field(..., description="Classified user intent")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    requires_hitl: bool = Field(False, description="Whether human-in-loop approval is needed")
    risk_level: Literal["LOW", "MEDIUM", "HIGH"] = Field("LOW", description="Risk assessment")
    reasoning: str = Field(..., description="Explanation for intent classification")
    suggested_workflow: str = Field(..., description="Recommended workflow to execute")


class MasterSupervisorState(BaseModel):
    """Internal state for Master Supervisor LangGraph"""
    organization_id: str
    user_id: str
    execution_id: str
    user_input: str
    original_request: Dict[str, Any]
    
    # Intent classification result
    intent_classification: Optional[IntentClassification] = None
    
    # Routing and execution
    target_domain: Optional[WorkflowDomain] = None
    workflow_result: Optional[Dict[str, Any]] = None
    
    # Status tracking
    status: Literal["PENDING", "CLASSIFYING", "ROUTING", "EXECUTING", "COMPLETED", "FAILED", "WAITING_HITL"] = "PENDING"
    errors: List[str] = Field(default_factory=list)
    
    # HITL support
    hitl_request: Optional[Dict[str, Any]] = None
    human_decision: Optional[str] = None


class MasterSupervisor:
    """
    Master Supervisor Agent for TalentSphere AI Platform.
    
    Responsibilities:
    1. Classify user intent from natural language input
    2. Route to appropriate domain subgraph (Sourcing, Screening, etc.)
    3. Coordinate multi-agent workflow execution
    4. Manage HITL (Human-in-the-Loop) approval gates
    5. Provide comprehensive error handling and fallback strategies
    6. Track execution metrics and observability
    """

    def __init__(
        self,
        db: AsyncSession,
        llm_service: Optional[LLMService] = None
    ):
        self.db = db
        self.llm_service = llm_service or LLMService(
            provider=LLMProvider.NEMOTRON,
            model_name="nvidia/nemotron-3-ultra",
            temperature=0.2
        )
        self.tool_framework = ToolExecutionFramework(db)
        self.hitl_manager = HITLGateManager(db)
        
        # Initialize domain-specific workflows
        self.sourcing_workflow = IntelligentSourcingWorkflow(db)
        
        # Build LangGraph state machine
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build LangGraph state machine for Master Supervisor orchestration."""
        graph = StateGraph(MasterSupervisorState)
        
        # Add nodes
        graph.add_node("intent_classifier", self._node_intent_classifier)
        graph.add_node("risk_assessment", self._node_risk_assessment)
        graph.add_node("domain_router", self._node_domain_router)
        graph.add_node("execute_sourcing", self._node_execute_sourcing)
        graph.add_node("execute_screening", self._node_execute_screening)
        graph.add_node("execute_interviews", self._node_execute_interviews)
        graph.add_node("execute_offers", self._node_execute_offers)
        graph.add_node("hitl_gate", self._node_hitl_gate)
        graph.add_node("finalizer", self._node_finalizer)
        graph.add_node("error_handler", self._node_error_handler)
        
        # Add edges
        graph.add_edge(START, "intent_classifier")
        graph.add_edge("intent_classifier", "risk_assessment")
        graph.add_edge("risk_assessment", "domain_router")
        
        # Conditional routing based on domain
        graph.add_conditional_edges(
            "domain_router",
            self._route_by_domain,
            {
                WorkflowDomain.SOURCING: "execute_sourcing",
                WorkflowDomain.SCREENING: "execute_screening",
                WorkflowDomain.INTERVIEWS: "execute_interviews",
                WorkflowDomain.OFFERS: "execute_offers",
                "error": "error_handler"
            }
        )
        
        # Domain execution flows to HITL or finalizer
        graph.add_edge("execute_sourcing", "hitl_gate")
        graph.add_edge("execute_screening", "hitl_gate")
        graph.add_edge("execute_interviews", "hitl_gate")
        graph.add_edge("execute_offers", "hitl_gate")
        
        # HITL gate conditional flow
        graph.add_conditional_edges(
            "hitl_gate",
            self._check_hitl_decision,
            {
                "approved": "finalizer",
                "pending": END,
                "rejected": "error_handler"
            }
        )
        
        graph.add_edge("finalizer", END)
        graph.add_edge("error_handler", END)
        
        return graph

    async def _node_intent_classifier(self, state: MasterSupervisorState) -> MasterSupervisorState:
        """
        Node 1: Classify user intent from natural language input.
        
        Determines which domain subgraph (Sourcing, Screening, Interviews, Offers, etc.)
        best matches the user's intent.
        """
        state.status = "CLASSIFYING"
        
        system_prompt = """You are TalentSphere's Master Intent Classifier.
        
Analyze the user's request and classify it into one of these domains:
1. SOURCING - Candidate discovery, JD optimization, job posting
2. SCREENING - Resume parsing, candidate matching, filtering
3. INTERVIEWS - Interview scheduling, assessments, feedback
4. OFFERS - Offer generation, negotiation, onboarding
5. REPORTING - Analytics, dashboards, reporting
6. KNOWLEDGE - RAG queries, knowledge base retrieval
7. COMPLIANCE - Audit trails, policy checks, fairness reviews

Return a JSON response with:
- domain: The primary domain (enum value)
- intent: The specific user intent
- confidence: Confidence score (0.0-1.0)
- requires_hitl: Whether human approval is needed
- risk_level: Risk assessment (LOW, MEDIUM, HIGH)
- reasoning: Brief explanation
- suggested_workflow: Specific workflow to execute
"""

        user_input = f"User Request: {state.user_input}\nContext: {json.dumps(state.original_request)}"

        async with trace_agent(
            agent_name="Intent Classifier",
            inputs={"user_input": state.user_input[:100]}
        ) as span:
            try:
                response = await self.llm_service.generate_response(
                    system_prompt=system_prompt,
                    user_input=user_input,
                    context={
                        "organization_id": state.organization_id,
                        "available_domains": [d.value for d in WorkflowDomain]
                    }
                )
                
                # Parse classification result
                classification_dict = self._parse_intent_classification(response)
                state.intent_classification = IntentClassification(**classification_dict)
                
                logger.info(
                    "Intent classification successful",
                    domain=state.intent_classification.domain,
                    confidence=state.intent_classification.confidence
                )
                span.end(outputs=classification_dict)
                
            except Exception as exc:
                logger.error("Intent classification failed", error=str(exc))
                state.errors.append(f"Intent classification error: {str(exc)}")
                state.status = "FAILED"
                span.end(error=exc)
        
        return state

    async def _node_risk_assessment(self, state: MasterSupervisorState) -> MasterSupervisorState:
        """
        Node 2: Perform risk assessment on the classified intent.
        
        Evaluates whether the request involves high-risk operations that
        require additional compliance checks or human approval.
        """
        if state.status == "FAILED" or not state.intent_classification:
            return state

        classification = state.intent_classification

        # Risk factors for HITL triggering
        high_risk_indicators = [
            classification.risk_level == "HIGH",
            classification.requires_hitl,
            "bulk_action" in state.user_input.lower(),
            "delete" in state.user_input.lower(),
            "override" in state.user_input.lower(),
        ]

        if any(high_risk_indicators) and classification.confidence < 0.95:
            classification.requires_hitl = True
            classification.risk_level = "HIGH"
            logger.warning(
                "High-risk operation detected",
                domain=classification.domain,
                risk_indicators=high_risk_indicators
            )

        return state

    async def _node_domain_router(self, state: MasterSupervisorState) -> MasterSupervisorState:
        """
        Node 3: Determine target domain and prepare for routing.
        """
        if state.status == "FAILED" or not state.intent_classification:
            return state

        state.target_domain = state.intent_classification.domain
        state.status = "ROUTING"
        
        logger.info(
            "Domain routing prepared",
            domain=state.target_domain,
            workflow=state.intent_classification.suggested_workflow
        )
        
        return state

    def _route_by_domain(self, state: MasterSupervisorState) -> str:
        """Determine which domain executor to invoke."""
        if state.status == "FAILED" or not state.target_domain:
            return "error"
        return state.target_domain.value

    async def _node_execute_sourcing(self, state: MasterSupervisorState) -> MasterSupervisorState:
        """Execute Intelligent Sourcing Workflow."""
        state.status = "EXECUTING"
        
        try:
            # Prepare workflow state
            workflow_state: AgentExecutionStateDict = {
                "organization_id": state.organization_id,
                "user_id": state.user_id,
                "agent_id": str(uuid.uuid4()),
                "execution_id": state.execution_id,
                "request": state.original_request,
                "intermediate_results": {},
                "final_output": {},
                "status": "RUNNING",
                "errors": []
            }

            async with trace_workflow(
                workflow_name="Sourcing Workflow (via Master Supervisor)",
                inputs=state.original_request
            ) as span:
                result = await self.sourcing_workflow.run(
                    state=workflow_state,
                    org_id=uuid.UUID(state.organization_id),
                    user_id=uuid.UUID(state.user_id),
                    user_permissions=["candidate:read", "candidate:write", "recruitment:read", "ai:execute"]
                )
                
                state.workflow_result = result
                state.status = "COMPLETED" if result.get("status") == "COMPLETED" else result.get("status", "RUNNING")
                
                span.end(outputs={"status": state.status, "job_id": result.get("request", {}).get("job_id")})
                
        except Exception as exc:
            logger.error("Sourcing workflow execution failed", error=str(exc))
            state.errors.append(f"Sourcing workflow error: {str(exc)}")
            state.status = "FAILED"

        return state

    async def _node_execute_screening(self, state: MasterSupervisorState) -> MasterSupervisorState:
        """Execute Screening Workflow (placeholder for future implementation)."""
        state.status = "EXECUTING"
        logger.info("Screening workflow execution requested (not yet implemented)")
        state.workflow_result = {"status": "not_implemented"}
        return state

    async def _node_execute_interviews(self, state: MasterSupervisorState) -> MasterSupervisorState:
        """Execute Interview Workflow (placeholder for future implementation)."""
        state.status = "EXECUTING"
        logger.info("Interview workflow execution requested (not yet implemented)")
        state.workflow_result = {"status": "not_implemented"}
        return state

    async def _node_execute_offers(self, state: MasterSupervisorState) -> MasterSupervisorState:
        """Execute Offers Workflow (placeholder for future implementation)."""
        state.status = "EXECUTING"
        logger.info("Offers workflow execution requested (not yet implemented)")
        state.workflow_result = {"status": "not_implemented"}
        return state

    async def _node_hitl_gate(self, state: MasterSupervisorState) -> MasterSupervisorState:
        """
        Node: Check if human-in-the-loop approval is required.
        """
        if state.status == "FAILED":
            return state

        classification = state.intent_classification
        if not classification or not classification.requires_hitl:
            return state

        # Create HITL gate
        try:
            hitl_res = await self.hitl_manager.check_and_create_hitl_gate(
                execution_id=uuid.UUID(state.execution_id),
                agent_id=uuid.UUID(state.intent_classification.domain.value),
                requested_by=uuid.UUID(state.user_id),
                action_name=f"Approve {classification.domain.value.title()} Workflow",
                risk_level=classification.risk_level,
                request_data=state.original_request,
                reason=f"Requires human approval: {classification.reasoning}"
            )
            
            state.hitl_request = hitl_res
            state.status = "WAITING_HITL"
            
            logger.info("HITL gate created", domain=classification.domain, risk_level=classification.risk_level)
            
        except Exception as exc:
            logger.error("HITL gate creation failed", error=str(exc))
            state.errors.append(f"HITL gate error: {str(exc)}")

        return state

    def _check_hitl_decision(self, state: MasterSupervisorState) -> str:
        """Determine HITL gate status."""
        if state.status == "WAITING_HITL":
            if state.human_decision:
                return "approved" if state.human_decision == "approved" else "rejected"
            return "pending"
        return "approved"

    async def _node_finalizer(self, state: MasterSupervisorState) -> MasterSupervisorState:
        """
        Node: Finalize execution and prepare response.
        """
        if state.status == "COMPLETED":
            logger.info(
                "Workflow execution completed successfully",
                domain=state.target_domain,
                execution_id=state.execution_id
            )
        elif state.status == "FAILED":
            logger.error(
                "Workflow execution failed",
                domain=state.target_domain,
                errors=state.errors
            )

        return state

    async def _node_error_handler(self, state: MasterSupervisorState) -> MasterSupervisorState:
        """Handle errors during workflow execution."""
        logger.error(
            "Master Supervisor error handling",
            status=state.status,
            errors=state.errors,
            execution_id=state.execution_id
        )
        state.status = "FAILED"
        return state

    def _parse_intent_classification(self, response: str) -> Dict[str, Any]:
        """Parse intent classification response from LLM."""
        try:
            # Try to extract JSON from response
            import json
            
            # Look for JSON in markdown code blocks
            if "```json" in response:
                json_text = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_text = response.split("```")[1].split("```")[0]
            else:
                json_text = response

            parsed = json.loads(json_text.strip())
            
            # Normalize domain value
            domain_str = str(parsed.get("domain", "sourcing")).lower()
            try:
                domain = WorkflowDomain(domain_str)
            except ValueError:
                domain = WorkflowDomain.SOURCING
            
            return {
                "domain": domain,
                "intent": parsed.get("intent", "Unknown intent"),
                "confidence": float(parsed.get("confidence", 0.7)),
                "requires_hitl": parsed.get("requires_hitl", False),
                "risk_level": parsed.get("risk_level", "LOW"),
                "reasoning": parsed.get("reasoning", "No reasoning provided"),
                "suggested_workflow": parsed.get("suggested_workflow", "default")
            }
        except (json.JSONDecodeError, KeyError, ValueError) as exc:
            logger.warning("Failed to parse intent classification response", error=str(exc))
            # Return safe default
            return {
                "domain": WorkflowDomain.SOURCING,
                "intent": "Unknown intent",
                "confidence": 0.5,
                "requires_hitl": False,
                "risk_level": "MEDIUM",
                "reasoning": "Failed to parse LLM response",
                "suggested_workflow": "default"
            }

    async def execute(
        self,
        organization_id: uuid.UUID,
        user_id: uuid.UUID,
        user_input: str,
        request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute Master Supervisor workflow.
        
        Args:
            organization_id: Organization UUID
            user_id: User UUID
            user_input: Natural language user input
            request_data: Structured request data
            
        Returns:
            Execution result with workflow output and status
        """
        execution_id = str(uuid.uuid4())
        
        # Create initial state
        initial_state = MasterSupervisorState(
            organization_id=str(organization_id),
            user_id=str(user_id),
            execution_id=execution_id,
            user_input=user_input,
            original_request=request_data
        )

        async with trace_workflow(
            workflow_name="Master Supervisor Orchestrator",
            inputs={"user_input": user_input, "request": request_data}
        ) as span:
            try:
                # Execute graph
                compiled_graph = self.graph.compile()
                
                # Since LangGraph is sync, we'll execute the nodes sequentially
                current_state = initial_state
                
                current_state = await self._node_intent_classifier(current_state)
                if current_state.status != "FAILED":
                    current_state = await self._node_risk_assessment(current_state)
                    current_state = await self._node_domain_router(current_state)
                    
                    # Route to domain executor
                    if current_state.target_domain == WorkflowDomain.SOURCING:
                        current_state = await self._node_execute_sourcing(current_state)
                    elif current_state.target_domain == WorkflowDomain.SCREENING:
                        current_state = await self._node_execute_screening(current_state)
                    elif current_state.target_domain == WorkflowDomain.INTERVIEWS:
                        current_state = await self._node_execute_interviews(current_state)
                    elif current_state.target_domain == WorkflowDomain.OFFERS:
                        current_state = await self._node_execute_offers(current_state)
                    else:
                        current_state = await self._node_error_handler(current_state)
                    
                    # HITL gate
                    current_state = await self._node_hitl_gate(current_state)
                    
                    # Finalizer
                    if current_state.status != "WAITING_HITL":
                        current_state = await self._node_finalizer(current_state)
                else:
                    current_state = await self._node_error_handler(current_state)

                # Prepare response
                response = {
                    "status": current_state.status,
                    "execution_id": execution_id,
                    "domain": current_state.target_domain.value if current_state.target_domain else None,
                    "workflow_result": current_state.workflow_result,
                    "hitl_request": current_state.hitl_request,
                    "errors": current_state.errors
                }

                span.end(outputs=response)
                return response

            except Exception as exc:
                logger.error("Master Supervisor execution failed", error=str(exc), execution_id=execution_id)
                span.end(error=exc)
                return {
                    "status": "FAILED",
                    "execution_id": execution_id,
                    "error": str(exc),
                    "errors": [str(exc)]
                }
