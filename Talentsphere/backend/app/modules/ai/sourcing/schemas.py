import uuid
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ExtractedJobRequirements(BaseModel):
    """Structured job requirements extracted by JobRequirementIntelligenceAgent."""
    role: str = Field(..., description="Job role or title")
    required_skills: List[str] = Field(default_factory=list, description="Mandatory required skills")
    preferred_skills: List[str] = Field(default_factory=list, description="Preferred or nice-to-have skills")
    minimum_experience_years: int = Field(default=0, description="Minimum years of experience required")
    education_requirements: List[str] = Field(default_factory=list, description="Education or degree requirements")
    location_requirements: List[str] = Field(default_factory=list, description="Location or work mode constraints")
    other_constraints: List[str] = Field(default_factory=list, description="Other specific requirements")


class CandidateAnalysisResult(BaseModel):
    """In-depth candidate profile & resume evidence analysis."""
    candidate_id: str
    first_name: str
    last_name: str
    skills_evidence: Dict[str, str] = Field(default_factory=dict, description="Skill to evidence snippet mapping")
    experience_years: int = 0
    education_summary: str = "Degree/Background"
    strengths: List[str] = Field(default_factory=list)
    gaps: List[str] = Field(default_factory=list)


class MatchingWeights(BaseModel):
    """Configurable organizational matching weights totaling 1.0 (100%)."""
    skills_weight: float = Field(default=0.35, description="Weight for skill match (0.0 to 1.0)")
    experience_weight: float = Field(default=0.25, description="Weight for experience match (0.0 to 1.0)")
    role_weight: float = Field(default=0.20, description="Weight for role alignment (0.0 to 1.0)")
    education_weight: float = Field(default=0.10, description="Weight for education match (0.0 to 1.0)")
    semantic_weight: float = Field(default=0.10, description="Weight for semantic vector fit (0.0 to 1.0)")
    min_match_threshold: float = Field(default=0.70, description="Minimum overall score to recommend SHORTLIST")


class CandidateMatchScore(BaseModel):
    """Detailed breakdown of candidate match evaluation."""
    candidate_id: str
    skill_match_score: float
    experience_match_score: float
    role_match_score: float
    education_match_score: float
    semantic_fit_score: float
    total_match_score: float
    matching_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)


class ComplianceReport(BaseModel):
    """Compliance and non-discrimination fairness report."""
    candidate_id: str
    compliance_status: str = Field(..., description="PASS or REVIEW_REQUIRED")
    risk_level: str = Field(..., description="LOW or HIGH")
    issues: List[str] = Field(default_factory=list)
    explanation: str = Field(..., description="Justification based strictly on job-relevant criteria")


class RankedCandidate(BaseModel):
    """Single ranked candidate item in final recommendation shortlist."""
    rank: int
    candidate_id: str
    candidate_name: str
    email: str
    match_score: float
    confidence: str = Field(..., description="HIGH, MEDIUM, or LOW")
    strengths: List[str] = Field(default_factory=list)
    gaps: List[str] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)
    recommended_action: str = Field(..., description="SHORTLIST, HOLD, or REJECT")


class SourcingRecommendation(BaseModel):
    """Recruiter-facing AI Sourcing Result."""
    job_id: str
    job_title: str
    total_candidates_analyzed: int
    candidates_shortlisted: int
    ranked_candidates: List[RankedCandidate] = Field(default_factory=list)
    compliance_status: str = "PASS"
    hitl_required: bool = False
    generated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class SourcingExecutionRequest(BaseModel):
    job_id: uuid.UUID = Field(..., description="Job UUID to source candidates for")
    weights: Optional[MatchingWeights] = Field(None, description="Optional custom organization weights")
    publish_to_boards: Optional[bool] = Field(False, description="Whether to publish job to job boards after optimization")
    target_boards: Optional[List[str]] = Field(None, description="Target job boards for publishing (e.g., linkedin, indeed, glassdoor)")


class SourcingExecutionResponse(BaseModel):
    execution_id: str
    status: str
    langsmith_trace_id: Optional[str] = None
    recommendation: Optional[SourcingRecommendation] = None
    message: str = "Sourcing execution initiated"
