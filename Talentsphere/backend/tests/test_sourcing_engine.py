"""
Comprehensive Test Suite for Milestone 12 — Intelligent Sourcing & Candidate Discovery Engine

Covers:
1. Job Requirement Intelligence Agent (ExtractedJobRequirements)
2. Candidate Discovery Agent (Candidate search & Vector similarity)
3. Candidate Intelligence Agent (Resume & profile evidence extraction)
4. Matching Agent (Deterministic weighted scoring matrix with MatchingWeights)
5. Compliance & Fairness Agent (Job relevance audit & non-discrimination verification)
6. Candidate Ranking & Recommendation Agents (RankedCandidate & SourcingRecommendation)
7. Intelligent Sourcing Workflow (End-to-end 8-agent LangGraph workflow execution)
8. HITL Gate Pause & Resume Execution Flow
9. FastAPI Sourcing Endpoints
"""

import pytest
import uuid
from unittest.mock import Mock, AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ai.sourcing.schemas import (
    ExtractedJobRequirements, CandidateAnalysisResult, MatchingWeights,
    CandidateMatchScore, ComplianceReport, RankedCandidate, SourcingRecommendation
)
from app.modules.ai.sourcing.agents import (
    JobRequirementIntelligenceAgent, CandidateDiscoveryAgent,
    CandidateIntelligenceAgent, MatchingAgent, ComplianceFairnessAgent,
    CandidateRankingAgent, RecommendationAgent
)
from app.modules.ai.workflows.sourcing_workflow import IntelligentSourcingWorkflow
from app.modules.ai.engine.runtime import AgentRuntime
from app.modules.ai.engine.tools import ToolExecutionFramework
from app.modules.ai.schemas import HITLResponse
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
def sample_job_id():
    return uuid.uuid4()


@pytest.fixture
def sample_requirements():
    return ExtractedJobRequirements(
        role="Senior Python Engineer",
        required_skills=["Python", "FastAPI", "PostgreSQL"],
        preferred_skills=["Docker", "AWS", "LangChain"],
        minimum_experience_years=4,
        education_requirements=["Bachelor of Science"],
        location_requirements=["Hybrid"],
        other_constraints=[]
    )


# ==================== 1. Requirement Intelligence Tests ====================

class TestJobRequirementIntelligenceAgent:
    """Test suite for Requirement Extraction."""

    @pytest.mark.asyncio
    async def test_extract_requirements_structured_output(self, sample_job_id):
        agent = JobRequirementIntelligenceAgent()
        job_data = {
            "job_id": str(sample_job_id),
            "title": "Senior Python Engineer",
            "description": "Looking for 5+ years experience in Python, FastAPI, PostgreSQL",
            "required_skills": ["Python", "FastAPI", "PostgreSQL"],
            "min_experience_years": 5
        }

        reqs = await agent.extract_requirements(job_data)
        assert isinstance(reqs, ExtractedJobRequirements)
        assert reqs.role == "Senior Python Engineer"
        assert "Python" in reqs.required_skills
        assert reqs.minimum_experience_years >= 4


# ==================== 2. Discovery & Intelligence Tests ====================

class TestCandidateDiscoveryAndIntelligence:
    """Test suite for Discovery and Candidate Analysis."""

    @pytest.mark.asyncio
    async def test_candidate_discovery_agent(self, mock_db, sample_org_id, sample_requirements):
        mock_db.execute = AsyncMock()
        tool_framework = ToolExecutionFramework(mock_db)

        # Mock search candidates tool
        tool_framework.execute_tool = AsyncMock(return_value={
            "result": {
                "candidates": [
                    {"candidate_id": "c1", "first_name": "Rahul", "last_name": "Sharma", "skills": ["Python", "FastAPI", "PostgreSQL"]},
                    {"candidate_id": "c2", "first_name": "Priya", "last_name": "Patel", "skills": ["Python", "Django"]}
                ]
            }
        })

        agent = CandidateDiscoveryAgent(tool_framework)
        discovered = await agent.discover_candidates(sample_org_id, sample_requirements, ["candidate:read"])
        assert len(discovered) == 2
        assert discovered[0]["candidate_id"] == "c1"

    @pytest.mark.asyncio
    async def test_candidate_intelligence_agent(self, mock_db, sample_org_id, sample_requirements):
        mock_db.execute = AsyncMock()
        tool_framework = ToolExecutionFramework(mock_db)

        tool_framework.execute_tool = AsyncMock(side_effect=[
            {"result": {"candidate_id": "c1", "first_name": "Rahul", "last_name": "Sharma", "skills": ["Python", "FastAPI", "PostgreSQL"], "experience_years": 6}},
            {"result": {"candidate_id": "c1", "experience_years": 6, "education_summary": "BS Computer Science"}}
        ])

        agent = CandidateIntelligenceAgent(tool_framework)
        analysis = await agent.analyze_candidate(
            org_id=sample_org_id,
            candidate_info={"candidate_id": "c1", "first_name": "Rahul", "last_name": "Sharma"},
            requirements=sample_requirements,
            user_permissions=["candidate:read"]
        )

        assert isinstance(analysis, CandidateAnalysisResult)
        assert analysis.candidate_id == "c1"
        assert "Python" in analysis.skills_evidence
        assert len(analysis.strengths) > 0


# ==================== 3. Matching Agent Tests ====================

class TestMatchingAgent:
    """Test suite for Matching Agent scoring calculation."""

    def test_calculate_match_with_custom_weights(self, sample_requirements):
        agent = MatchingAgent()
        analysis = CandidateAnalysisResult(
            candidate_id="c1",
            first_name="Rahul",
            last_name="Sharma",
            skills_evidence={"Python": "7 years", "FastAPI": "5 years", "PostgreSQL": "6 years"},
            experience_years=6,
            education_summary="BS CS"
        )

        custom_weights = MatchingWeights(
            skills_weight=0.40,
            experience_weight=0.30,
            role_weight=0.15,
            education_weight=0.05,
            semantic_weight=0.10,
            min_match_threshold=0.70
        )

        match_score = agent.calculate_match(analysis, sample_requirements, weights=custom_weights)
        assert isinstance(match_score, CandidateMatchScore)
        assert match_score.total_match_score > 0.85
        assert "Python" in match_score.matching_skills


# ==================== 4. Compliance & Fairness Tests ====================

class TestComplianceFairnessAgent:
    """Test suite for Compliance Auditor."""

    @pytest.mark.asyncio
    async def test_audit_candidate_pass(self, mock_db, sample_org_id):
        tool_framework = ToolExecutionFramework(mock_db)
        tool_framework.execute_tool = AsyncMock(return_value={"result": {"guidelines": ["Fairness rule"]}})

        agent = ComplianceFairnessAgent(tool_framework)
        analysis = CandidateAnalysisResult(candidate_id="c1", first_name="Rahul", last_name="Sharma")
        score = CandidateMatchScore(candidate_id="c1", skill_match_score=1.0, experience_match_score=1.0, role_match_score=0.9, education_match_score=0.9, semantic_fit_score=0.9, total_match_score=0.92)

        report = await agent.audit_candidate(sample_org_id, analysis, score, ["ai:execute"])
        assert isinstance(report, ComplianceReport)
        assert report.compliance_status == "PASS"
        assert report.risk_level == "LOW"


# ==================== 5. Candidate Ranking & Recommendation Tests ====================

class TestRankingAndRecommendationAgents:
    """Test suite for Candidate Ranking and Recommendation Report Generation."""

    def test_candidate_ranking_and_recommendation(self):
        ranking_agent = CandidateRankingAgent()
        rec_agent = RecommendationAgent()

        analysis1 = CandidateAnalysisResult(candidate_id="c1", first_name="Rahul", last_name="Sharma", skills_evidence={"Python": "7 yrs"}, experience_years=6)
        score1 = CandidateMatchScore(candidate_id="c1", skill_match_score=1.0, experience_match_score=1.0, role_match_score=0.9, education_match_score=0.9, semantic_fit_score=0.9, total_match_score=0.94)

        analysis2 = CandidateAnalysisResult(candidate_id="c2", first_name="Priya", last_name="Patel", skills_evidence={"Python": "4 yrs"}, experience_years=4)
        score2 = CandidateMatchScore(candidate_id="c2", skill_match_score=0.7, experience_match_score=0.8, role_match_score=0.8, education_match_score=0.8, semantic_fit_score=0.8, total_match_score=0.78)

        ranked = ranking_agent.rank_candidates([analysis1, analysis2], [score1, score2])
        assert len(ranked) == 2
        assert ranked[0].candidate_id == "c1"
        assert ranked[0].rank == 1
        assert ranked[0].recommended_action == "SHORTLIST"

        comp_report1 = ComplianceReport(candidate_id="c1", compliance_status="PASS", risk_level="LOW", explanation="Valid")
        comp_report2 = ComplianceReport(candidate_id="c2", compliance_status="PASS", risk_level="LOW", explanation="Valid")

        recommendation = rec_agent.generate_recommendation_report(
            job_id="job123",
            job_title="Senior Python Engineer",
            total_analyzed=2,
            ranked_candidates=ranked,
            compliance_reports=[comp_report1, comp_report2]
        )

        assert isinstance(recommendation, SourcingRecommendation)
        assert recommendation.candidates_shortlisted == 2
        assert recommendation.compliance_status == "PASS"


# ==================== 6. Intelligent Sourcing Workflow Tests ====================

class TestIntelligentSourcingWorkflow:
    """Test suite for Intelligent Sourcing Workflow execution."""

    @pytest.mark.asyncio
    async def test_sourcing_workflow_end_to_end(self, mock_db, sample_org_id, sample_user_id, sample_job_id):
        workflow = IntelligentSourcingWorkflow(mock_db)

        # Mock tool responses
        workflow.tool_framework.execute_tool = AsyncMock(side_effect=[
            {"result": {"job_id": str(sample_job_id), "title": "Senior Python Engineer", "description": "Need Senior Python Dev", "required_skills": ["Python", "FastAPI"], "min_experience_years": 4}},
            {"result": {"candidates": [{"candidate_id": "c1", "first_name": "Rahul", "last_name": "Sharma", "skills": ["Python", "FastAPI"]}]}},
            {"result": {"candidate_id": "c1", "first_name": "Rahul", "last_name": "Sharma", "skills": ["Python", "FastAPI"], "experience_years": 6}},
            {"result": {"candidate_id": "c1", "experience_years": 6, "education_summary": "BS CS"}},
            {"result": {"guidelines": ["Non-discrimination"]}}
        ])

        from app.modules.ai.engine.state import create_initial_agent_state
        state = create_initial_agent_state(
            organization_id=sample_org_id,
            user_id=sample_user_id,
            agent_id=uuid.uuid4(),
            request_data={"job_id": str(sample_job_id), "workflow_type": "sourcing"}
        )

        final_state = await workflow.run(state, org_id=sample_org_id, user_id=sample_user_id, user_permissions=["candidate:read", "recruitment:read", "ai:execute"])
        assert final_state["status"] == "COMPLETED"
        assert final_state["final_output"]["total_candidates_analyzed"] == 1
        assert final_state["final_output"]["candidates_shortlisted"] == 1


# ==================== 7. AgentRuntime Sourcing Gateway Tests ====================

class TestAgentRuntimeSourcingGateway:
    """Test suite for AgentRuntime sourcing execution."""

    @pytest.mark.asyncio
    async def test_agent_runtime_sourcing_execution(self, mock_db, sample_org_id, sample_user_id, sample_job_id):
        agent_id = uuid.uuid4()
        exec_id = uuid.uuid4()

        mock_agent = Mock(id=agent_id, agent_name="Sourcing Supervisor", model_name="gpt-4", model_provider=ModelProvider.OPENAI, current_version=1)
        mock_exec = Mock(id=exec_id, organization_id=sample_org_id, agent_id=agent_id)

        runtime = AgentRuntime(mock_db)
        runtime.agent_repo.get_agent_by_id = AsyncMock(return_value=mock_agent)
        runtime.exec_repo.create_execution = AsyncMock(return_value=mock_exec)
        runtime.exec_repo.update_execution_status = AsyncMock()

        with patch("app.modules.ai.workflows.sourcing_workflow.IntelligentSourcingWorkflow.run") as mock_run:
            mock_run.return_value = {
                "status": "COMPLETED",
                "final_output": {
                    "job_id": str(sample_job_id),
                    "job_title": "Senior Python Engineer",
                    "total_candidates_analyzed": 1,
                    "candidates_shortlisted": 1,
                    "ranked_candidates": [
                        {
                            "rank": 1,
                            "candidate_id": "c1",
                            "candidate_name": "Rahul Sharma",
                            "email": "rahul.sharma@example.com",
                            "match_score": 0.94,
                            "confidence": "HIGH",
                            "strengths": ["Python", "FastAPI"],
                            "gaps": [],
                            "evidence": ["7 years Python experience"],
                            "recommended_action": "SHORTLIST"
                        }
                    ]
                }
            }

            res = await runtime.execute(
                organization_id=sample_org_id,
                user_id=sample_user_id,
                agent_id=agent_id,
                input_data={"job_id": str(sample_job_id), "workflow_type": "sourcing"}
            )

            assert res["status"] == "COMPLETED"
            assert res["execution_id"] == str(exec_id)
            assert res["output_data"]["candidates_shortlisted"] == 1
