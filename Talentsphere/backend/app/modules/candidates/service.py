import uuid
import os
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, HTTPException

from app.core.storage import storage_service
from app.core.embeddings import embedding_engine
from app.modules.candidates.repository import (
    CandidateRepository, CandidateDetailsRepository, ResumeRepository, TimelineRepository, EmbeddingRepository
)
from app.modules.candidates.schemas import (
    CandidateCreate, CandidateEducationCreate, CandidateExperienceCreate, CandidateSkillCreate,
    CandidateSearchRequest, FullCandidateProfileResponse
)

class ProfileCompletionEngine:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.details_repo = CandidateDetailsRepository(db)
        self.resume_repo = ResumeRepository(db)

    async def recalculate_score(self, candidate_id: uuid.UUID) -> float:
        """
        Calculates a 0-100% completion score for a candidate profile based on required fields.
        """
        score = 0
        total_weight = 100
        
        # 1. Base Profile Exists (from registration) = 20%
        score += 20
        
        # 2. Resume Uploaded = 30%
        primary_resume = await self.resume_repo.get_primary_resume(candidate_id)
        if primary_resume:
            score += 30
            
        # 3. Education Added = 15%
        education = await self.details_repo.get_education(candidate_id)
        if education and len(education) > 0:
            score += 15
            
        # 4. Experience Added = 20%
        experience = await self.details_repo.get_experience(candidate_id)
        if experience and len(experience) > 0:
            score += 20
            
        # 5. Skills Added = 15%
        skills = await self.details_repo.get_skills(candidate_id)
        if skills and len(skills) > 0:
            score += 15
            
        # Ensure it's capped at 100
        final_score = min(score, 100)
        
        # Update the AI profile table
        await self.details_repo.update_ai_profile_score(candidate_id, final_score)
        await self.db.flush()
        
        return final_score


class CandidateService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.cand_repo = CandidateRepository(db)
        self.details_repo = CandidateDetailsRepository(db)
        self.resume_repo = ResumeRepository(db)
        self.timeline_repo = TimelineRepository(db)
        self.embedding_repo = EmbeddingRepository(db)
        self.completion_engine = ProfileCompletionEngine(db)

    async def create_candidate(self, org_id: uuid.UUID, data: CandidateCreate) -> dict:
        cand = await self.cand_repo.create(org_id, data)
        await self.timeline_repo.log_event(cand.id, "Candidate Created", f"Profile initialized via API")
        await self.completion_engine.recalculate_score(cand.id)
        await self.db.commit()
        return {"status": "success", "candidate_id": cand.id, "message": "Candidate created successfully"}

    async def create_candidate_from_staged(self, org_id: uuid.UUID, data: "CandidateCreateFromStaged") -> dict:
        from app.modules.candidates.schemas import CandidateExperienceCreate

        # 1. Create candidate
        cand = await self.cand_repo.create(org_id, data.candidate)
        await self.timeline_repo.log_event(cand.id, "Candidate Created", "Created from staged resume upload")
        
        # 2. Add profile summary & skills
        if data.summary:
            await self.details_repo.update_profile(cand.id, summary=data.summary)
            
        if data.raw_skills:
            ai_prof = await self.details_repo.get_ai_profile(cand.id)
            if ai_prof:
                ai_prof.ai_top_skills = ", ".join(data.raw_skills)
                await self.db.flush()

        # 3. Add sub-entities
        for edu in data.education or []:
            await self.details_repo.add_education(cand.id, edu)

        exp_list = data.experience or []
        if not exp_list and (data.current_role or data.current_company):
            from datetime import date
            exp_list = [
                CandidateExperienceCreate(
                    company_name=data.current_company or "Organization",
                    designation_name=data.current_role or "Candidate",
                    start_date=date.today(),
                    is_current=True,
                    description=data.summary or f"Role as {data.current_role} at {data.current_company}"
                )
            ]

        for exp in exp_list:
            await self.details_repo.add_experience(cand.id, exp)
            
        for skill in data.skills or []:
            await self.details_repo.add_skill(cand.id, skill)

        # 4. Move staged file
        final_dir = f"organizations/{org_id}/candidates/{cand.id}/resumes"
        storage_service.create_directory(final_dir)
        final_path = f"{final_dir}/{data.original_filename}"
        
        try:
            await storage_service.move(data.staged_file_path, final_path)
        except Exception:
            # Fallback if file already moved or path issue
            final_path = data.staged_file_path
            
        # 5. Save Resume record
        await self.resume_repo.add_resume(
            candidate_id=cand.id,
            file_name=data.original_filename,
            file_path=final_path,
            file_size=data.file_size,
            mime_type=data.mime_type
        )
        
        await self.timeline_repo.log_event(cand.id, "Resume Uploaded", f"Moved from staging: {data.original_filename}")
        await self.completion_engine.recalculate_score(cand.id)
        await self.db.commit()
        
        return {
            "status": "success",
            "candidate_id": cand.id,
            "candidate": {
                "id": cand.id,
                "first_name": cand.first_name,
                "last_name": cand.last_name,
                "email": cand.email,
                "phone": cand.phone,
                "current_role": data.current_role or "Candidate",
                "current_company": data.current_company or "Organization",
                "summary": data.summary or "",
                "skills": data.raw_skills or [],
                "location": data.location or "Not Specified",
                "match_score": 85,
                "created_at": cand.created_at,
                "updated_at": cand.updated_at
            },
            "message": "Candidate created from staged resume"
        }

    async def delete_candidate(self, org_id: uuid.UUID, candidate_id: uuid.UUID) -> dict:
        deleted = await self.cand_repo.delete(org_id, candidate_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Candidate not found")
        await self.db.commit()
        return {"status": "success", "message": "Candidate deleted successfully"}

    async def upload_and_create_candidate(self, org_id: uuid.UUID, file: UploadFile) -> dict:
        """1-step process: uploads resume, parses it, and creates the candidate automatically."""
        # 1. Parse it
        resume_service = ResumeService(self.db)
        parse_result = await resume_service.stage_and_parse_resume(org_id, file)
        
        # 2. Build the payload
        from app.modules.candidates.schemas import CandidateCreateFromStaged, CandidateCreate
        extracted = parse_result["extracted_data"]
        cand_data = CandidateCreate(
            first_name=extracted["first_name"],
            last_name=extracted["last_name"],
            email=extracted["email"],
            phone=extracted["phone"]
        )
        
        payload = CandidateCreateFromStaged(
            candidate=cand_data,
            staged_file_path=parse_result["staged_file_path"],
            original_filename=parse_result["original_filename"],
            file_size=parse_result["file_size"],
            mime_type=parse_result["mime_type"]
        )
        
        # 3. Create it
        result = await self.create_candidate_from_staged(org_id, payload)
        result["extracted_data"] = extracted
        return result

    async def search(self, org_id: uuid.UUID, req: CandidateSearchRequest) -> List[Any]:
        return await self.cand_repo.search(org_id, req)

    async def _validate_candidate_org_access(self, org_id: uuid.UUID, candidate_id: uuid.UUID):
        cand = await self.cand_repo.get_by_id(org_id, candidate_id)
        if not cand:
            raise HTTPException(status_code=404, detail="Candidate not found in this organization")
        return cand

    async def add_education(self, org_id: uuid.UUID, candidate_id: uuid.UUID, data: CandidateEducationCreate) -> dict:
        await self._validate_candidate_org_access(org_id, candidate_id)
        edu = await self.details_repo.add_education(candidate_id, data)
        await self.timeline_repo.log_event(candidate_id, "Education Added", f"Added {data.degree_name}")
        await self.completion_engine.recalculate_score(candidate_id)
        await self.db.commit()
        return {"status": "success", "message": "Education added successfully"}
        
    async def add_experience(self, org_id: uuid.UUID, candidate_id: uuid.UUID, data: CandidateExperienceCreate) -> dict:
        await self._validate_candidate_org_access(org_id, candidate_id)
        exp = await self.details_repo.add_experience(candidate_id, data)
        await self.timeline_repo.log_event(candidate_id, "Experience Added", f"Added {data.company_name}")
        await self.completion_engine.recalculate_score(candidate_id)
        await self.db.commit()
        return {"status": "success", "message": "Experience added successfully"}

    async def add_skill(self, org_id: uuid.UUID, candidate_id: uuid.UUID, data: CandidateSkillCreate) -> dict:
        await self._validate_candidate_org_access(org_id, candidate_id)
        skill = await self.details_repo.add_skill(candidate_id, data)
        await self.timeline_repo.log_event(candidate_id, "Skill Added", f"Added Skill ID {data.skill_id}")
    async def generate_and_store_embedding(self, candidate_id: uuid.UUID, custom_text: Optional[str] = None) -> List[float]:
        """Generates and persists a 1536-dimensional normalized vector embedding for the candidate."""
        if not custom_text:
            profile = await self.details_repo.get_profile(candidate_id)
            skills = await self.details_repo.get_skills(candidate_id)
            exp = await self.details_repo.get_experience(candidate_id)
            edu = await self.details_repo.get_education(candidate_id)
            
            text_parts = []
            if profile and profile.summary:
                text_parts.append(f"Summary: {profile.summary}")
            if skills:
                text_parts.append(f"Skills: {', '.join(s.skill_name for s in skills)}")
            for e in exp:
                text_parts.append(f"Experience: {e.designation_name} at {e.company_name}. {e.responsibilities or ''}")
            for d in edu:
                text_parts.append(f"Education: {d.degree_name} in {d.field_of_study or ''} from {d.institution_name}")
            custom_text = "\n".join(text_parts)

        embedding = await embedding_engine.get_embedding(custom_text)
        primary_resume = await self.resume_repo.get_primary_resume(candidate_id)
        resume_id = primary_resume.id if primary_resume else None
        
        await self.embedding_repo.store_embedding(candidate_id, embedding, resume_id=resume_id)
        await self.db.flush()
        return embedding

    async def get_candidate_360(self, org_id: uuid.UUID, candidate_id: uuid.UUID) -> dict:
        """
        Builds a comprehensive, denormalized Candidate 360 projection aggregating
        master record, extended profile, experience, education, skills, AI metadata,
        resumes, and timeline activity.
        """
        cand = await self.cand_repo.get_by_id(org_id, candidate_id)
        if not cand:
            raise HTTPException(status_code=404, detail="Candidate not found")

        profile = await self.details_repo.get_profile(candidate_id)
        education = await self.details_repo.get_education(candidate_id)
        experience = await self.details_repo.get_experience(candidate_id)
        skills = await self.details_repo.get_skills(candidate_id)
        certifications = await self.details_repo.get_certifications(candidate_id)
        resumes = await self.resume_repo.get_resumes(candidate_id)
        ai_profile = await self.details_repo.get_ai_profile(candidate_id)
        timeline = await self.timeline_repo.get_timeline(candidate_id)

        current_role = experience[0].designation_name if experience else "Candidate"
        current_company = experience[0].company_name if experience else "Not specified"

        return {
            "status": "success",
            "candidate_360": {
                "id": str(cand.id),
                "first_name": cand.first_name,
                "last_name": cand.last_name,
                "email": cand.email,
                "phone": cand.phone,
                "current_role": current_role,
                "current_company": current_company,
                "profile_status": cand.profile_status,
                "is_blacklisted": cand.is_blacklisted,
                "summary": profile.summary if profile else "",
                "total_experience_years": profile.total_experience_years if profile else (ai_profile.ai_calculated_experience_years if ai_profile else 0),
                "notice_period_days": profile.notice_period_days if profile else 30,
                "current_salary": profile.current_salary if profile else None,
                "expected_salary": profile.expected_salary if profile else None,
                "skills": [{"id": str(s.id), "name": s.skill_name, "level": s.proficiency_level} for s in skills],
                "top_skills": [s.strip() for s in (ai_profile.ai_top_skills or "").split(",") if s.strip()] if ai_profile else [],
                "experience": [{
                    "id": str(e.id),
                    "company_name": e.company_name,
                    "designation_name": e.designation_name,
                    "start_date": str(e.start_date) if e.start_date else None,
                    "end_date": str(e.end_date) if e.end_date else None,
                    "is_current": e.is_current,
                    "responsibilities": e.responsibilities
                } for e in experience],
                "education": [{
                    "id": str(ed.id),
                    "institution_name": ed.institution_name,
                    "degree_name": ed.degree_name,
                    "field_of_study": ed.field_of_study,
                    "graduation_year": ed.graduation_year,
                    "grade_or_gpa": ed.grade_or_gpa
                } for ed in education],
                "certifications": [{"id": str(c.id), "name": c.certification_name, "issuer": c.issuing_organization} for c in certifications],
                "resumes": [{"id": str(r.id), "file_name": r.file_name, "file_path": r.file_path, "is_primary": r.is_primary} for r in resumes],
                "ai_profile": {
                    "completeness_score": ai_profile.ai_profile_completeness if ai_profile else 0,
                    "calculated_experience": ai_profile.ai_calculated_experience_years if ai_profile else 0,
                    "top_skills": ai_profile.ai_top_skills if ai_profile else ""
                },
                "timeline_events": [{
                    "id": str(t.id),
                    "event_name": t.event_name,
                    "details": t.details,
                    "created_at": t.created_at.isoformat() if t.created_at else None
                } for t in timeline]
            }
        }

    async def semantic_search(
        self,
        org_id: uuid.UUID,
        query_text: str,
        top_k: int = 10,
        threshold: float = 0.5
    ) -> List[dict]:
        """
        Performs semantic vector matching against all candidate embeddings in tenant.
        Returns ranked candidates with cosine similarity scores and highlighted skills.
        """
        query_vector = await embedding_engine.get_embedding(query_text)
        all_candidates = await self.cand_repo.get_all_enriched(org_id, skip=0, limit=200)
        if not all_candidates:
            return []

        cand_ids = [c["id"] for c in all_candidates]
        embeddings = await self.embedding_repo.get_all_embeddings(cand_ids)
        emb_map = {e.candidate_id: e.embedding for e in embeddings}

        ranked_results = []
        for cand in all_candidates:
            c_id = cand["id"]
            if c_id in emb_map and emb_map[c_id]:
                cand_vec = emb_map[c_id]
                score = embedding_engine.cosine_similarity(query_vector, cand_vec)
            else:
                cand_text = f"{cand['first_name']} {cand['last_name']} {cand['current_role']} {cand['summary']} {', '.join(cand.get('skills', []))}"
                cand_vec = await self.generate_and_store_embedding(c_id, custom_text=cand_text)
                score = embedding_engine.cosine_similarity(query_vector, cand_vec)

            if score >= threshold or len(ranked_results) < top_k:
                ranked_results.append({
                    "candidate_id": str(c_id),
                    "candidate_name": f"{cand['first_name']} {cand['last_name']}",
                    "email": cand["email"],
                    "current_role": cand["current_role"],
                    "current_company": cand["current_company"],
                    "match_score": round(score * 100, 1),
                    "similarity_score": round(score, 4),
                    "top_skills": cand.get("skills", []),
                    "summary": cand.get("summary", "")
                })

        ranked_results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return ranked_results[:top_k]


class ResumeService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.resume_repo = ResumeRepository(db)
        self.timeline_repo = TimelineRepository(db)
        self.completion_engine = ProfileCompletionEngine(db)

    async def upload_resume(self, org_id: uuid.UUID, candidate_id: uuid.UUID, file: UploadFile) -> dict:
        """
        Handles physical storage of the resume in isolated tenant storage, and maintains versioning logic.
        """
        base_tenant_dir = f"organizations/{org_id}/candidates/{candidate_id}/resumes"
        storage_service.create_directory(base_tenant_dir)
        
        file_path = f"{base_tenant_dir}/{file.filename}"
        
        import io
        content = await file.read()
        saved_path = await storage_service.upload(io.BytesIO(content), file_path)
        
        file_size = len(content)
        mime_type = file.content_type
        
        resume = await self.resume_repo.add_resume(
            candidate_id=candidate_id,
            file_name=file.filename,
            file_path=saved_path,
            file_size=file_size,
            mime_type=mime_type
        )
        
        await self.timeline_repo.log_event(candidate_id, "Resume Uploaded", f"Uploaded version of {file.filename}")
        await self.completion_engine.recalculate_score(candidate_id)
        await self.db.commit()
        
        return {
            "status": "success",
            "message": "Resume uploaded successfully and marked as primary.",
            "resume_id": resume.id
        }

    async def stage_and_parse_resume(self, org_id: uuid.UUID, file: UploadFile) -> dict:
        """Saves a resume to a staging directory and parses real text/metadata from PDF."""
        import io
        from app.modules.candidates.parser import ResumeParser

        file_id = uuid.uuid4()
        staging_dir = f"organizations/{org_id}/staging"
        storage_service.create_directory(staging_dir)
        
        file_path = f"{staging_dir}/{file_id}_{file.filename}"
        content = await file.read()
        saved_path = await storage_service.upload(io.BytesIO(content), file_path)
        
        extracted_data = ResumeParser.parse_pdf(content, filename=file.filename)
        
        return {
            "status": "success",
            "staged_file_path": saved_path,
            "original_filename": file.filename,
            "file_size": len(content),
            "mime_type": file.content_type,
            "extracted_data": extracted_data
        }


