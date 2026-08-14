import uuid
from typing import Dict, Any

class AutomationHookDispatcher:
    """
    Event dispatcher for workflow stage transitions.
    In Milestone 6, this serves as the foundational integration layer for future 
    LangGraph AI Supervisor and subagents (e.g. AI Resume Parser, Ranking Agent, Compensation Advisor).
    """

    @staticmethod
    async def dispatch_stage_hook(
        application_id: uuid.UUID,
        from_stage_id: uuid.UUID | None,
        to_stage_id: uuid.UUID,
        stage_name: str
    ) -> Dict[str, Any]:
        """
        Dispatches an event payload for LangGraph agents to consume asynchronously.
        """
        event_type = f"RECRUITMENT_STAGE_ENTERED_{stage_name.upper().replace(' ', '_')}"
        
        # Payload structured specifically for LangGraph supervisor subscription
        payload = {
            "event_type": event_type,
            "application_id": str(application_id),
            "from_stage_id": str(from_stage_id) if from_stage_id else None,
            "to_stage_id": str(to_stage_id),
            "stage_name": stage_name,
            "status": "HOOK_DISPATCHED_TO_LANGGRAPH",
            "subscribed_agents": [
                "AI_Resume_Parser_Agent",
                "Candidate_Matching_Agent",
                "Ranking_Agent"
            ]
        }
        return payload
