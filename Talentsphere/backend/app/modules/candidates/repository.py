import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, update, func

from app.modules.candidates.models import (
    Candidate, CandidateProfile, CandidateEducation, CandidateExperience,
    CandidateSkill, CandidateCertification, CandidateResume, ResumeVersion,
    CandidateAiProfile, CandidateTimeline, CandidateEmbedding,
    CandidateAiSummary, CandidateAiRecommendation
)
from app.modules.candidates.schemas import (
    CandidateCreate, CandidateEducationCreate, CandidateExperienceCreate,
    CandidateSkillCreate, CandidateCertificationCreate, CandidateSearchRequest
)

class CandidateRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, org_id: uuid.UUID, data: CandidateCreate) -> Candidate:
        candidate = Candidate(**data.model_dump(), organization_id=org_id)
        self.db.add(candidate)
        await self.db.flush()
        
        # Auto-create empty profile and AI profile
        profile = CandidateProfile(candidate_id=candidate.id)
        ai_profile = CandidateAiProfile(candidate_id=candidate.id, ai_profile_completeness=0)
        
        self.db.add(profile)
        self.db.add(ai_profile)
        await self.db.flush()
        
        return candidate

    async def get_by_id(self, org_id: uuid.UUID, candidate_id: uuid.UUID) -> Optional[Candidate]:
        stmt = select(Candidate).where(
            Candidate.id == candidate_id, 
            Candidate.organization_id == org_id
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_all(self, org_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Candidate]:
        stmt = select(Candidate).where(Candidate.organization_id == org_id).offset(skip).limit(limit)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def delete(self, org_id: uuid.UUID, candidate_id: uuid.UUID) -> bool:
        stmt = select(Candidate).where(Candidate.id == candidate_id, Candidate.organization_id == org_id)
        res = await self.db.execute(stmt)
        cand = res.scalar_one_or_none()
        if cand:
            await self.db.delete(cand)
            await self.db.flush()
            return True
        return False

    async def get_all_enriched(self, org_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        cands = await self.get_all(org_id, skip, limit)
        results = []
        details_repo = CandidateDetailsRepository(self.db)
        resume_repo = ResumeRepository(self.db)
        for c in cands:
            profile = await details_repo.get_profile(c.id)
            experiences = await details_repo.get_experience(c.id)
            education = await details_repo.get_education(c.id)
            skills = await details_repo.get_skills(c.id)
            resumes = await resume_repo.get_resumes(c.id)
            ai_prof = await details_repo.get_ai_profile(c.id)
            
            current_role = experiences[0].designation_name if experiences else "Candidate"
            current_company = experiences[0].company_name if experiences else "Organization"
            summary_text = profile.summary if profile and profile.summary else ""
            
            skill_list = []
            if ai_prof and ai_prof.ai_top_skills:
                skill_list = [s.strip() for s in ai_prof.ai_top_skills.split(',') if s.strip()]
                
            results.append({
                "id": c.id,
                "organization_id": c.organization_id,
                "first_name": c.first_name,
                "last_name": c.last_name,
                "email": c.email,
                "phone": c.phone,
                "location": "Not Specified",
                "current_role": current_role,
                "current_company": current_company,
                "summary": summary_text,
                "skills": skill_list,
                "match_score": int(ai_prof.ai_profile_completeness or 85) if ai_prof else 85,
                "experiences": experiences,
                "education": education,
                "documents": resumes,
                "created_at": c.created_at,
                "updated_at": c.updated_at
            })
        return results

    async def search(self, org_id: uuid.UUID, req: CandidateSearchRequest) -> List[Candidate]:
        stmt = select(Candidate).where(Candidate.organization_id == org_id)
        
        if req.query:
            search_pattern = f"%{req.query}%"
            stmt = stmt.where(
                or_(
                    Candidate.first_name.ilike(search_pattern),
                    Candidate.last_name.ilike(search_pattern),
                    Candidate.email.ilike(search_pattern),
                    Candidate.phone.ilike(search_pattern)
                )
            )
            
        if req.skills and len(req.skills) > 0:
            stmt = stmt.join(CandidateSkill).where(CandidateSkill.skill_id.in_(req.skills))
            
        # Simplified for now. Advanced joining for experience and notice period goes here.
        stmt = stmt.limit(req.limit).offset(req.offset)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())


class CandidateDetailsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_profile(self, candidate_id: uuid.UUID) -> Optional[CandidateProfile]:
        stmt = select(CandidateProfile).where(CandidateProfile.candidate_id == candidate_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def update_profile(self, candidate_id: uuid.UUID, summary: str = None) -> CandidateProfile:
        prof = await self.get_profile(candidate_id)
        if not prof:
            prof = CandidateProfile(candidate_id=candidate_id, summary=summary)
            self.db.add(prof)
        else:
            if summary:
                prof.summary = summary
        await self.db.flush()
        return prof

    async def get_education(self, candidate_id: uuid.UUID) -> List[CandidateEducation]:
        stmt = select(CandidateEducation).where(CandidateEducation.candidate_id == candidate_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def add_education(self, candidate_id: uuid.UUID, data: CandidateEducationCreate) -> CandidateEducation:
        edu = CandidateEducation(**data.model_dump(), candidate_id=candidate_id)
        self.db.add(edu)
        await self.db.flush()
        return edu

    async def get_experience(self, candidate_id: uuid.UUID) -> List[CandidateExperience]:
        stmt = select(CandidateExperience).where(CandidateExperience.candidate_id == candidate_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def add_experience(self, candidate_id: uuid.UUID, data: CandidateExperienceCreate) -> CandidateExperience:
        exp = CandidateExperience(**data.model_dump(), candidate_id=candidate_id)
        self.db.add(exp)
        await self.db.flush()
        return exp

    async def get_skills(self, candidate_id: uuid.UUID) -> List[CandidateSkill]:
        stmt = select(CandidateSkill).where(CandidateSkill.candidate_id == candidate_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())
        
    async def add_skill(self, candidate_id: uuid.UUID, data: CandidateSkillCreate) -> CandidateSkill:
        skill = CandidateSkill(**data.model_dump(), candidate_id=candidate_id)
        self.db.add(skill)
        await self.db.flush()
        return skill

    async def get_certifications(self, candidate_id: uuid.UUID) -> List[CandidateCertification]:
        stmt = select(CandidateCertification).where(CandidateCertification.candidate_id == candidate_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def get_ai_profile(self, candidate_id: uuid.UUID) -> Optional[CandidateAiProfile]:
        stmt = select(CandidateAiProfile).where(CandidateAiProfile.candidate_id == candidate_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()
        
    async def update_ai_profile_score(self, candidate_id: uuid.UUID, score: float):
        stmt = update(CandidateAiProfile).where(
            CandidateAiProfile.candidate_id == candidate_id
        ).values(ai_profile_completeness=score)
        await self.db.execute(stmt)


class ResumeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_primary_resume(self, candidate_id: uuid.UUID) -> Optional[CandidateResume]:
        stmt = select(CandidateResume).where(
            CandidateResume.candidate_id == candidate_id,
            CandidateResume.is_primary == True
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_resumes(self, candidate_id: uuid.UUID) -> List[CandidateResume]:
        stmt = select(CandidateResume).where(CandidateResume.candidate_id == candidate_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def add_resume(self, candidate_id: uuid.UUID, file_name: str, file_path: str, file_size: int, mime_type: str) -> CandidateResume:
        # Demote previous primary resumes
        stmt = update(CandidateResume).where(CandidateResume.candidate_id == candidate_id).values(is_primary=False)
        await self.db.execute(stmt)
        
        # Add new resume
        resume = CandidateResume(
            candidate_id=candidate_id,
            file_name=file_name,
            file_path=file_path,
            file_size=file_size,
            mime_type=mime_type,
            is_primary=True
        )
        self.db.add(resume)
        await self.db.flush()
        
        # Save version history
        version = ResumeVersion(
            candidate_id=candidate_id,
            resume_id=resume.id,
            version_number=1, # simplified versioning
            file_name=file_name,
            file_path=file_path
        )
        self.db.add(version)
        await self.db.flush()
        
        return resume

class TimelineRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def log_event(self, candidate_id: uuid.UUID, event_name: str, details: str = None):
        event = CandidateTimeline(
            candidate_id=candidate_id,
            event_name=event_name,
            details=details
        )
        self.db.add(event)
        await self.db.flush()

    async def get_timeline(self, candidate_id: uuid.UUID) -> List[CandidateTimeline]:
        stmt = select(CandidateTimeline).where(CandidateTimeline.candidate_id == candidate_id).order_by(CandidateTimeline.created_at.desc())
        res = await self.db.execute(stmt)
        return list(res.scalars().all())


class EmbeddingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def store_embedding(self, candidate_id: uuid.UUID, embedding_vector: List[float], resume_id: Optional[uuid.UUID] = None) -> CandidateEmbedding:
        stmt = select(CandidateEmbedding).where(CandidateEmbedding.candidate_id == candidate_id)
        res = await self.db.execute(stmt)
        existing = res.scalar_one_or_none()
        if existing:
            existing.embedding = embedding_vector
            if resume_id:
                existing.resume_id = resume_id
            await self.db.flush()
            return existing
        else:
            cand_emb = CandidateEmbedding(
                candidate_id=candidate_id,
                resume_id=resume_id,
                embedding=embedding_vector
            )
            self.db.add(cand_emb)
            await self.db.flush()
            return cand_emb

    async def get_embedding(self, candidate_id: uuid.UUID) -> Optional[CandidateEmbedding]:
        stmt = select(CandidateEmbedding).where(CandidateEmbedding.candidate_id == candidate_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_all_embeddings(self, candidate_ids: List[uuid.UUID]) -> List[CandidateEmbedding]:
        if not candidate_ids:
            return []
        stmt = select(CandidateEmbedding).where(CandidateEmbedding.candidate_id.in_(candidate_ids))
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

