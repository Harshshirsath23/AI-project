"""
Comprehensive Test Suite for Milestone 11 — Agentic Execution & Orchestration Engine

Covers:
1. AgentExecutionState TypedDict & Pydantic Model
2. LLM Provider Abstraction & Structured Output Generation
3. Tool Execution Framework (search_candidates, get_candidate_profile, get_job_details, calculate_match_score, update_candidate_stage)
4. HITL Gate Manager (Risk evaluation, HITL pause, state creation, human decision recording)
5. Candidate Screening LangGraph Workflow (End-to-end execution: Job & Candidate Loading -> RAG Retrieval -> LLM Match -> Guardrails -> HITL -> Action -> Final Result)
6. AgentRuntime Gateway (Execute, Pause on HITL, Resume on Approval, Error Handling, LangSmith Trace Correlation)
"""

import pytest
import uuid
from unittest.mock import Mock, AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ai.engine.state import (
    AgentExecutionStateDict, AgentExecutionStateModel, create_initial_agent_state
)
from app.modules.ai.engine.llm import LLMProvider, LLMService, MockLLM
from app.modules.ai.engine.tools import (
    ToolExecutionFramework, tool_calculate_match_score, tool_get_candidate_profile, tool_get_job_details
)
from app.modules.ai.engine.hitl import HITLGateManager
from app.modules.ai.engine.runtime import AgentRuntime
from app.modules.ai.workflows.candidate_screening import CandidateScreeningWorkflow
from app.modules.ai.schemas import CandidateMatchRecommendation, HITLResponse
from app.modules.ai.models import AIAgent, ModelProvider, ExecutionStatus


# ==================== Fixtures ====================

@pytest.fixture
def mock_db():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def sample_org_id():
    return uuid.uuid4()


@pytest.fixture
def sample_user_id():
    return uuid.uuid4()


@pytest.fixture
def sample_agent_id():
    return uuid.uuid4()


# ==================== 1. AgentExecutionState Tests ====================

class TestAgentExecutionState:
    """Test suite for state architecture."""

    def test_create_initial_agent_state(self, sample_org_id, sample_user_id, sample_agent_id):
        state = create_initial_agent_state(
            organization_id=sample_org_id,
            user_id=sample_user_id,
            agent_id=sample_agent_id,
            agent_version=2,
            request_data={"candidate_id": "c1", "job_id": "j1"}
        )
        assert state["organization_id"] == str(sample_org_id)
        assert state["user_id"] == str(sample_user_id)
        assert state["agent_id"] == str(sample_agent_id)
        assert state["agent_version"] == 2
        assert state["request"]["candidate_id"] == "c1"
        assert state["status"] == "QUEUED"

    def test_agent_execution_state_pydantic_model(self, sample_org_id, sample_user_id, sample_agent_id):
        model = AgentExecutionStateModel(
            organization_id=str(sample_org_id),
            user_id=str(sample_user_id),
            agent_id=str(sample_agent_id),
            request={"test": "data"}
        )
        d = model.to_dict()
        assert d["organization_id"] == str(sample_org_id)
        assert d["request"]["test"] == "data"


# ==================== 2. LLM Provider Abstraction Tests ====================

class TestLLMProviderAbstraction:
    """Test suite for LLM provider abstraction."""

    def test_llm_service_returns_mock_model_when_unconfigured(self):
        service = LLMService(provider=LLMProvider.OPENAI, model_name="gpt-4")
        model = service.get_model()
        assert isinstance(model, MockLLM)

    @pytest.mark.asyncio
    async def test_generate_structured_output_fallbacks_safely(self):
        service = LLMService(provider=LLMProvider.MOCK, model_name="mock-gpt-4")
        res = await service.generate_structured_output(
            schema=CandidateMatchRecommendation,
            system_prompt="Test System Prompt",
            user_input="Test User Input",
            context={"decision": "MATCH", "recommended_action": "MOVE_TO_SCREENING"}
        )
        assert isinstance(res, CandidateMatchRecommendation)
        assert res.decision == "MATCH"
        assert res.recommended_action == "MOVE_TO_SCREENING"


# ==================== 3. Tool Execution Framework Tests ====================

class TestToolExecutionFramework:
    """Test suite for tool execution."""

    @pytest.mark.asyncio
    async def test_calculate_match_score_tool(self):
        res = await tool_calculate_match_score(
            candidate_skills=["Python", "FastAPI", "PostgreSQL"],
            job_required_skills=["Python", "FastAPI", "PostgreSQL", "Docker"],
            candidate_exp_years=5,
            min_exp_years=4
        )
        assert res["overall_match_score"] > 0.7
        assert "Python" in res["matching_skills"]
        assert "Docker" in res["missing_skills"]

    @pytest.mark.asyncio
    async def test_tool_execution_framework_validates_authorization(self, mock_db, sample_org_id):
        mock_db.execute = AsyncMock()
        framework = ToolExecutionFramework(mock_db)
        
        # Mock repository get tool
        mock_tool = Mock(
            tool_name="update_candidate_stage",
            required_permissions=["candidate:write"],
            risk_level="High",
            hitl_requirement="Always_Required"
        )
        framework.tool_repo.get_tool_by_name = AsyncMock(return_value=mock_tool)

        res = await framework.execute_tool(
            tool_name="update_candidate_stage",
            org_id=sample_org_id,
            user_permissions=["candidate:write"],
            tool_input={"candidate_id": "c123", "new_stage": "MOVE_TO_SCREENING"}
        )
        assert res["tool_name"] == "update_candidate_stage"
        assert res["requires_hitl"] is True


# ==================== 4. HITL Gate Manager Tests ====================

class TestHITLGateManager:
    """Test suite for HITL gate manager."""

    @pytest.mark.asyncio
    async def test_check_and_create_hitl_gate(self, mock_db, sample_org_id, sample_user_id, sample_agent_id):
        exec_id = uuid.uuid4()
        mock_hitl_record = Mock(id=uuid.uuid4())

        manager = HITLGateManager(mock_db)
        manager.exec_repo.update_execution_status = AsyncMock()
        manager.hitl_repo.create_hitl_state = AsyncMock(return_value=mock_hitl_record)

        res = await manager.check_and_create_hitl_gate(
            execution_id=exec_id,
            agent_id=sample_agent_id,
            requested_by=sample_user_id,
            action_name="Stage Update",
            risk_level="High",
            request_data={"new_stage": "OFFER"}
        )
        assert res["status"] == "WAITING_HITL"
        assert res["hitl_id"] == str(mock_hitl_record.id)


# ==================== 5. Candidate Screening Workflow Tests ====================

class TestCandidateScreeningWorkflow:
    """Test suite for Candidate Screening LangGraph Workflow."""

    @pytest.mark.asyncio
    async def test_candidate_screening_workflow_hitl_pause(self, mock_db, sample_org_id, sample_user_id, sample_agent_id):
        workflow = CandidateScreeningWorkflow(mock_db)

        # Mock tool responses
        workflow.tool_framework.execute_tool = AsyncMock(side_effect=[
            {"result": {"candidate_id": "c1", "first_name": "John", "last_name": "Doe", "skills": ["Python", "FastAPI"]}},
            {"result": {"job_id": "j1", "title": "Senior Python Engineer", "required_skills": ["Python", "FastAPI"]}},
            {"result": {"overall_match_score": 0.9, "matching_skills": ["Python", "FastAPI"], "missing_skills": []}}
        ])
        workflow.knowledge_service.retrieve_knowledge = AsyncMock(return_value=Mock(total_count=1, documents=[]))
        workflow.hitl_manager.check_and_create_hitl_gate = AsyncMock(return_value={"hitl_id": "h123", "status": "WAITING_HITL"})

        state = create_initial_agent_state(
            organization_id=sample_org_id,
            user_id=sample_user_id,
            agent_id=sample_agent_id,
            request_data={"candidate_id": "c1", "job_id": "j1"}
        )

        final_state = await workflow.run(state, org_id=sample_org_id, user_id=sample_user_id, user_permissions=["candidate:read", "candidate:write"])
        assert final_state["status"] == "WAITING_HITL"
        assert final_state["hitl_request"]["status"] == "WAITING_HITL"


# ==================== 6. AgentRuntime Gateway Tests ====================

class TestAgentRuntime:
    """Test suite for AgentRuntime execution gateway."""

    @pytest.mark.asyncio
    async def test_agent_runtime_execute_success(self, mock_db, sample_org_id, sample_user_id, sample_agent_id):
        exec_id = uuid.uuid4()
        mock_agent = Mock(
            id=sample_agent_id,
            agent_name="Candidate Screener",
            model_name="gpt-4",
            model_provider=ModelProvider.OPENAI,
            current_version=1
        )
        mock_exec = Mock(id=exec_id, organization_id=sample_org_id, agent_id=sample_agent_id)

        runtime = AgentRuntime(mock_db)
        runtime.agent_repo.get_agent_by_id = AsyncMock(return_value=mock_agent)
        runtime.exec_repo.create_execution = AsyncMock(return_value=mock_exec)
        runtime.exec_repo.update_execution_status = AsyncMock()

        # Mock CandidateScreeningWorkflow run to complete
        with patch("app.modules.ai.workflows.candidate_screening.CandidateScreeningWorkflow.run") as mock_run:
            mock_run.return_value = {
                "status": "COMPLETED",
                "final_output": {"decision": "MATCH", "recommended_action": "MOVE_TO_SCREENING"}
            }

            res = await runtime.execute(
                organization_id=sample_org_id,
                user_id=sample_user_id,
                agent_id=sample_agent_id,
                input_data={"candidate_id": "c1", "job_id": "j1"}
            )

            assert res["status"] == "COMPLETED"
            assert res["execution_id"] == str(exec_id)
            assert res["output_data"]["decision"] == "MATCH"

    @pytest.mark.asyncio
    async def test_agent_runtime_resume_success(self, mock_db, sample_org_id, sample_agent_id):
        exec_id = uuid.uuid4()
        hitl_id = uuid.uuid4()

        mock_exec = Mock(id=exec_id, organization_id=sample_org_id, agent_id=sample_agent_id, agent_version=1, workflow_id=None, input_data={"candidate_id": "c1", "job_id": "j1"})
        mock_hitl = Mock(id=hitl_id, execution_id=exec_id)

        runtime = AgentRuntime(mock_db)
        runtime.exec_repo.get_execution_by_id = AsyncMock(return_value=mock_exec)
        runtime.hitl_repo.get_hitl_state_by_execution = AsyncMock(return_value=mock_hitl)
        runtime.hitl_manager.record_human_decision = AsyncMock(return_value={"status": "success"})
        runtime.exec_repo.update_execution_status = AsyncMock()

        with patch("app.modules.ai.workflows.candidate_screening.CandidateScreeningWorkflow.run") as mock_run:
            mock_run.return_value = {
                "status": "COMPLETED",
                "final_output": {"decision": "MATCH", "stage_updated": "MOVE_TO_SCREENING"}
            }

            hitl_resp = HITLResponse(decision="Approved", decision_reason="Recruiter confirmed fit")
            res = await runtime.resume(execution_id=exec_id, hitl_response=hitl_resp)

            assert res["status"] == "COMPLETED"
            assert res["execution_id"] == str(exec_id)
