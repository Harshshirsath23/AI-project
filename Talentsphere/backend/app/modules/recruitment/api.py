from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from app.database.session import get_async_db
from app.modules.auth.dependencies import get_current_organization, get_current_user, require_permission
from app.modules.recruitment.schemas import (
    HiringPlanCreate, HiringPlanResponse, HiringRequestCreate,
    JobCreate, JobResponse, PipelineCreate, PipelineResponse, StageCreate, RecruitmentStageResponse,
    CandidateApplicationCreate, CandidateApplicationResponse, ApplicationTransitionRequest, ApplicationTransitionResponse,
    CandidateMatchRequest, CandidateMatchResponse, RecruitmentDashboardResponse
)
from app.modules.recruitment.service import RecruitmentService

router = APIRouter(tags=["Recruitment & Workflow Management"])

# -----------------------------
# Hiring Plans & Requisitions
# -----------------------------
@router.post("/hiring-plans", summary="Create Hiring Plan", dependencies=[Depends(require_permission("hiring_plans:manage"))])
async def create_hiring_plan(
    data: HiringPlanCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    service = RecruitmentService(db)
    return await service.create_hiring_plan(org_id, data)

@router.get("/hiring-plans", response_model=List[HiringPlanResponse], summary="List Hiring Plans", dependencies=[Depends(require_permission("hiring_plans:manage"))])
async def list_hiring_plans(
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    service = RecruitmentService(db)
    return await service.get_hiring_plans(org_id)

@router.post("/requisitions", summary="Create Job Requisition", dependencies=[Depends(require_permission("hiring_plans:manage"))])
async def create_hiring_request(
    data: HiringRequestCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    service = RecruitmentService(db)
    return await service.create_hiring_request(org_id, current_user.id, data)

# -----------------------------
# Job Requisitions & Postings
# -----------------------------
@router.post("/jobs", summary="Create and Publish Job", dependencies=[Depends(require_permission("jobs:write"))])
async def create_job(
    data: JobCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    service = RecruitmentService(db)
    return await service.create_job(org_id, data)

@router.get("/jobs", response_model=List[JobResponse], summary="List All Jobs", dependencies=[Depends(require_permission("jobs:read"))])
async def list_jobs(
    skip: int = 0,
    limit: int = 100,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    service = RecruitmentService(db)
    return await service.get_jobs(org_id, skip, limit)

@router.get("/jobs/{job_id}", response_model=JobResponse, summary="Get Job Details", dependencies=[Depends(require_permission("jobs:read"))])
async def get_job_by_id(
    job_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    service = RecruitmentService(db)
    return await service.get_job_by_id(org_id, job_id)

# -----------------------------
# Workflow Pipeline Builder
# -----------------------------
@router.post("/stages", response_model=RecruitmentStageResponse, summary="Create Workflow Stage", dependencies=[Depends(require_permission("pipelines:manage"))])
async def create_stage(
    data: StageCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    service = RecruitmentService(db)
    res = await service.create_stage(org_id, data)
    repo = service.pipeline_repo
    stages = await repo.get_stages(org_id)
    return [s for s in stages if s.id == res["stage_id"]][0]

@router.get("/stages", response_model=List[RecruitmentStageResponse], summary="List Workflow Stages", dependencies=[Depends(require_permission("pipelines:manage"))])
async def list_stages(
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    service = RecruitmentService(db)
    return await service.get_stages(org_id)

@router.post("/pipelines", summary="Create Recruitment Pipeline Template", dependencies=[Depends(require_permission("pipelines:manage"))])
async def create_pipeline(
    data: PipelineCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    service = RecruitmentService(db)
    return await service.create_pipeline(org_id, data)

# -----------------------------
# Candidate Applications & Transitions
# -----------------------------
@router.post("/applications", summary="Apply Candidate to Job", dependencies=[Depends(require_permission("applications:manage"))])
async def apply_candidate(
    data: CandidateApplicationCreate,
    db: AsyncSession = Depends(get_async_db)
):
    service = RecruitmentService(db)
    return await service.apply_to_job(data)

@router.post("/applications/{application_id}/move", response_model=ApplicationTransitionResponse, summary="Advance Candidate Stage (Workflow Engine)", dependencies=[Depends(require_permission("applications:manage"))])
async def move_application_stage(
    application_id: uuid.UUID,
    req: ApplicationTransitionRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    service = RecruitmentService(db)
    return await service.advance_application_stage(application_id, current_user.id, req)

# -----------------------------
# Matching & Analytics Dashboard
# -----------------------------
@router.post("/matching/score", response_model=CandidateMatchResponse, summary="Rule-Based Candidate Match Score", dependencies=[Depends(require_permission("jobs:read"))])
async def match_candidate(
    req: CandidateMatchRequest,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    service = RecruitmentService(db)
    return await service.match_candidate(org_id, req.candidate_id, req.job_id)

@router.get("/dashboard", response_model=RecruitmentDashboardResponse, summary="Recruitment Analytics Dashboard", dependencies=[Depends(require_permission("reports:view"))])
async def get_recruitment_dashboard(
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    service = RecruitmentService(db)
    return await service.get_dashboard(org_id)
