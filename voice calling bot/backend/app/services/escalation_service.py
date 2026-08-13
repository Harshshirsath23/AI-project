"""Call escalation service detecting customer handoff triggers and low confidence."""

import re
from typing import Tuple, Optional
from app.core.logging import get_logger

logger = get_logger(__name__)

ESCALATION_KEYWORDS = [
    r"\bhuman\b",
    r"\bagent\b",
    r"\bsupervisor\b",
    r"\brepresentative\b",
    r"\bmanager\b",
    r"\bperson\b",
    r"\breal person\b",
    r"\bcomplaint\b",
    r"\blawsuit\b",
    r"\bangry\b",
    r"\bfrustrated\b",
    r"\bstop calling\b",
    r"\btransfer me\b",
]

ESCALATION_PATTERN = re.compile("|".join(ESCALATION_KEYWORDS), re.IGNORECASE)


class EscalationService:
    """Service evaluating call escalation status and human routing."""

    @staticmethod
    def check_escalation_triggers(user_speech: str) -> Tuple[bool, Optional[str]]:
        """Check if customer speech contains escalation keywords or frustration signals."""
        if not user_speech:
            return False, None

        match = ESCALATION_PATTERN.search(user_speech)
        if match:
            trigger_word = match.group(0)
            logger.warning("Escalation trigger detected in speech", trigger=trigger_word)
            return True, f"Keyword trigger: '{trigger_word}'"

        return False, None

    @staticmethod
    def evaluate_confidence(confidence_score: float, threshold: float = 0.6) -> bool:
        """Evaluate if LLM or speech confidence falls below acceptable threshold."""
        return confidence_score < threshold

    @staticmethod
    async def trigger_call_escalation(call_id: str, lead_name: str = "there") -> str:
        """Perform escalation: mark call record in DB and return smooth handoff dialogue."""
        logger.info("Executing call escalation transfer", call_id=call_id)

        try:
            from app.database.connection import SessionLocal
            from app.models.call import Call

            with SessionLocal() as db:
                call_record = db.query(Call).filter(Call.id == call_id).first()
                if call_record:
                    call_record.status = "escalated"
                    db.commit()
        except Exception as e:
            logger.error("Failed to update call escalation status in DB", call_id=call_id, error=str(e))

        return f"I completely understand {lead_name}. I'm transferring your call to a representative right now. Please stay on the line."


escalation_service = EscalationService()
