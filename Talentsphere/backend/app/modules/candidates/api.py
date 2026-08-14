from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any
import uuid

from app.database.session import get_async_db
from app.modules.auth.dependencies import get_current_organization, require_permission
from app.modules.candidates.schemas import (
    CandidateCreate, CandidateResponse, CandidateEducationCreate,
    CandidateExperienceCreate, CandidateSkillCreate, CandidateSearchRequest,
    FullCandidateProfileResponse, CandidateCreateFromStaged, FullCandidateSummaryResponse,
    CandidateSemanticSearchRequest
)
from app.modules.candidates.service import CandidateService, ResumeService
from app.modules.candidates.repository import CandidateRepository, CandidateDetailsRepository, ResumeRepository

router = APIRouter(tags=["Candidate Management"])

# -----------------------------
# Core Candidate Management
# -----------------------------

@router.get("/", response_model=List[FullCandidateSummaryResponse], summary="List All Candidates", dependencies=[Depends(require_permission("candidate:read"))])
async def list_candidates(
    skip: int = 0,
    limit: int = 100,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Retrieves a paginated list of all enriched candidates for the tenant."""
    repo = CandidateRepository(db)
    return await repo.get_all_enriched(org_id, skip, limit)

@router.post("/upload", summary="Upload Resume PDF & Parse Candidate", description="Uploads a PDF resume, parses candidate name, email, phone number, creates the candidate record, and moves the resume to isolated tenant storage.", dependencies=[Depends(require_permission("candidate:write"))])
async def upload_resume_and_create_candidate(
    file: UploadFile = File(...),
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Parses real candidate info from uploaded resume PDF and creates candidate automatically."""
    service = CandidateService(db)
    return await service.upload_and_create_candidate(org_id, file)

@router.post("/parse", summary="Parse Resume PDF", description="Uploads a PDF resume and extracts candidate data without creating the candidate record.", dependencies=[Depends(require_permission("candidate:write"))])
async def parse_resume(
    file: UploadFile = File(...),
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Parses real candidate info from uploaded resume PDF to be reviewed on the frontend before creation."""
    resume_service = ResumeService(db)
    return await resume_service.stage_and_parse_resume(org_id, file)

@router.post("/from-staged", summary="Create Candidate from Staged Resume", description="Creates a candidate record from a previously staged resume, including extracted/reviewed skills, experiences, and summary.", dependencies=[Depends(require_permission("candidate:write"))])
async def create_candidate_from_staged(
    data: CandidateCreateFromStaged,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Creates candidate from staged resume payload after user review in frontend."""
    service = CandidateService(db)
    return await service.create_candidate_from_staged(org_id, data)

@router.post("/", summary="Create Candidate Manually", description="Creates a candidate manually using a JSON payload.", dependencies=[Depends(require_permission("candidate:write"))])
async def create_candidate(
    data: CandidateCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Creates a candidate record manually from JSON data."""
    service = CandidateService(db)
    return await service.create_candidate(org_id, data)

@router.post("/search", response_model=List[CandidateResponse], summary="Enterprise Candidate Search", dependencies=[Depends(require_permission("candidate:read"))])
async def search_candidates(
    req: CandidateSearchRequest,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Boolean and parametric search across candidate profiles."""
    service = CandidateService(db)
    return await service.search(org_id, req)

@router.get("/{candidate_id}", response_model=FullCandidateProfileResponse, summary="Get Full Candidate Profile", dependencies=[Depends(require_permission("candidate:read"))])
async def get_candidate_profile(
    candidate_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Returns the full aggregated candidate profile including education, experience, skills, and resumes."""
    repo = CandidateRepository(db)
    details_repo = CandidateDetailsRepository(db)
    resume_repo = ResumeRepository(db)
    
    cand = await repo.get_by_id(org_id, candidate_id)
    if not cand:
        raise HTTPException(status_code=404, detail="Candidate not found")
        
    ai_profile = await details_repo.get_ai_profile(candidate_id)
    edu = await details_repo.get_education(candidate_id)
    exp = await details_repo.get_experience(candidate_id)
    skills = await details_repo.get_skills(candidate_id)
    resumes = await resume_repo.get_resumes(candidate_id)
    
    return FullCandidateProfileResponse(
        candidate=cand,
        education=edu,
        experience=exp,
        skills=skills,
        resumes=resumes,
        ai_profile=ai_profile
    )

# -----------------------------
# Detailed Sections
# -----------------------------

@router.post("/{candidate_id}/education", summary="Add Education", dependencies=[Depends(require_permission("candidate:write"))])
async def add_education(
    candidate_id: uuid.UUID,
    data: CandidateEducationCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Appends education record to candidate profile."""
    service = CandidateService(db)
    return await service.add_education(org_id, candidate_id, data)

@router.post("/{candidate_id}/experience", summary="Add Experience", dependencies=[Depends(require_permission("candidate:write"))])
async def add_experience(
    candidate_id: uuid.UUID,
    data: CandidateExperienceCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Appends work experience record to candidate profile."""
    service = CandidateService(db)
    return await service.add_experience(org_id, candidate_id, data)

@router.post("/{candidate_id}/skills", summary="Add Skill", dependencies=[Depends(require_permission("candidate:write"))])
async def add_skill(
    candidate_id: uuid.UUID,
    data: CandidateSkillCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Appends skill to candidate profile."""
    service = CandidateService(db)
    return await service.add_skill(org_id, candidate_id, data)

@router.post("/{candidate_id}/resume", summary="Upload Candidate Resume File", dependencies=[Depends(require_permission("candidate:write"))])
async def upload_candidate_resume(
    candidate_id: uuid.UUID,
    file: UploadFile = File(...),
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Uploads resume file for an existing candidate record."""
    resume_service = ResumeService(db)
    return await resume_service.upload_resume(org_id, candidate_id, file)

@router.get("/{candidate_id}/360", summary="Get Candidate 360 Projection", description="Returns denormalized full candidate 360 projection for sub-50ms rich profile visualization.", dependencies=[Depends(require_permission("candidate:read"))])
async def get_candidate_360(
    candidate_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Retrieves full denormalized Candidate 360 profile."""
    service = CandidateService(db)
    return await service.get_candidate_360(org_id, candidate_id)

@router.post("/semantic-search", summary="Vector Semantic Search", description="Natural-language vector similarity search against tenant candidate pool using 1536-dimensional embeddings.", dependencies=[Depends(require_permission("candidate:read"))])
async def semantic_search_candidates(
    req: CandidateSemanticSearchRequest,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Executes pgvector cosine similarity search across candidates."""
    service = CandidateService(db)
    return await service.semantic_search(
        org_id=org_id,
        query_text=req.query,
        top_k=req.top_k,
        threshold=req.threshold
    )

@router.delete("/{candidate_id}", summary="Delete Candidate", dependencies=[Depends(require_permission("candidate:write"))])
async def delete_candidate(
    candidate_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Removes a candidate record."""
    service = CandidateService(db)
    return await service.delete_candidate(org_id, candidate_id)
