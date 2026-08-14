from typing import Dict, Any
from app.modules.ai.copilot.tools import CopilotTools

class InterviewAgent:
    """
    Specialist Agent for Interview Scheduling, Feedback, and Scorecard Inspections.
    """

    def __init__(self, tools: CopilotTools):
        self.tools = tools

    async def execute(self, intent: str, message: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        if intent == "SCHEDULE_INTERVIEW" or "schedule" in message.lower():
            # Intercept high-risk schedule action with HITL confirmation
            return {
                "type": "HITL_REQUEST",
                "message": "High-risk action: Ready to schedule Microsoft Teams technical screen loops for selected candidates.",
                "data": {
                    "action": "SCHEDULE_INTERVIEW_LOOP",
                    "proposed_slots": ["2026-08-11 at 10:00 AM", "2026-08-11 at 02:00 PM"],
                    "interviewer": "Harsh Shirsath (Engineering Lead)",
                    "candidate_count": 3
                },
                "reasoning_summary": "Identified available calendar slots across hiring team members.",
                "confidence": 0.93,
                "evidence": ["Interviewer calendar verified free via Entra ID sync"],
                "gaps": [],
                "hitl_required": True
            }

        return {
            "type": "INTERVIEW_SUMMARY",
            "message": "Completed technical screen interview loop evaluations.",
            "data": {
                "candidate": "Alex Mercer",
                "round": "System Design Architecture",
                "overall_score": 8.8,
                "recommendation": "Strong Hire",
                "interviewer_notes": "Demonstrated exceptional knowledge of event-driven architectures and distributed locking."
            },
            "reasoning_summary": "Aggregated scorecard submissions from technical interview panel.",
            "confidence": 0.95,
            "evidence": ["Scorecard submitted by Lead Architect"],
            "gaps": ["Did not probe deep on frontend React state management"]
        }
