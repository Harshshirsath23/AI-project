"""
Comprehensive tests for LangSmith AI Observability, Tracing, Debugging & Evaluation System.

Covers:
1. Configuration & Enabled/Disabled Toggles
2. Resilience & Fault-Tolerance (LangSmith outage / failure degradation)
3. Data Privacy, Credentials & PII Sanitization
4. Trace Metadata & Tag Standards
5. Correlation between PostgreSQL AI Execution and LangSmith Traces
6. HITL Event Tracing & Decision Correlation
7. Agent & Workflow Version Telemetry
8. Evaluation Manager & Metric Feedback Recording
"""

import pytest
import uuid
from unittest.mock import Mock, AsyncMock, patch

from app.core.config import Settings
from app.core.observability.privacy import (
    sanitize_payload, sanitize_string, sanitize_error_message, REDACTED_TEXT, REDACTED_PAYLOAD
)
from app.core.observability.context import (
    TraceContext, get_current_trace_context, update_trace_context, clear_trace_context
)
from app.core.observability.metadata import build_trace_metadata, build_trace_tags
from app.core.observability.langsmith import get_langsmith_client, get_langchain_tracer, is_langsmith_available
from app.core.observability.tracing import (
    TraceSpan, trace_span, trace_agent, trace_workflow, trace_tool, trace_rag, trace_hitl
)
from app.core.observability.decorators import (
    traceable_agent, traceable_workflow, traceable_tool, traceable_rag
)
from app.core.observability.evaluation import (
    EvaluationMetric, EvaluationScore, EvaluationManager
)
from app.modules.ai.models import AIExecution, ModelProvider, ExecutionStatus
from app.modules.ai.schemas import AIExecutionCreate, HITLRequest, HITLResponse
from app.modules.ai.service import ExecutionService, KnowledgeService, RetrievalRequest


from sqlalchemy.ext.asyncio import AsyncSession


# ==================== Fixtures ====================

@pytest.fixture
def mock_db():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def sample_org_id():
    return uuid.uuid4()


@pytest.fixture
def sample_execution_data():
    return AIExecutionCreate(
        agent_id=uuid.uuid4(),
        input_data={"resume_text": "Sample resume for observability test"}
    )


# ==================== 1. Configuration & Toggle Tests ====================

class TestObservabilityConfig:
    """Test suite for LangSmith configuration logic."""

    def test_disabled_by_default_when_no_api_key(self):
        s = Settings(LANGSMITH_TRACING=True, LANGSMITH_API_KEY="")
        assert s.is_langsmith_enabled is False

    def test_disabled_when_tracing_flag_false(self):
        s = Settings(LANGSMITH_TRACING=False, LANGSMITH_API_KEY="ls__test_key")
        assert s.is_langsmith_enabled is False

    def test_enabled_when_tracing_true_and_key_provided(self):
        s = Settings(LANGSMITH_TRACING=True, LANGSMITH_API_KEY="ls__test_key")
        assert s.is_langsmith_enabled is True

    def test_langsmith_available_returns_false_when_disabled(self):
        with patch("app.core.config.settings.LANGSMITH_TRACING", False):
            assert is_langsmith_available() is False


# ==================== 2. Privacy & PII Sanitization Tests ====================

class TestPrivacySanitizer:
    """Test suite for payload sanitization, credential scrubbing, and PII protection."""

    def test_scrub_sensitive_dict_keys(self):
        raw_dict = {
            "username": "recruiter1",
            "password": "SuperSecretPassword123!",
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.secret",
            "api_key": "sk_test_123456789012345678",
            "candidate_notes": "Great profile"
        }
        sanitized = sanitize_payload(raw_dict)
        assert sanitized["password"] == REDACTED_TEXT
        assert sanitized["access_token"] == REDACTED_TEXT
        assert sanitized["api_key"] == REDACTED_TEXT
        assert sanitized["username"] == "recruiter1"

    def test_scrub_pii_emails_and_phones_in_strings(self):
        text = "Contact candidate John Doe at john.doe@example.com or +1-555-019-2834."
        sanitized = sanitize_string(text)
        assert "john.doe@example.com" not in sanitized
        assert "[REDACTED_EMAIL]" in sanitized
        assert "+1-555-019-2834" not in sanitized
        assert "[REDACTED_PHONE]" in sanitized

    def test_capture_content_disabled_returns_redacted_payload(self):
        payload = {"resume": "Very long candidate resume content..."}
        result = sanitize_payload(payload, capture_content=False)
        assert result == REDACTED_PAYLOAD

    def test_sanitize_error_message(self):
        err = Exception("Database auth failed for user admin with token eyJhbGciOiJIUzI1NiJ9...")
        sanitized = sanitize_error_message(err)
        assert "eyJhbGciOiJIUzI1NiJ9" not in sanitized
        assert REDACTED_TEXT in sanitized


# ==================== 3. Trace Context & Metadata Tests ====================

class TestTraceContextAndMetadata:
    """Test suite for ContextVar state propagation and metadata standards."""

    def test_context_update_and_retrieval(self):
        clear_trace_context()
        org_id = uuid.uuid4()
        agent_id = uuid.uuid4()

        update_trace_context(organization_id=org_id, agent_id=agent_id, agent_version=2)
        ctx = get_current_trace_context()

        assert ctx.organization_id == str(org_id)
        assert ctx.agent_id == str(agent_id)
        assert ctx.agent_version == 2

    def test_build_trace_metadata_includes_standard_fields(self):
        clear_trace_context()
        org_id = str(uuid.uuid4())
        update_trace_context(organization_id=org_id, feature_name="candidate_screening")

        meta = build_trace_metadata(extra_metadata={"custom_key": "val"})
        assert meta["organization_id"] == org_id
        assert meta["feature_name"] == "candidate_screening"
        assert meta["custom_key"] == "val"
        assert "platform" in meta

    def test_build_trace_tags(self):
        clear_trace_context()
        update_trace_context(feature_name="resume_parser")
        tags = build_trace_tags(extra_tags=["test_tag"])
        assert "feature:resume_parser" in tags
        assert "test_tag" in tags


# ==================== 4. Resilience & Outage Degradation Tests ====================

class TestResilienceAndFaultTolerance:
    """Verify that LangSmith errors/outages NEVER fail application execution."""

    @pytest.mark.asyncio
    async def test_trace_span_suppresses_langsmith_connection_errors(self):
        with patch("app.core.observability.tracing.get_langsmith_client", side_effect=Exception("LangSmith API Down")):
            # Tracing span should NOT raise exception even if client crashes
            async with trace_span(name="Test Faulty Span", run_type="chain") as span:
                result = 42
            assert result == 42

    @pytest.mark.asyncio
    async def test_traceable_agent_decorator_resilient_to_telemetry_failure(self):
        @traceable_agent(agent_name="Resilient Agent")
        async def sample_agent_task(x: int) -> int:
            return x * 2

        with patch("app.core.observability.tracing.get_langsmith_client", side_effect=RuntimeError("Timeout")):
            res = await sample_agent_task(21)
            assert res == 42


# ==================== 5. Database Execution Correlation Tests ====================

class TestExecutionCorrelation:
    """Verify PostgreSQL AIExecution and LangSmith trace correlation."""

    @pytest.mark.asyncio
    async def test_execution_creation_correlates_trace_id(self, mock_db, sample_org_id, sample_execution_data):
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()

        service = ExecutionService(mock_db)
        mock_execution = Mock(id=uuid.uuid4(), organization_id=sample_org_id, agent_id=sample_execution_data.agent_id)
        service.execution_repo.create_execution = AsyncMock(return_value=mock_execution)
        service.agent_repo.get_agent_by_id = AsyncMock(return_value=Mock(model_provider=ModelProvider.OPENAI, model_name="gpt-4", current_version=1))

        # Set mock active trace context
        clear_trace_context()
        fake_trace_id = str(uuid.uuid4())
        update_trace_context(trace_id=fake_trace_id)

        result = await service.create_execution(sample_org_id, sample_execution_data)
        assert result["status"] == "success"
        assert result["langsmith_trace_id"] == fake_trace_id


# ==================== 6. HITL Telemetry Tests ====================

class TestHITLTelemetry:
    """Verify HITL event tracing and decision correlation."""

    @pytest.mark.asyncio
    async def test_request_hitl_emits_telemetry_and_updates_status(self, mock_db, sample_org_id):
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        exec_id = uuid.uuid4()
        agent_id = uuid.uuid4()

        mock_exec = Mock(id=exec_id, organization_id=sample_org_id, agent_id=agent_id)
        mock_hitl = Mock(id=uuid.uuid4())

        service = ExecutionService(mock_db)
        service.execution_repo.get_execution_by_id = AsyncMock(return_value=mock_exec)
        service.execution_repo.update_execution_status = AsyncMock()
        service.hitl_repo.create_hitl_state = AsyncMock(return_value=mock_hitl)

        hitl_req = HITLRequest(
            execution_id=exec_id,
            reason="High risk candidate status change",
            timeout_minutes=30,
            request_data={"candidate_id": "c123"}
        )

        res = await service.request_hitl(exec_id, hitl_req)
        assert res["status"] == "success"
        assert "hitl_id" in res
        service.execution_repo.update_execution_status.assert_called_with(exec_id, ExecutionStatus.WAITING_HITL)


# ==================== 7. Evaluation Manager Tests ====================

class TestEvaluationFramework:
    """Test suite for evaluation metric calculations and feedback recording."""

    def test_record_feedback_degrades_gracefully_when_disabled(self):
        with patch("app.core.config.settings.LANGSMITH_TRACING", False):
            success = EvaluationManager.record_feedback(
                run_id="run-123",
                metric=EvaluationMetric.CORRECTNESS,
                score=0.95,
                comment="Accurate output"
            )
            assert success is False

    def test_evaluate_structured_output_validity(self):
        output = {"name": "John", "skills": ["Python", "SQL"]}
        res = EvaluationManager.evaluate_structured_output_validity(output, ["name", "skills", "experience"])
        assert res.metric == EvaluationMetric.STRUCTURED_OUTPUT_VALIDITY
        assert res.score == 2 / 3
        assert "experience" in res.comment

    def test_evaluate_retrieval_quality(self):
        docs = [{"chunk": "content1"}, {"chunk": "content2"}]
        res = EvaluationManager.evaluate_retrieval_quality(docs, min_expected_docs=2)
        assert res.score == 1.0
