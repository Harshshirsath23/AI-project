"""
TalentSphere Intelligent Sourcing & Candidate Discovery Package
"""

from app.modules.ai.sourcing.schemas import (
    ExtractedJobRequirements,
    CandidateAnalysisResult,
    MatchingWeights,
    CandidateMatchScore,
    ComplianceReport,
    RankedCandidate,
    SourcingRecommendation,
    SourcingExecutionRequest,
    SourcingExecutionResponse
)
from app.modules.ai.sourcing.agents import (
    JobRequirementIntelligenceAgent,
    CandidateDiscoveryAgent,
    CandidateIntelligenceAgent,
    MatchingAgent,
    ComplianceFairnessAgent,
    CandidateRankingAgent,
    RecommendationAgent
)

__all__ = [
    "ExtractedJobRequirements",
    "CandidateAnalysisResult",
    "MatchingWeights",
    "CandidateMatchScore",
    "ComplianceReport",
    "RankedCandidate",
    "SourcingRecommendation",
    "SourcingExecutionRequest",
    "SourcingExecutionResponse",
    "JobRequirementIntelligenceAgent",
    "CandidateDiscoveryAgent",
    "CandidateIntelligenceAgent",
    "MatchingAgent",
    "ComplianceFairnessAgent",
    "CandidateRankingAgent",
    "RecommendationAgent"
]
