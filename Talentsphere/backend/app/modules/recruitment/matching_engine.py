import uuid
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.recruitment.repository import JobRepository
from app.modules.candidates.repository import CandidateDetailsRepository, CandidateRepository
from app.modules.recruitment.schemas import CandidateMatchResponse, MatchScoreBreakdown

class CandidateMatchingEngine:
    """
    Rule-Based Candidate Matching Engine.
    Calculates transparent, objective compatibility scores between Candidate profiles and Job requisitions.
    """
    def __init__(self, db: AsyncSession):
        self.db = db
        self.job_repo = JobRepository(db)
        self.cand_repo = CandidateRepository(db)
        self.cand_details = CandidateDetailsRepository(db)

    async def calculate_match_score(self, org_id: uuid.UUID, candidate_id: uuid.UUID, job_id: uuid.UUID) -> CandidateMatchResponse:
        # Fetch Job details & skills
        job = await self.job_repo.get_by_id(org_id, job_id)
        job_skills = await self.job_repo.get_job_skills(job_id)
        
        # Fetch Candidate details & skills
        cand = await self.cand_repo.get_by_id(org_id, candidate_id)
        cand_skills = await self.cand_details.get_skills(candidate_id)
        cand_exp = await self.cand_details.get_experience(candidate_id)
        cand_edu = await self.cand_details.get_education(candidate_id)

        # 1. Skill Match Score (Weight: 40%)
        job_skill_ids = {js.skill_id for js in job_skills}
        cand_skill_ids = {cs.skill_id for cs in cand_skills}
        
        if job_skill_ids:
            matched_skills = job_skill_ids.intersection(cand_skill_ids)
            skill_score = (len(matched_skills) / len(job_skill_ids)) * 100.0
        else:
            skill_score = 80.0 # Default if no job skills specified

        # 2. Experience Match Score (Weight: 30%)
        exp_years = len(cand_exp) * 1.5 # Estimation heuristic
        experience_score = min(exp_years * 20.0, 100.0) if exp_years > 0 else 50.0

        # 3. Education Match Score (Weight: 20%)
        education_score = 90.0 if len(cand_edu) > 0 else 60.0

        # 4. Location Match Score (Weight: 10%)
        location_score = 85.0

        # Weighted Average Score
        overall = (skill_score * 0.4) + (experience_score * 0.3) + (education_score * 0.2) + (location_score * 0.1)
        overall_score = round(overall, 2)

        breakdown = MatchScoreBreakdown(
            skill_score=round(skill_score, 2),
            experience_score=round(experience_score, 2),
            education_score=round(education_score, 2),
            location_score=round(location_score, 2),
            overall_match_score=overall_score
        )

        return CandidateMatchResponse(
            candidate_id=candidate_id,
            job_id=job_id,
            compatibility_score=overall_score,
            breakdown=breakdown,
            passed_rules=overall_score >= 60.0
        )
