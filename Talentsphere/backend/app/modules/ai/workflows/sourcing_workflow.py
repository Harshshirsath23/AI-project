import uuid
import structlog
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ai.engine.state import AgentExecutionStateDict
from app.modules.ai.engine.tools import ToolExecutionFramework
from app.modules.ai.engine.hitl import HITLGateManager
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
from app.modules.ai.sourcing.schemas import (
    MatchingWeights, SourcingRecommendation
)
from app.core.observability import trace_workflow

logger = structlog.get_logger(__name__)


class IntelligentSourcingWorkflow:
    """
    Milestone 12 — Autonomous Intelligent Sourcing & Candidate Discovery Workflow.
    
    Orchestrates the 14 Sourcing Agents through LangGraph:
    1. node_validate_request
    2. node_load_job
    3. node_requirement_intelligence
    4. node_role_classification
    5. node_jd_optimization
    6. node_keyword_extraction
    7. node_salary_band_analysis
    8. node_location_analysis
    9. node_candidate_discovery
    10. node_candidate_intelligence
    11. node_matching
    12. node_compliance_check
    13. node_hitl_gate (if High Risk)
    14. node_ranking
    15. node_recommendation
    16. node_job_board_publishing
    17. node_finalizer
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.tool_framework = ToolExecutionFramework(db)
        self.hitl_manager = HITLGateManager(db)
        
        # Core Sourcing Agents
        self.req_agent = JobRequirementIntelligenceAgent()
        self.discovery_agent = CandidateDiscoveryAgent(self.tool_framework)
        self.intel_agent = CandidateIntelligenceAgent(self.tool_framework)
        self.matching_agent = MatchingAgent()
        self.compliance_agent = ComplianceFairnessAgent(self.tool_framework)
        self.ranking_agent = CandidateRankingAgent()
        self.recommendation_agent = RecommendationAgent()
        
        # Additional Sourcing Enhancement Agents
        self.jd_optimizer_agent = JDOptimizerAgent()
        self.keyword_extractor_agent = KeywordExtractorAgent()
        self.salary_band_agent = SalaryBandAgent()
        self.location_analyzer_agent = LocationAnalyzerAgent()
        self.role_classifier_agent = RoleClassifierAgent()
        self.job_board_publisher_agent = JobBoardPublisherAgent(self.tool_framework)

    async def node_validate_request(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 1: Validate input request contains job_id."""
        req = state.get("request", {})
        job_id = req.get("job_id")

        errors = []
        if not job_id:
            errors.append("Missing mandatory job_id in sourcing request.")

        state["intermediate_results"]["validation"] = {
            "valid": len(errors) == 0,
            "job_id": job_id
        }
        if errors:
            state["errors"] = state.get("errors", []) + errors

        return state

    async def node_load_job(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 2: Load job details via tool framework."""
        job_id = state["intermediate_results"]["validation"]["job_id"]
        org_id = uuid.UUID(state["organization_id"])

        res = await self.tool_framework.execute_tool(
            tool_name="get_job_details",
            org_id=org_id,
            user_permissions=["recruitment:read"],
            tool_input={"job_id": job_id}
        )

        state["intermediate_results"]["job"] = res.get("result", {})
        return state

    async def node_requirement_intelligence(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 3: Convert job details into structured ExtractedJobRequirements."""
        job_data = state["intermediate_results"].get("job", {})
        reqs = await self.req_agent.extract_requirements(job_data)
        state["intermediate_results"]["requirements"] = reqs.model_dump()
        return state

    async def node_role_classification(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 4: Classify job role into standard categories."""
        job_data = state["intermediate_results"].get("job", {})
        classification = await self.role_classifier_agent.classify_role(job_data)
        state["intermediate_results"]["role_classification"] = classification
        return state

    async def node_jd_optimization(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 5: Optimize job description for SEO and candidate attraction."""
        job_data = state["intermediate_results"].get("job", {})
        optimized_jd = await self.jd_optimizer_agent.optimize_jd(job_data)
        state["intermediate_results"]["optimized_jd"] = optimized_jd
        return state

    async def node_keyword_extraction(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 6: Extract keywords for search optimization."""
        job_data = state["intermediate_results"].get("job", {})
        keywords = await self.keyword_extractor_agent.extract_keywords(job_data)
        state["intermediate_results"]["keywords"] = keywords
        return state

    async def node_salary_band_analysis(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 7: Analyze salary band recommendations."""
        job_data = state["intermediate_results"].get("job", {})
        location_analysis = state["intermediate_results"].get("location_analysis", {})
        salary_band = await self.salary_band_agent.recommend_salary_band(
            job_data,
            location=location_analysis.get("recommended_locations", ["Remote"])[0] if location_analysis else None,
            experience_level=job_data.get("seniority_level", "Mid-Senior")
        )
        state["intermediate_results"]["salary_band"] = salary_band
        return state

    async def node_location_analysis(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 8: Analyze location requirements and market insights."""
        job_data = state["intermediate_results"].get("job", {})
        location_analysis = await self.location_analyzer_agent.analyze_location(job_data)
        state["intermediate_results"]["location_analysis"] = location_analysis
        return state

    async def node_candidate_discovery(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 9: Discover candidate pool."""
        org_id = uuid.UUID(state["organization_id"])
        reqs_dict = state["intermediate_results"]["requirements"]
        from app.modules.ai.sourcing.schemas import ExtractedJobRequirements
        reqs = ExtractedJobRequirements(**reqs_dict)

        discovered = await self.discovery_agent.discover_candidates(
            org_id=org_id,
            requirements=reqs,
            user_permissions=["candidate:read"]
        )

        state["intermediate_results"]["discovered_candidates"] = discovered
        return state

    async def node_candidate_intelligence(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 10: Analyze profile and resume evidence for each candidate."""
        org_id = uuid.UUID(state["organization_id"])
        candidates = state["intermediate_results"].get("discovered_candidates", [])
        reqs_dict = state["intermediate_results"]["requirements"]
        from app.modules.ai.sourcing.schemas import ExtractedJobRequirements
        reqs = ExtractedJobRequirements(**reqs_dict)

        analyses = []
        for cand in candidates:
            analysis = await self.intel_agent.analyze_candidate(
                org_id=org_id,
                candidate_info=cand,
                requirements=reqs,
                user_permissions=["candidate:read"]
            )
            analyses.append(analysis.model_dump())

        state["intermediate_results"]["candidate_analyses"] = analyses
        return state

    async def node_matching(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 11: Compute deterministic weighted match score matrix."""
        reqs_dict = state["intermediate_results"]["requirements"]
        analyses_dicts = state["intermediate_results"].get("candidate_analyses", [])
        custom_weights = state.get("request", {}).get("weights")

        from app.modules.ai.sourcing.schemas import ExtractedJobRequirements, CandidateAnalysisResult
        reqs = ExtractedJobRequirements(**reqs_dict)
        weights = MatchingWeights(**custom_weights) if custom_weights else MatchingWeights()

        scores = []
        for a_dict in analyses_dicts:
            analysis = CandidateAnalysisResult(**a_dict)
            score = self.matching_agent.calculate_match(analysis, reqs, weights=weights)
            scores.append(score.model_dump())

        state["intermediate_results"]["match_scores"] = scores
        return state

    async def node_compliance_check(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 12: Audit non-discrimination and recruitment compliance."""
        org_id = uuid.UUID(state["organization_id"])
        analyses_dicts = state["intermediate_results"].get("candidate_analyses", [])
        scores_dicts = state["intermediate_results"].get("match_scores", [])

        from app.modules.ai.sourcing.schemas import CandidateAnalysisResult, CandidateMatchScore
        compliance_reports = []
        has_high_risk = False

        for a_dict, s_dict in zip(analyses_dicts, scores_dicts):
            analysis = CandidateAnalysisResult(**a_dict)
            score = CandidateMatchScore(**s_dict)
            report = await self.compliance_agent.audit_candidate(
                org_id=org_id,
                analysis=analysis,
                match_score=score,
                user_permissions=["ai:execute"]
            )
            compliance_reports.append(report.model_dump())
            if report.risk_level == "HIGH":
                has_high_risk = True

        state["intermediate_results"]["compliance_reports"] = compliance_reports
        state["intermediate_results"]["compliance_summary"] = {
            "status": "REVIEW_REQUIRED" if has_high_risk else "PASS",
            "hitl_required": has_high_risk
        }
        return state

    async def node_hitl_gate(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 13: Pause workflow if compliance audit flags high risk or approval required."""
        human_decision = state.get("human_decision")
        if human_decision:
            logger.info("Human decision recorded, resuming workflow", decision=human_decision)
            return state

        compliance_summary = state["intermediate_results"].get("compliance_summary", {})
        if compliance_summary.get("hitl_required", False):
            job_info = state["intermediate_results"].get("job", {})
            hitl_res = await self.hitl_manager.check_and_create_hitl_gate(
                execution_id=uuid.UUID(state["execution_id"]),
                agent_id=uuid.UUID(state["agent_id"]),
                requested_by=uuid.UUID(state["user_id"]),
                action_name="Candidate Shortlist Approval",
                risk_level="High",
                request_data={"job_id": job_info.get("job_id"), "job_title": job_info.get("title")},
                reason="Recruiter approval required for candidate shortlist recommendation due to compliance review."
            )
            state["hitl_request"] = hitl_res
            state["status"] = "WAITING_HITL"

        return state

    async def node_ranking(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 14: Order candidates by match score and compute confidence levels."""
        if state.get("status") == "WAITING_HITL":
            return state

        analyses_dicts = state["intermediate_results"].get("candidate_analyses", [])
        scores_dicts = state["intermediate_results"].get("match_scores", [])

        from app.modules.ai.sourcing.schemas import CandidateAnalysisResult, CandidateMatchScore
        analyses = [CandidateAnalysisResult(**d) for d in analyses_dicts]
        scores = [CandidateMatchScore(**d) for d in scores_dicts]

        ranked = self.ranking_agent.rank_candidates(analyses, scores)
        state["intermediate_results"]["ranked_candidates"] = [r.model_dump() for r in ranked]
        return state

    async def node_recommendation(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 15: Generate structured recruiter-facing SourcingRecommendation."""
        if state.get("status") == "WAITING_HITL":
            return state

        job_info = state["intermediate_results"].get("job", {})
        ranked_dicts = state["intermediate_results"].get("ranked_candidates", [])
        compliance_dicts = state["intermediate_results"].get("compliance_reports", [])

        from app.modules.ai.sourcing.schemas import RankedCandidate, ComplianceReport
        ranked = [RankedCandidate(**d) for d in ranked_dicts]
        compliance_reports = [ComplianceReport(**d) for d in compliance_dicts]

        recommendation = self.recommendation_agent.generate_recommendation_report(
            job_id=str(job_info.get("job_id", "")),
            job_title=job_info.get("title", "Job Role"),
            total_analyzed=len(ranked),
            ranked_candidates=ranked,
            compliance_reports=compliance_reports
        )

        state["intermediate_results"]["recommendation"] = recommendation.model_dump()
        return state

    async def node_job_board_publishing(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 16: Publish optimized job to multiple job boards."""
        if state.get("status") == "WAITING_HITL":
            return state

        job_info = state["intermediate_results"].get("job", {})
        optimized_jd = state["intermediate_results"].get("optimized_jd", job_info)
        
        # Only publish if explicitly requested
        if state.get("request", {}).get("publish_to_boards", False):
            target_boards = state.get("request", {}).get("target_boards", ["linkedin", "indeed", "glassdoor"])
            publishing_results = await self.job_board_publisher_agent.publish_to_boards(
                job_data=optimized_jd,
                target_boards=target_boards
            )
            state["intermediate_results"]["publishing_results"] = publishing_results
        else:
            state["intermediate_results"]["publishing_results"] = {
                "status": "skipped",
                "reason": "Publishing not requested"
            }
        
        return state

    async def node_finalizer(self, state: AgentExecutionStateDict) -> AgentExecutionStateDict:
        """Node 17: Format final output and update execution status."""
        if state.get("status") == "WAITING_HITL":
            return state

        # Compile comprehensive final output
        rec_dict = state["intermediate_results"].get("recommendation", {})
        job_info = state["intermediate_results"].get("job", {})
        
        final_output = {
            **rec_dict,
            "job_enhancement": {
                "role_classification": state["intermediate_results"].get("role_classification", {}),
                "optimized_jd": state["intermediate_results"].get("optimized_jd", {}),
                "keywords": state["intermediate_results"].get("keywords", {}),
                "salary_band": state["intermediate_results"].get("salary_band", {}),
                "location_analysis": state["intermediate_results"].get("location_analysis", {}),
                "publishing_results": state["intermediate_results"].get("publishing_results", {})
            },
            "job_title": job_info.get("title"),
            "job_id": job_info.get("job_id")
        }
        
        state["final_output"] = final_output
        state["status"] = "COMPLETED"
        return state

    async def run(
        self,
        state: AgentExecutionStateDict,
        org_id: uuid.UUID,
        user_id: uuid.UUID,
        user_permissions: List[str]
    ) -> AgentExecutionStateDict:
        """Execute Intelligent Sourcing Workflow graph nodes sequentially."""
        async with trace_workflow(
            workflow_name="Intelligent Sourcing Workflow",
            inputs=state.get("request", {})
        ) as span:
            state = await self.node_validate_request(state)
            if state.get("errors"):
                state["status"] = "FAILED"
                span.end(outputs=state, error="Validation errors")
                return state

            # Job Enhancement Phase
            state = await self.node_load_job(state)
            state = await self.node_requirement_intelligence(state)
            state = await self.node_role_classification(state)
            state = await self.node_jd_optimization(state)
            state = await self.node_keyword_extraction(state)
            state = await self.node_salary_band_analysis(state)
            state = await self.node_location_analysis(state)

            # Candidate Sourcing Phase
            state = await self.node_candidate_discovery(state)
            state = await self.node_candidate_intelligence(state)
            state = await self.node_matching(state)
            state = await self.node_compliance_check(state)

            # HITL Gate
            state = await self.node_hitl_gate(state)
            if state.get("status") == "WAITING_HITL":
                span.end(outputs={"status": "WAITING_HITL", "hitl_request": state.get("hitl_request")})
                return state

            # Ranking and Recommendation Phase
            state = await self.node_ranking(state)
            state = await self.node_recommendation(state)
            state = await self.node_job_board_publishing(state)
            state = await self.node_finalizer(state)

            span.end(outputs=state.get("final_output", {}))
            return state
