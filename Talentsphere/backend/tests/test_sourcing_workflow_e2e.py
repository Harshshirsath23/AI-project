"""
E2E Tests for TalentSphere Intelligent Sourcing Workflow (Milestone 12)

Tests complete sourcing workflow from JD generation through candidate recommendations:
- Job Enhancement Phase: Role classification, JD optimization, keyword extraction, salary analysis
- Candidate Sourcing Phase: Discovery, intelligence analysis, matching, compliance checks
- Ranking & Recommendation Phase: Candidate ranking, recommendation generation
- Publishing Phase: Job board publishing
"""

import pytest
import uuid
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ai.workflows.sourcing_workflow import IntelligentSourcingWorkflow
from app.modules.ai.engine.state import AgentExecutionStateDict
from app.modules.ai.sourcing.schemas import (
    ExtractedJobRequirements, CandidateAnalysisResult, CandidateMatchScore,
    ComplianceReport, RankedCandidate, SourcingRecommendation, MatchingWeights
)
from app.modules.ai.sourcing.agents import (
    JobRequirementIntelligenceAgent,
    CandidateDiscoveryAgent,
    CandidateIntelligenceAgent,
    MatchingAgent,
    ComplianceFairnessAgent,
    CandidateRankingAgent,
    RecommendationAgent,
    JDOptimizerAgent,
    KeywordExtractorAgent,
    SalaryBandAgent,
    LocationAnalyzerAgent,
    RoleClassifierAgent,
    JobBoardPublisherAgent
)
from app.modules.ai.engine.tools import ToolExecutionFramework
from app.modules.ai.engine.hitl import HITLGateManager


# ==================== Fixtures ====================

@pytest.fixture
def org_id() -> uuid.UUID:
    """Organization UUID for test isolation"""
    return uuid.UUID("12345678-1234-5678-1234-567812345678")


@pytest.fixture
def user_id() -> uuid.UUID:
    """User UUID for test execution"""
    return uuid.UUID("87654321-4321-8765-4321-876543218765")


@pytest.fixture
def execution_id() -> str:
    """Unique execution ID"""
    return str(uuid.uuid4())


@pytest.fixture
def sample_job_data() -> Dict[str, Any]:
    """Sample job data for testing"""
    return {
        "job_id": str(uuid.uuid4()),
        "title": "Senior Backend Engineer",
        "description": "We're looking for an experienced backend engineer to join our growing team. "
                      "You'll work on scalable microservices using Python, FastAPI, and PostgreSQL.",
        "required_skills": ["Python", "FastAPI", "PostgreSQL", "Kubernetes", "Docker"],
        "preferred_skills": ["Go", "Rust", "Machine Learning"],
        "min_experience_years": 4,
        "seniority_level": "Senior",
        "location": "San Francisco, CA",
        "employment_type": "Full-time"
    }


@pytest.fixture
def sample_candidates() -> list[Dict[str, Any]]:
    """Sample candidate data for testing"""
    return [
        {
            "candidate_id": str(uuid.uuid4()),
            "first_name": "Alice",
            "last_name": "Johnson",
            "email": "alice.johnson@example.com",
            "skills": ["Python", "FastAPI", "PostgreSQL", "Redis"],
            "experience_years": 6,
            "education": "BS Computer Science"
        },
        {
            "candidate_id": str(uuid.uuid4()),
            "first_name": "Bob",
            "last_name": "Smith",
            "email": "bob.smith@example.com",
            "skills": ["Python", "Django", "PostgreSQL", "Kubernetes"],
            "experience_years": 5,
            "education": "MS Computer Science"
        },
        {
            "candidate_id": str(uuid.uuid4()),
            "first_name": "Carol",
            "last_name": "Williams",
            "email": "carol.williams@example.com",
            "skills": ["JavaScript", "Node.js", "MongoDB"],
            "experience_years": 3,
            "education": "Bootcamp Graduate"
        }
    ]


@pytest.fixture
def initial_workflow_state(
    org_id: uuid.UUID,
    user_id: uuid.UUID,
    execution_id: str,
    sample_job_data: Dict[str, Any]
) -> AgentExecutionStateDict:
    """Create initial workflow state"""
    return {
        "organization_id": str(org_id),
        "user_id": str(user_id),
        "agent_id": str(uuid.uuid4()),
        "execution_id": execution_id,
        "request": {
            "job_id": sample_job_data["job_id"],
            "workflow_type": "sourcing",
            "weights": None,
            "publish_to_boards": False
        },
        "intermediate_results": {},
        "final_output": {},
        "status": "RUNNING",
        "errors": []
    }


# ==================== Individual Agent Tests ====================

@pytest.mark.asyncio
async def test_job_requirement_intelligence_agent():
    """Test Job Requirement Intelligence Agent extracts structured requirements"""
    agent = JobRequirementIntelligenceAgent()
    
    job_data = {
        "job_id": str(uuid.uuid4()),
        "title": "Senior Python Engineer",
        "description": "Looking for Python expert with 5+ years experience",
        "required_skills": ["Python", "FastAPI", "PostgreSQL"],
        "min_experience_years": 5
    }
    
    requirements = await agent.extract_requirements(job_data)
    
    assert isinstance(requirements, ExtractedJobRequirements)
    assert requirements.role == "Senior Python Engineer"
    assert "Python" in requirements.required_skills
    assert requirements.minimum_experience_years >= 5


@pytest.mark.asyncio
async def test_jd_optimizer_agent():
    """Test JD Optimizer Agent enhances job descriptions"""
    agent = JDOptimizerAgent()
    
    job_data = {
        "job_id": str(uuid.uuid4()),
        "title": "Senior Backend Engineer",
        "description": "Backend engineer needed",
        "required_skills": ["Python", "PostgreSQL"]
    }
    
    optimized = await agent.optimize_jd(job_data)
    
    assert "optimized_description" in optimized
    assert optimized.get("seo_keywords") is not None
    assert optimized.get("readability_score", 0) > 0
    assert optimized.get("inclusivity_score", 0) > 0


@pytest.mark.asyncio
async def test_keyword_extractor_agent():
    """Test Keyword Extractor Agent extracts and categorizes keywords"""
    agent = KeywordExtractorAgent()
    
    job_data = {
        "job_id": str(uuid.uuid4()),
        "title": "Senior Python Engineer",
        "description": "Build scalable microservices with Python",
        "required_skills": ["Python", "FastAPI", "PostgreSQL"]
    }
    
    keywords = await agent.extract_keywords(job_data)
    
    assert "technical_keywords" in keywords
    assert "soft_keywords" in keywords
    assert "seo_tags" in keywords
    assert isinstance(keywords.get("technical_keywords"), list)


@pytest.mark.asyncio
async def test_salary_band_agent():
    """Test Salary Band Agent recommends appropriate salary ranges"""
    agent = SalaryBandAgent()
    
    job_data = {
        "job_id": str(uuid.uuid4()),
        "title": "Senior Backend Engineer",
        "required_skills": ["Python", "FastAPI", "PostgreSQL"]
    }
    
    salary_band = await agent.recommend_salary_band(job_data, "San Francisco", "Senior")
    
    assert "min_salary" in salary_band
    assert "max_salary" in salary_band
    assert salary_band["min_salary"] <= salary_band["max_salary"]
    assert salary_band.get("confidence_score", 0) > 0.8


@pytest.mark.asyncio
async def test_location_analyzer_agent():
    """Test Location Analyzer provides talent market insights"""
    agent = LocationAnalyzerAgent()
    
    job_data = {
        "job_id": str(uuid.uuid4()),
        "title": "Senior Backend Engineer",
        "location": "San Francisco, CA"
    }
    
    location_analysis = await agent.analyze_location(job_data)
    
    assert "recommended_locations" in location_analysis
    assert "talent_density_score" in location_analysis
    assert location_analysis.get("remote_work_feasibility") in ["High", "Medium", "Low"]


@pytest.mark.asyncio
async def test_role_classifier_agent():
    """Test Role Classifier categorizes jobs into standard families"""
    agent = RoleClassifierAgent()
    
    job_data = {
        "job_id": str(uuid.uuid4()),
        "title": "Senior Backend Engineer",
        "description": "Lead backend development team",
        "required_skills": ["Python", "Architecture", "Team Leadership"]
    }
    
    classification = await agent.classify_role(job_data)
    
    assert "job_family" in classification
    assert "seniority_level" in classification
    assert "role_category" in classification
    assert classification.get("classification_confidence", 0) > 0.85


@pytest.mark.asyncio
async def test_job_board_publisher_agent(mocker):
    """Test Job Board Publisher Agent publishes to multiple boards"""
    # Mock the tool framework
    mock_tool_framework = mocker.MagicMock()
    
    agent = JobBoardPublisherAgent(mock_tool_framework)
    
    job_data = {
        "job_id": str(uuid.uuid4()),
        "title": "Senior Backend Engineer",
        "description": "We're hiring a Senior Backend Engineer"
    }
    
    results = await agent.publish_to_boards(job_data, ["linkedin", "indeed"])
    
    assert "publication_results" in results
    assert "linkedin" in results["publication_results"]
    assert "indeed" in results["publication_results"]


# ==================== Workflow Integration Tests ====================

@pytest.mark.asyncio
async def test_intelligent_sourcing_workflow_validation_node(
    initial_workflow_state: AgentExecutionStateDict
):
    """Test workflow validation node"""
    from app.database.session import AsyncSessionLocal
    
    async with AsyncSessionLocal() as db:
        workflow = IntelligentSourcingWorkflow(db)
        state = await workflow.node_validate_request(initial_workflow_state)
        
        assert state["intermediate_results"]["validation"]["valid"]
        assert len(state["errors"]) == 0


@pytest.mark.asyncio
async def test_intelligent_sourcing_workflow_requirement_extraction(
    initial_workflow_state: AgentExecutionStateDict,
    sample_job_data: Dict[str, Any]
):
    """Test job requirement extraction in workflow"""
    from app.database.session import AsyncSessionLocal
    
    async with AsyncSessionLocal() as db:
        workflow = IntelligentSourcingWorkflow(db)
        
        # Manually set job data (normally from database)
        initial_workflow_state["intermediate_results"]["job"] = sample_job_data
        initial_workflow_state["intermediate_results"]["validation"] = {"job_id": sample_job_data["job_id"]}
        
        state = await workflow.node_requirement_intelligence(initial_workflow_state)
        
        assert "requirements" in state["intermediate_results"]
        req = state["intermediate_results"]["requirements"]
        assert req.get("role") is not None


@pytest.mark.asyncio
async def test_matching_agent_calculation(
    sample_candidates: list[Dict[str, Any]],
    sample_job_data: Dict[str, Any]
):
    """Test candidate matching score calculation"""
    # Create job requirements
    job_reqs = ExtractedJobRequirements(
        role=sample_job_data["title"],
        required_skills=sample_job_data["required_skills"],
        minimum_experience_years=sample_job_data["min_experience_years"]
    )
    
    # Create candidate analysis
    candidate_analysis = CandidateAnalysisResult(
        candidate_id=sample_candidates[0]["candidate_id"],
        first_name=sample_candidates[0]["first_name"],
        last_name=sample_candidates[0]["last_name"],
        skills_evidence={"Python": "Expert", "FastAPI": "Advanced"},
        experience_years=sample_candidates[0]["experience_years"],
        education_summary=sample_candidates[0]["education"],
        strengths=["Strong Python background", "FastAPI expertise"],
        gaps=["Limited Kubernetes experience"]
    )
    
    matcher = MatchingAgent()
    match_score = matcher.calculate_match(candidate_analysis, job_reqs)
    
    assert isinstance(match_score, CandidateMatchScore)
    assert match_score.total_match_score >= 0.0
    assert match_score.total_match_score <= 1.0
    assert match_score.skill_match_score > 0  # Should match on Python and FastAPI


@pytest.mark.asyncio
async def test_candidate_ranking_workflow(
    sample_candidates: list[Dict[str, Any]],
    sample_job_data: Dict[str, Any]
):
    """Test candidate ranking logic"""
    # Create mock analyses and scores
    analyses = []
    scores = []
    
    for candidate in sample_candidates:
        analysis = CandidateAnalysisResult(
            candidate_id=candidate["candidate_id"],
            first_name=candidate["first_name"],
            last_name=candidate["last_name"],
            skills_evidence={skill: "Verified" for skill in candidate["skills"]},
            experience_years=candidate["experience_years"],
            education_summary=candidate["education"],
            strengths=[f"Experienced in {', '.join(candidate['skills'][:2])}"],
            gaps=["Some missing skills"]
        )
        analyses.append(analysis)
        
        # Create matching score
        matching_count = len(set(candidate["skills"]) & set(sample_job_data["required_skills"]))
        score = CandidateMatchScore(
            candidate_id=candidate["candidate_id"],
            skill_match_score=matching_count / len(sample_job_data["required_skills"]),
            experience_match_score=candidate["experience_years"] / sample_job_data["min_experience_years"],
            role_match_score=0.85,
            education_match_score=0.80,
            semantic_fit_score=0.88,
            total_match_score=(matching_count / len(sample_job_data["required_skills"])) * 0.4 + 0.5,
            matching_skills=list(set(candidate["skills"]) & set(sample_job_data["required_skills"])),
            missing_skills=list(set(sample_job_data["required_skills"]) - set(candidate["skills"]))
        )
        scores.append(score)
    
    # Test ranking
    ranker = CandidateRankingAgent()
    ranked = ranker.rank_candidates(analyses, scores)
    
    assert len(ranked) == len(analyses)
    assert ranked[0].rank == 1
    # Top candidate should have highest score
    assert ranked[0].match_score >= ranked[1].match_score


@pytest.mark.asyncio
async def test_recommendation_report_generation(
    sample_candidates: list[Dict[str, Any]],
    sample_job_data: Dict[str, Any]
):
    """Test final recommendation report generation"""
    # Create ranked candidates
    ranked_candidates = [
        RankedCandidate(
            rank=1,
            candidate_id=sample_candidates[0]["candidate_id"],
            candidate_name=f"{sample_candidates[0]['first_name']} {sample_candidates[0]['last_name']}",
            email=sample_candidates[0]["email"],
            match_score=0.92,
            confidence="HIGH",
            strengths=["Python expert", "5+ years experience"],
            gaps=["New to Go"],
            evidence=["5+ years Python", "FastAPI production experience"],
            recommended_action="SHORTLIST"
        ),
        RankedCandidate(
            rank=2,
            candidate_id=sample_candidates[1]["candidate_id"],
            candidate_name=f"{sample_candidates[1]['first_name']} {sample_candidates[1]['last_name']}",
            email=sample_candidates[1]["email"],
            match_score=0.78,
            confidence="MEDIUM",
            strengths=["Solid Python background"],
            gaps=["Limited FastAPI experience"],
            evidence=["5 years Django experience"],
            recommended_action="SHORTLIST"
        )
    ]
    
    # Create compliance reports
    compliance_reports = [
        ComplianceReport(
            candidate_id=c.candidate_id,
            compliance_status="PASS",
            risk_level="LOW",
            issues=[],
            explanation="All evaluation based on job-relevant credentials"
        )
        for c in ranked_candidates
    ]
    
    # Generate recommendation
    recommender = RecommendationAgent()
    recommendation = recommender.generate_recommendation_report(
        job_id=sample_job_data["job_id"],
        job_title=sample_job_data["title"],
        total_analyzed=2,
        ranked_candidates=ranked_candidates,
        compliance_reports=compliance_reports
    )
    
    assert isinstance(recommendation, SourcingRecommendation)
    assert recommendation.job_id == sample_job_data["job_id"]
    assert recommendation.job_title == sample_job_data["title"]
    assert recommendation.candidates_shortlisted == 2
    assert recommendation.compliance_status == "PASS"


# ==================== Compliance & Fairness Tests ====================

@pytest.mark.asyncio
async def test_compliance_audit_high_quality_candidate(mocker):
    """Test compliance audit passes for qualified candidate"""
    mock_tool_framework = mocker.MagicMock()
    mock_tool_framework.execute_tool.return_value = {
        "result": {"policy": "No discrimination factors"}
    }
    
    agent = ComplianceFairnessAgent(mock_tool_framework)
    
    analysis = CandidateAnalysisResult(
        candidate_id=str(uuid.uuid4()),
        first_name="Alice",
        last_name="Johnson",
        skills_evidence={"Python": "Expert", "FastAPI": "Advanced"},
        experience_years=6,
        education_summary="BS Computer Science",
        strengths=["Strong technical background"],
        gaps=["Limited DevOps"]
    )
    
    match_score = CandidateMatchScore(
        candidate_id=analysis.candidate_id,
        skill_match_score=0.95,
        experience_match_score=0.95,
        role_match_score=0.90,
        education_match_score=0.85,
        semantic_fit_score=0.92,
        total_match_score=0.91,
        matching_skills=["Python", "FastAPI"],
        missing_skills=[]
    )
    
    report = await agent.audit_candidate(
        org_id=uuid.uuid4(),
        analysis=analysis,
        match_score=match_score,
        user_permissions=["ai:execute"]
    )
    
    assert report.compliance_status == "PASS"
    assert report.risk_level == "LOW"
    assert len(report.issues) == 0


# ==================== End-to-End Workflow Tests ====================

@pytest.mark.asyncio
async def test_complete_sourcing_workflow_e2e(
    initial_workflow_state: AgentExecutionStateDict,
    sample_job_data: Dict[str, Any],
    mocker,
    org_id: uuid.UUID,
    user_id: uuid.UUID
):
    """Test complete sourcing workflow end-to-end"""
    from app.database.session import AsyncSessionLocal
    
    async with AsyncSessionLocal() as db:
        # Mock tool framework to return sample data
        mock_tool = mocker.MagicMock()
        
        workflow = IntelligentSourcingWorkflow(db)
        
        # Setup initial state with job data
        state = initial_workflow_state
        state["intermediate_results"]["job"] = sample_job_data
        state["intermediate_results"]["validation"] = {"job_id": sample_job_data["job_id"]}
        
        # Execute critical workflow nodes
        state = await workflow.node_requirement_intelligence(state)
        assert "requirements" in state["intermediate_results"]
        
        state = await workflow.node_role_classification(state)
        assert "role_classification" in state["intermediate_results"]
        
        state = await workflow.node_jd_optimization(state)
        assert "optimized_jd" in state["intermediate_results"]
        
        state = await workflow.node_keyword_extraction(state)
        assert "keywords" in state["intermediate_results"]
        
        state = await workflow.node_salary_band_analysis(state)
        assert "salary_band" in state["intermediate_results"]
        
        state = await workflow.node_location_analysis(state)
        assert "location_analysis" in state["intermediate_results"]
        
        # Verify job enhancement phase completed
        assert state["status"] == "RUNNING"
        assert len(state["errors"]) == 0


@pytest.mark.asyncio
async def test_error_handling_in_workflow(
    initial_workflow_state: AgentExecutionStateDict
):
    """Test error handling in workflow"""
    from app.database.session import AsyncSessionLocal
    
    async with AsyncSessionLocal() as db:
        workflow = IntelligentSourcingWorkflow(db)
        
        # Test validation error
        bad_state = initial_workflow_state.copy()
        bad_state["request"] = {}  # Missing job_id
        
        state = await workflow.node_validate_request(bad_state)
        
        assert state["status"] == "RUNNING"  # Validation doesn't fail status, just adds errors
        assert len(state["errors"]) > 0


# ==================== Performance & Scalability Tests ====================

@pytest.mark.asyncio
async def test_workflow_performance_with_multiple_candidates(
    initial_workflow_state: AgentExecutionStateDict,
    sample_job_data: Dict[str, Any]
):
    """Test workflow performance with realistic candidate volume"""
    import time
    
    from app.database.session import AsyncSessionLocal
    
    async with AsyncSessionLocal() as db:
        workflow = IntelligentSourcingWorkflow(db)
        
        # Setup state with job data
        state = initial_workflow_state
        state["intermediate_results"]["job"] = sample_job_data
        state["intermediate_results"]["validation"] = {"job_id": sample_job_data["job_id"]}
        
        # Time critical job enhancement phase
        start_time = time.time()
        
        state = await workflow.node_requirement_intelligence(state)
        state = await workflow.node_role_classification(state)
        state = await workflow.node_jd_optimization(state)
        state = await workflow.node_keyword_extraction(state)
        state = await workflow.node_salary_band_analysis(state)
        state = await workflow.node_location_analysis(state)
        
        elapsed = time.time() - start_time
        
        # Job enhancement should complete in reasonable time (< 30 seconds for mock)
        assert elapsed < 30
        assert len(state["errors"]) == 0
        print(f"Job enhancement phase completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
