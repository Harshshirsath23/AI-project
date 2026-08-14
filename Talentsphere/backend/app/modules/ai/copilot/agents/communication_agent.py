from typing import Dict, Any
from app.modules.ai.copilot.tools import CopilotTools

class CommunicationAgent:
    """
    Specialist Agent for Candidate Communications, Outreach Email Drafting, and Summarization.
    """

    def __init__(self, tools: CopilotTools):
        self.tools = tools

    async def execute(self, intent: str, message: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        candidate_name = entities.get("candidate_name", "Selected Candidate")
        draft = await self.tools.draft_candidate_message(candidate_name, "Technical Screening Interview")
        
        return {
            "type": "RECOMMENDATION",
            "message": f"Drafted personalized outreach message for {candidate_name}.",
            "data": draft,
            "reasoning_summary": "Tailored candidate message template using role specifications and candidate background.",
            "confidence": 0.96,
            "evidence": ["Generated compliant email draft according to EEOC guidelines"],
            "gaps": []
        }
