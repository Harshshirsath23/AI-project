import uuid
from typing import Dict, Any, Literal
from sqlalchemy.ext.asyncio import AsyncSession
from langgraph.graph import StateGraph, START, END

from app.modules.ai.copilot.state import CopilotState
from app.modules.ai.copilot.validators import CopilotValidator
from app.modules.ai.copilot.tools import CopilotTools
from app.modules.ai.copilot.agents.supervisor import CopilotSupervisor
from app.modules.ai.copilot.agents.candidate_agent import CandidateAgent
from app.modules.ai.copilot.agents.recruitment_agent import RecruitmentAgent
from app.modules.ai.copilot.agents.interview_agent import InterviewAgent
from app.modules.ai.copilot.agents.communication_agent import CommunicationAgent
from app.modules.ai.copilot.agents.analytics_agent import AnalyticsAgent

class CopilotWorkflowBuilder:
    """
    Builds the LangGraph for the AI Recruitment Copilot.
    """
    
    def __init__(self, db: AsyncSession, org_id: uuid.UUID):
        self.db = db
        self.org_id = org_id
        self.tools = CopilotTools(db, org_id)
        
    def build_graph(self):
        builder = StateGraph(CopilotState)
        
        # Define Nodes
        builder.add_node("validate_input", self._validate_input_node)
        builder.add_node("supervisor", self._supervisor_node)
        builder.add_node("candidate_agent", self._candidate_agent_node)
        builder.add_node("recruitment_agent", self._recruitment_agent_node)
        builder.add_node("interview_agent", self._interview_agent_node)
        builder.add_node("communication_agent", self._communication_agent_node)
        builder.add_node("analytics_agent", self._analytics_agent_node)
        builder.add_node("hitl_gate", self._hitl_gate_node)
        builder.add_node("nemotron_reasoning", self._nemotron_reasoning_node)
        
        # Define Edges
        builder.add_edge(START, "validate_input")
        builder.add_edge("validate_input", "supervisor")
        
        # Conditional routing from supervisor
        builder.add_conditional_edges("supervisor", self._route_from_supervisor)
        
        # Edges from specialists to reasoning
        for agent in ["candidate_agent", "recruitment_agent", "interview_agent", "communication_agent", "analytics_agent"]:
            builder.add_edge(agent, "nemotron_reasoning")
            
        # Conditional routing from reasoning (HITL vs END)
        builder.add_conditional_edges("nemotron_reasoning", self._route_after_reasoning)
        
        builder.add_edge("hitl_gate", END)
        
        return builder.compile()

    async def _validate_input_node(self, state: CopilotState) -> dict:
        user_msg = CopilotValidator.validate_user_input(state.get("user_message", ""))
        user_msg = CopilotValidator.sanitize_pii(user_msg)
        return {"user_message": user_msg}

    async def _supervisor_node(self, state: CopilotState) -> dict:
        intent_data = CopilotSupervisor.classify_intent(state["user_message"])
        return {
            "intent": intent_data["intent"],
            "intent_confidence": intent_data["confidence"],
            "metadata": {"domain": intent_data["domain"]}
        }

    def _route_from_supervisor(self, state: CopilotState) -> str:
        domain = state.get("metadata", {}).get("domain", "candidate")
        return f"{domain}_agent"

    async def _candidate_agent_node(self, state: CopilotState) -> dict:
        agent = CandidateAgent(self.tools)
        result = await agent.execute(state["intent"], state["user_message"], state.get("entities", {}))
        return {"final_response": result}

    async def _recruitment_agent_node(self, state: CopilotState) -> dict:
        agent = RecruitmentAgent(self.tools)
        result = await agent.execute(state["intent"], state["user_message"], state.get("entities", {}))
        return {"final_response": result}

    async def _interview_agent_node(self, state: CopilotState) -> dict:
        agent = InterviewAgent(self.tools)
        result = await agent.execute(state["intent"], state["user_message"], state.get("entities", {}))
        return {"final_response": result}

    async def _communication_agent_node(self, state: CopilotState) -> dict:
        agent = CommunicationAgent(self.tools)
        result = await agent.execute(state["intent"], state["user_message"], state.get("entities", {}))
        return {"final_response": result}

    async def _analytics_agent_node(self, state: CopilotState) -> dict:
        agent = AnalyticsAgent(self.tools)
        result = await agent.execute(state["intent"], state["user_message"], state.get("entities", {}))
        return {"final_response": result}

    async def _nemotron_reasoning_node(self, state: CopilotState) -> dict:
        # In a full implementation, we'd pass state to Nemotron 3 Ultra to synthesize the result
        # For now, we take the result from the agent execution
        res = state.get("final_response", {})
        hitl = res.get("hitl_required", False)
        
        return {
            "reasoning": res.get("reasoning_summary", "Execution completed via deterministic fallback."),
            "response_type": "HITL_REQUEST" if hitl else res.get("type", "TEXT"),
            "hitl_request": res.get("data") if hitl else None
        }

    def _route_after_reasoning(self, state: CopilotState) -> str:
        if state.get("response_type") == "HITL_REQUEST":
            return "hitl_gate"
        return END

    async def _hitl_gate_node(self, state: CopilotState) -> dict:
        # Halt execution, state saved in DB. Pending human approval.
        return {"status": "hitl_blocked"}


class CopilotWorkflowRunner:
    """
    Wrapper to execute the compiled LangGraph.
    """
    def __init__(self, db: AsyncSession, org_id: uuid.UUID):
        self.db = db
        self.org_id = org_id
        self.builder = CopilotWorkflowBuilder(db, org_id)
        self.graph = self.builder.build_graph()

    async def run(self, state: CopilotState) -> CopilotState:
        # Run graph
        final_state = await self.graph.ainvoke(state)
        return final_state
