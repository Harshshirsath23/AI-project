from typing import Dict, Any

class WorkflowRulesEngine:
    """Evaluates configurable business rules for stage transitions."""

    @staticmethod
    def evaluate_stage_rules(stage_name: str, candidate_score: float = 80.0) -> Dict[str, Any]:
        """
        Evaluates dynamic stage rules (e.g., Screening Minimum Score > 70).
        """
        rules_passed = True
        reason = "All workflow stage rules passed"

        if "screening" in stage_name.lower() and candidate_score < 70.0:
            rules_passed = False
            reason = f"Candidate score ({candidate_score}) is below the required Screening threshold of 70.0"

        return {
            "rules_passed": rules_passed,
            "reason": reason,
            "evaluated_score": candidate_score
        }
