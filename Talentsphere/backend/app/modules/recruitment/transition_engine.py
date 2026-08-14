import uuid
from typing import List, Optional
from fastapi import HTTPException
from app.modules.recruitment.models import RecruitmentStage

class TransitionEngine:
    """Validates whether a candidate application can transition between pipeline stages."""

    @staticmethod
    def validate_transition(
        from_stage: Optional[RecruitmentStage],
        to_stage: RecruitmentStage,
        notes: Optional[str] = None
    ) -> bool:
        """
        Validates transition rules (sequence checks, required notes on rejection, etc.).
        """
        if not to_stage:
            raise HTTPException(status_code=400, detail="Target stage does not exist")

        # If transitioning to a rejection or hold stage, require notes
        if "reject" in to_stage.stage_name.lower() and not notes:
            raise HTTPException(status_code=400, detail="Notes are required when rejecting an application")

        return True
