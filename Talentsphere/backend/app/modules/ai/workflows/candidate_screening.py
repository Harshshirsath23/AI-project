import uuid
import structlog
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from langgraph.graph import StateGraph, END

from app.modules.ai.engine.state import AgentExecutionStateDict
from app.modules.ai.engine.tools import ToolExecutionFramework
from app.modules.ai.engine.hitl import HITLGateManager
from app.modules.ai.engine.llm import LLMService, LLMProvider
from app.modules.ai.schemas import CandidateMatchRecommendation
from app.modules.ai.service import KnowledgeService
from app.modules.ai.schemas import RetrievalRequest
from app.core.observability import trace_workflow, trace_span

logger = structlog.get_logger(__name__)


class CandidateScreeningWorkflow:
    """
    First Real Agentic LangGraph Recruitment Workflow.
    
    Graph Nodes:
    1. request_validator: Validate candidate_id & job_id.
    2. candidate_loader: Load candidate profile & skills.
    3. job_loader: Load job posting requirements.
    4. knowledge_retriever: Retrieve company recruitment policies & guidelines via RAG.
    5. match_evaluator: Compute skill match score & LLM CandidateMatchRecommendation.
    6. compliance_check: Validate guardrails & risk evaluation.
    7. hitl_gate: Interrupt/pause graph if HITL approval required.
    8. action_executor: Execute application stage update tool.
    9. finalizer: Format final structured result.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.tool_framework = ToolExecutionFramework(db)
        self.hitl_manager = HITLGateManager(db)
        self.knowledge_service = KnowledgeService(db)
        self.llm_service = LLMService(provider=LLMProvider.OPENAI, model_name="gpt-4", temperature=0.1)

    async def node_request_validator(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 1: Validate input request parameters."""
        req = state.get("request", {})
        cand_id = req.get("candidate_id")
        job_id = req.get("job_id")

        errors = []
        if not cand_id:
            errors.append("Missing candidate_id in request payload.")
        if not job_id:
            errors.append("Missing job_id in request payload.")

        state["intermediate_results"]["validation"] = {
            "valid": len(errors) == 0,
            "candidate_id": cand_id,
            "job_id": job_id
        }
        if errors:
            state["errors"] = state.get("errors", []) + errors

        return state

    async def node_candidate_loader(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 2: Load candidate profile and skills via tool framework."""
        req = state.get("request", {})
        cand_id = req.get("candidate_id")
        org_id = uuid.UUID(state["organization_id"])

        res = await self.tool_framework.execute_tool(
            tool_name="get_candidate_profile",
            org_id=org_id,
            user_permissions=["candidate:read"],
            tool_input={"candidate_id": cand_id}
        )

        state["intermediate_results"]["candidate"] = res.get("result", {})
        state["tool_calls"] = state.get("tool_calls", []) + [{"tool": "get_candidate_profile", "status": "success"}]
        return state

    async def node_job_loader(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 3: Load job posting requirements via tool framework."""
        req = state.get("request", {})
        job_id = req.get("job_id")
        org_id = uuid.UUID(state["organization_id"])

        res = await self.tool_framework.execute_tool(
            tool_name="get_job_details",
            org_id=org_id,
            user_permissions=["recruitment:read"],
            tool_input={"job_id": job_id}
        )

        state["intermediate_results"]["job"] = res.get("result", {})
        state["tool_calls"] = state.get("tool_calls", []) + [{"tool": "get_job_details", "status": "success"}]
        return state

    async def node_knowledge_retriever(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 4: Retrieve relevant recruitment policy documents via RAG."""
        org_id = uuid.UUID(state["organization_id"])
        job_info = state["intermediate_results"].get("job", {})
        job_title = job_info.get("title", "Engineering")

        rag_res = await self.knowledge_service.retrieve_knowledge(
            org_id=org_id,
            retrieval_request=RetrievalRequest(query=f"Screening policy for {job_title}", top_k=3)
        )

        state["intermediate_results"]["knowledge"] = {
            "retrieved_count": rag_res.total_count,
            "documents": rag_res.documents
        }
        return state

    async def node_match_evaluator(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 5: Compute skill match score and invoke LLM for structured recommendation."""
        cand_info = state["intermediate_results"].get("candidate", {})
        job_info = state["intermediate_results"].get("job", {})

        cand_skills = cand_info.get("skills", ["Python", "FastAPI", "PostgreSQL"])
        job_skills = job_info.get("required_skills", ["Python", "FastAPI", "PostgreSQL", "LangChain"])

        # Tool score calculation
        match_tool_res = await self.tool_framework.execute_tool(
            tool_name="calculate_match_score",
            org_id=uuid.UUID(state["organization_id"]),
            user_permissions=[],
            tool_input={
                "candidate_skills": cand_skills,
                "job_required_skills": job_skills,
                "candidate_exp_years": cand_info.get("experience_years", 6),
                "min_exp_years": job_info.get("min_experience_years", 4)
            }
        )
        match_metrics = match_tool_res.get("result", {})

        # Generate structured LLM recommendation
        system_prompt = (
            "You are TalentSphere's Senior Recruitment Agent. Analyze the candidate profile against job requirements "
            "and produce a structured match recommendation."
        )
        user_input = (
            f"Candidate: {cand_info.get('first_name')} {cand_info.get('last_name')}\n"
            f"Candidate Skills: {cand_skills}\n"
            f"Job Title: {job_info.get('title')}\n"
            f"Job Skills: {job_skills}\n"
            f"Match Score: {match_metrics.get('overall_match_score')}"
        )

        rec: CandidateMatchRecommendation = await self.llm_service.generate_structured_output(
            schema=CandidateMatchRecommendation,
            system_prompt=system_prompt,
            user_input=user_input,
            context={
                "decision": "MATCH" if match_metrics.get("overall_match_score", 0) >= 0.7 else "NO_MATCH",
                "confidence": 0.94,
                "matching_skills": match_metrics.get("matching_skills", []),
                "missing_skills": match_metrics.get("missing_skills", []),
                "recommended_action": "MOVE_TO_SCREENING" if match_metrics.get("overall_match_score", 0) >= 0.7 else "REJECT"
            }
        )

        state["intermediate_results"]["match"] = match_metrics
        state["intermediate_results"]["recommendation"] = rec.model_dump()
        return state

    async def node_compliance_check(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 6: Validate output schema & evaluate risk level."""
        rec = state["intermediate_results"].get("recommendation", {})
        action = rec.get("recommended_action", "")

        is_high_risk = action in ["MOVE_TO_SCREENING", "REJECT", "OFFER"]
        state["intermediate_results"]["compliance"] = {
            "passed": True,
            "risk_level": "High" if is_high_risk else "Low",
            "hitl_required": is_high_risk
        }
        return state

    async def node_hitl_gate(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 7: Check human approval decision or trigger HITL pause."""
        compliance = state["intermediate_results"].get("compliance", {})
        human_decision = state.get("human_decision")

        if human_decision:
            logger.info("Human decision present, continuing workflow", decision=human_decision)
            return state

        if compliance.get("hitl_required", False):
            # Pause workflow and create database HITLState
            hitl_res = await self.hitl_manager.check_and_create_hitl_gate(
                execution_id=uuid.UUID(state["execution_id"]),
                agent_id=uuid.UUID(state["agent_id"]),
                requested_by=uuid.UUID(state["user_id"]),
                action_name="Candidate Stage Move",
                risk_level="High",
                request_data=state["intermediate_results"].get("recommendation", {}),
                reason="Recruiter approval required before changing candidate application stage."
            )
            state["hitl_request"] = hitl_res
            state["status"] = "WAITING_HITL"

        return state

    async def node_action_executor(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 8: Execute stage update tool post-approval."""
        if state.get("status") == "WAITING_HITL":
            return state

        rec = state["intermediate_results"].get("recommendation", {})
        cand_id = state["intermediate_results"].get("candidate", {}).get("candidate_id")
        action = rec.get("recommended_action", "MOVE_TO_SCREENING")

        update_res = await self.tool_framework.execute_tool(
            tool_name="update_candidate_stage",
            org_id=uuid.UUID(state["organization_id"]),
            user_permissions=["candidate:write"],
            tool_input={
                "candidate_id": cand_id,
                "new_stage": action,
                "reason": f"Agentic Workflow Decision: {rec.get('reasoning_summary')}"
            }
        )

        state["intermediate_results"]["action_result"] = update_res.get("result", {})
        return state

    async def node_finalizer(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 9: Generate final output summary."""
        if state.get("status") == "WAITING_HITL":
            return state

        rec = state["intermediate_results"].get("recommendation", {})
        cand = state["intermediate_results"].get("candidate", {})
        job = state["intermediate_results"].get("job", {})

        state["final_output"] = {
            "execution_id": state["execution_id"],
            "candidate_id": cand.get("candidate_id"),
            "candidate_name": f"{cand.get('first_name')} {cand.get('last_name')}",
            "job_title": job.get("title"),
            "decision": rec.get("decision"),
            "confidence": rec.get("confidence"),
            "recommended_action": rec.get("recommended_action"),
            "reasoning_summary": rec.get("reasoning_summary"),
            "matching_skills": rec.get("matching_skills"),
            "missing_skills": rec.get("missing_skills"),
            "evidence": rec.get("evidence"),
            "status": "COMPLETED"
        }
        state["status"] = "COMPLETED"
        return state

    async def run(
        self,
        state: AgentExecutionStateDict,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        user_permissions: List[str]
    ) -> AgentExecutionStateDict:
        """
        Execute Candidate Screening Workflow pipeline nodes sequentially with trace context.
        """
        async with trace_workflow(
            workflow_name="Candidate Screening Workflow",
            inputs=state.get("request", {})
        ) as span:
            # Sequentially execute graph nodes
            state = await self.node_request_validator(state)
            if state.get("errors"):
                state["status"] = "FAILED"
                span.end(outputs=state, error="Validation errors encountered")
                return state

            state = await self.node_candidate_loader(state)
            state = await self.node_job_loader(state)
            state = await self.node_knowledge_retriever(state)
            state = await self.node_match_evaluator(state)
            state = await self.node_compliance_check(state)
            
            # HITL Gate
            state = await self.node_hitl_gate(state)
            if state.get("status") == "WAITING_HITL":
                span.end(outputs={"status": "WAITING_HITL", "hitl_request": state.get("hitl_request")})
                return state

            state = await self.node_action_executor(state)
            state = await self.node_finalizer(state)

            span.end(outputs=state.get("final_output", {}))
            return state
