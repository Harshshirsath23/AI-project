from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
import structlog

from app.core.config import settings
from app.core.observability.langsmith import get_langsmith_client
from app.core.observability.privacy import sanitize_payload

logger = structlog.get_logger(__name__)


class EvaluationMetric(str, Enum):
    CORRECTNESS = "Correctness"
    RELEVANCE = "Relevance"
    GROUNDEDNESS = "Groundedness"
    SAFETY = "Safety"
    POLICY_COMPLIANCE = "PolicyCompliance"
    STRUCTURED_OUTPUT_VALIDITY = "StructuredOutputValidity"
    TOOL_SELECTION = "ToolSelection"
    DECISION_QUALITY = "DecisionQuality"
    RETRIEVAL_QUALITY = "RetrievalQuality"


@dataclass
class EvaluationScore:
    metric: EvaluationMetric
    score: float  # Normalized 0.0 to 1.0
    comment: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class EvaluationManager:
    """
    Manages evaluation runs and feedback recording for LangSmith.
    Enables tracking of AI quality metrics across versions, models, and agents.
    """

    @staticmethod
    def record_feedback(
        run_id: str,
        metric: EvaluationMetric | str,
        score: float,
        comment: Optional[str] = None,
        correction: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Record evaluation score/feedback against a specific LangSmith run ID.
        Fails safely without raising exceptions if LangSmith is unavailable.
        """
        if not settings.is_langsmith_enabled:
            return False

        client = get_langsmith_client()
        if not client or not run_id:
            return False

        try:
            metric_key = metric.value if isinstance(metric, EvaluationMetric) else str(metric)
            sanitized_comment = sanitize_payload(comment) if comment else None
            sanitized_correction = sanitize_payload(correction) if correction else None

            client.create_feedback(
                run_id=run_id,
                key=metric_key,
                score=max(0.0, min(1.0, float(score))),
                comment=sanitized_comment,
                correction=sanitized_correction
            )
            logger.info(
                "LangSmith feedback recorded",
                run_id=run_id,
                metric=metric_key,
                score=score
            )
            return True
        except Exception as exc:
            logger.warning("Failed to submit feedback to LangSmith", error=str(exc), run_id=run_id)
            return False

    @staticmethod
    def evaluate_structured_output_validity(
        output_data: Dict[str, Any],
        required_schema_keys: List[str]
    ) -> EvaluationScore:
        """
        Deterministic evaluator for checking if AI output complies with required schema keys.
        """
        if not required_schema_keys:
            return EvaluationScore(
                metric=EvaluationMetric.STRUCTURED_OUTPUT_VALIDITY,
                score=1.0,
                comment="No schema keys specified."
            )

        present = [k for k in required_schema_keys if k in output_data]
        score = len(present) / len(required_schema_keys)
        missing = [k for k in required_schema_keys if k not in output_data]

        return EvaluationScore(
            metric=EvaluationMetric.STRUCTURED_OUTPUT_VALIDITY,
            score=score,
            comment=f"Missing keys: {missing}" if missing else "Valid schema",
            metadata={"missing_keys": missing, "present_keys": present}
        )

    @staticmethod
    def evaluate_retrieval_quality(
        retrieved_documents: List[Any],
        min_expected_docs: int = 1
    ) -> EvaluationScore:
        """
        Deterministic evaluator for document retrieval quality.
        """
        doc_count = len(retrieved_documents)
        if doc_count >= min_expected_docs:
            score = 1.0
        elif doc_count > 0:
            score = doc_count / min_expected_docs
        else:
            score = 0.0

        return EvaluationScore(
            metric=EvaluationMetric.RETRIEVAL_QUALITY,
            score=score,
            comment=f"Retrieved {doc_count} documents (min expected: {min_expected_docs})",
            metadata={"doc_count": doc_count}
        )
