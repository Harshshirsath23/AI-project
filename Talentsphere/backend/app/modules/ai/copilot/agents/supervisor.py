from typing import Dict, Any, Optional
from enum import Enum
import structlog
from langgraph.graph import StateGraph, END

from app.modules.ai.copilot.state import CopilotState
from app.modules.ai.engine.state import AgentExecutionStateDict
from app.modules.ai.engine.llm import LLMService, LLMProvider

logger = structlog.get_logger(__name__)


class SubgraphType(str, Enum):
    """Domain subgraph types for routing."""
    SOURCING = "sourcing"
    SCREENING = "screening"
    INTERVIEW = "interview"
    OFFER = "offer"
    GENERAL = "general"


class WorkflowStage(str, Enum):
    """Workflow stages for routing decisions."""
    JD_GENERATION = "jd_generation"
    CANDIDATE_SOURCING = "candidate_sourcing"
    RESUME_SCREENING = "resume_screening"
    INTERVIEW_SCHEDULING = "interview_scheduling"
    OFFER_GENERATION = "offer_generation"
    COMPLETED = "completed"


class MasterSupervisor:
    """
    Central LangGraph Supervisor Orchestrator.
    
    Routes workflow execution to appropriate domain subgraphs based on:
    - Workflow type and stage
    - Input data characteristics
    - LLM-based intent classification
    - Business logic rules
    """

    def __init__(self, llm_service: Optional[LLMService] = None):
        self.llm_service = llm_service or LLMService(
            provider=LLMProvider.NEMOTRON, 
            model_name="nvidia/nemotron-3-ultra"
        )

    async def route_workflow(
        self, 
        state: AgentExecutionStateDict
    ) -> str:
        """
        Determine which subgraph should handle the current workflow execution.
        
        Args:
            state: Current workflow execution state
            
        Returns:
            Subgraph identifier for routing
        """
        request_data = state.get("request", {})
        workflow_type = request_data.get("workflow_type", "general")
        
        # Direct routing based on workflow type
        if workflow_type == "sourcing":
            return SubgraphType.SOURCING.value
        elif workflow_type == "screening":
            return SubgraphType.SCREENING.value
        elif workflow_type == "interview":
            return SubgraphType.INTERVIEW.value
        elif workflow_type == "offer":
            return SubgraphType.OFFER.value
        
        # Intelligent routing based on input data
        return await self._intelligent_route(state)

    async def _intelligent_route(self, state: AgentExecutionStateDict) -> str:
        """
        Use LLM to determine appropriate subgraph when workflow type is not explicit.
        """
        request_data = state.get("request", {})
        
        # Rule-based routing for common patterns
        if "job_id" in request_data and "candidate_id" not in request_data:
            return SubgraphType.SOURCING.value
        elif "candidate_id" in request_data and "job_id" in request_data:
            return SubgraphType.SCREENING.value
        elif "interview_id" in request_data:
            return SubgraphType.INTERVIEW.value
        elif "offer_id" in request_data or "salary" in request_data:
            return SubgraphType.OFFER.value
        
        # LLM-based routing for complex cases
        routing_prompt = self._build_routing_prompt(request_data)
        routing_decision = await self.llm_service.generate_response(
            system_prompt="You are a workflow routing expert. Determine which recruitment subgraph should handle this request.",
            user_input=routing_prompt,
            context={"default_route": SubgraphType.GENERAL.value}
        )
        
        # Parse LLM response and map to subgraph
        return self._parse_routing_response(routing_decision)

    def _build_routing_prompt(self, request_data: Dict[str, Any]) -> str:
        """Build prompt for LLM-based routing decision."""
        return f"""
        Analyze this recruitment workflow request and determine which subgraph should handle it:
        
        Available subgraphs:
        - sourcing: Job creation, JD generation, candidate discovery, job board publishing
        - screening: Resume parsing, candidate matching, skill assessment, bias detection
        - interview: Interview scheduling, question generation, transcript analysis
        - offer: Salary negotiation, offer letter generation, background checks
        
        Request data: {request_data}
        
        Respond with just the subgraph name (sourcing/screening/interview/offer/general).
        """

    def _parse_routing_response(self, response: str) -> str:
        """Parse LLM routing response and map to subgraph type."""
        response_lower = response.lower()
        
        if "sourcing" in response_lower:
            return SubgraphType.SOURCING.value
        elif "screening" in response_lower or "matching" in response_lower:
            return SubgraphType.SCREENING.value
        elif "interview" in response_lower:
            return SubgraphType.INTERVIEW.value
        elif "offer" in response_lower or "salary" in response_lower:
            return SubgraphType.OFFER.value
        
        return SubgraphType.GENERAL.value

    async def determine_next_stage(
        self, 
        state: AgentExecutionStateDict
    ) -> WorkflowStage:
        """
        Determine the next stage in the recruitment pipeline.
        
        Args:
            state: Current workflow execution state
            
        Returns:
            Next workflow stage
        """
        output_data = state.get("output_data", {})
        intermediate_results = state.get("intermediate_results", {})
        
        # Stage determination based on completed work
        if "job_description" in output_data or "optimized_jd" in intermediate_results:
            return WorkflowStage.CANDIDATE_SOURCING
        elif "ranked_candidates" in intermediate_results or "candidates_shortlisted" in output_data:
            return WorkflowStage.RESUME_SCREENING
        elif "interview_questions" in output_data or "interview_analysis" in output_data:
            return WorkflowStage.OFFER_GENERATION
        elif "offer_letter" in output_data or "offer_details" in output_data:
            return WorkflowStage.COMPLETED
        
        # Default to JD generation if starting fresh
        return WorkflowStage.JD_GENERATION


class CopilotSupervisor:
    """
    Copilot Intent Classifier for conversational AI interactions.
    Determines intent and dispatches execution to specialist domain agents.
    """

    @staticmethod
    def classify_intent(user_message: str) -> Dict[str, Any]:
        """Classifies intent category and specific intent string."""
        msg = user_message.lower()
        
        if any(w in msg for w in ["find", "search", "candidate", "engineer", "resume", "compare", "experience", "skill"]):
            if "compare" in msg:
                return {"intent": "COMPARE_CANDIDATES", "domain": "candidate", "confidence": 0.96}
            return {"intent": "SEARCH_CANDIDATES", "domain": "candidate", "confidence": 0.95}
            
        elif any(w in msg for w in ["job", "pipeline", "requisition", "stage", "move", "shortlist"]):
            if "pipeline" in msg or "stage" in msg:
                return {"intent": "GET_PIPELINE", "domain": "recruitment", "confidence": 0.94}
            return {"intent": "GET_JOB", "domain": "recruitment", "confidence": 0.93}
            
        elif any(w in msg for w in ["schedule", "interview", "scorecard", "feedback", "calendar", "slot"]):
            if "schedule" in msg:
                return {"intent": "SCHEDULE_INTERVIEW", "domain": "interview", "confidence": 0.95}
            return {"intent": "GET_FEEDBACK", "domain": "interview", "confidence": 0.92}
            
        elif any(w in msg for w in ["draft", "message", "invitation", "email", "contact", "reach out"]):
            return {"intent": "DRAFT_MESSAGE", "domain": "communication", "confidence": 0.94}
            
        elif any(w in msg for w in ["metric", "analytics", "bottleneck", "velocity", "conversion", "time-to-hire"]):
            return {"intent": "HIRING_METRICS", "domain": "analytics", "confidence": 0.96}
            
        elif any(w in msg for w in ["policy", "document", "eeoc", "rule", "guideline"]):
            return {"intent": "KNOWLEDGE_SEARCH", "domain": "rag", "confidence": 0.91}
            
        return {"intent": "SEARCH_CANDIDATES", "domain": "candidate", "confidence": 0.85}
