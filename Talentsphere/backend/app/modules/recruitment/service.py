import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.modules.recruitment.repository import (
    HiringPlanRepository, JobRepository, PipelineRepository, ApplicationRepository
)
from app.modules.recruitment.schemas import (
    HiringPlanCreate, HiringRequestCreate, JobCreate, PipelineCreate, StageCreate, CandidateApplicationCreate,
    ApplicationTransitionRequest, ApplicationTransitionResponse, CandidateMatchResponse, RecruitmentDashboardResponse
)
from app.modules.recruitment.workflow_engine import WorkflowEngine
from app.modules.recruitment.matching_engine import CandidateMatchingEngine
from app.modules.recruitment.dashboard import RecruitmentDashboardService

class RecruitmentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.plan_repo = HiringPlanRepository(db)
        self.job_repo = JobRepository(db)
        self.pipeline_repo = PipelineRepository(db)
        self.app_repo = ApplicationRepository(db)
        self.workflow_engine = WorkflowEngine(db)
        self.matching_engine = CandidateMatchingEngine(db)
        self.dashboard_service = RecruitmentDashboardService(db)

    # -------------------------
    # Hiring Plans & Requisitions
    # -------------------------
    async def create_hiring_plan(self, org_id: uuid.UUID, data: HiringPlanCreate) -> dict:
        plan = await self.plan_repo.create_plan(org_id, data)
        await self.db.commit()
        return {"status": "success", "hiring_plan_id": plan.id, "message": "Hiring plan created successfully"}

    async def get_hiring_plans(self, org_id: uuid.UUID) -> List[Any]:
        return await self.plan_repo.get_plans(org_id)

    async def create_hiring_request(self, org_id: uuid.UUID, user_id: uuid.UUID, data: HiringRequestCreate) -> dict:
        req = await self.plan_repo.create_request(org_id, user_id, data)
        await self.db.commit()
        return {"status": "success", "requisition_id": req.id, "message": "Job requisition created successfully"}

    # -------------------------
    # Jobs
    # -------------------------
    async def create_job(self, org_id: uuid.UUID, data: JobCreate) -> dict:
        job = await self.job_repo.create_job(org_id, data)
        await self.db.commit()
        return {"status": "success", "job_id": job.id, "message": "Job published successfully"}

    async def get_jobs(self, org_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Any]:
        return await self.job_repo.get_all_jobs(org_id, skip, limit)

    async def get_job_by_id(self, org_id: uuid.UUID, job_id: uuid.UUID) -> Any:
        job = await self.job_repo.get_by_id(org_id, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job

    # -------------------------
    # Pipelines & Stages
    # -------------------------
    async def create_stage(self, org_id: uuid.UUID, data: StageCreate) -> dict:
        stage = await self.pipeline_repo.create_stage(org_id, data)
        await self.db.commit()
        return {"status": "success", "stage_id": stage.id, "message": "Workflow stage created successfully"}

    async def get_stages(self, org_id: uuid.UUID) -> List[Any]:
        return await self.pipeline_repo.get_stages(org_id)

    async def create_pipeline(self, org_id: uuid.UUID, data: PipelineCreate) -> dict:
        pipeline = await self.pipeline_repo.create_pipeline(org_id, data)
        await self.db.commit()
        return {"status": "success", "pipeline_id": pipeline.id, "message": "Recruitment pipeline created successfully"}

    # -------------------------
    # Candidate Applications & Workflow
    # -------------------------
    async def apply_to_job(self, data: CandidateApplicationCreate) -> dict:
        # Determine first stage of pipeline if provided
        first_stage_id = None
        if data.pipeline_id:
            stages = await self.pipeline_repo.get_pipeline_stages(data.pipeline_id)
            if stages:
                first_stage_id = stages[0].id

        app = await self.app_repo.create_application(data, first_stage_id)
        await self.db.commit()
        return {"status": "success", "application_id": app.id, "message": "Candidate applied to job successfully"}

    async def advance_application_stage(self, application_id: uuid.UUID, user_id: uuid.UUID, req: ApplicationTransitionRequest) -> ApplicationTransitionResponse:
        res = await self.workflow_engine.execute_stage_transition(
            application_id=application_id,
            to_stage_id=req.to_stage_id,
            user_id=user_id,
            notes=req.notes,
            trigger_hook=req.trigger_automation_hook
        )
        await self.db.commit()
        return ApplicationTransitionResponse(**res)

    # -------------------------
    # Candidate Matching & Dashboard
    # -------------------------
    async def match_candidate(self, org_id: uuid.UUID, candidate_id: uuid.UUID, job_id: uuid.UUID) -> CandidateMatchResponse:
        return await self.matching_engine.calculate_match_score(org_id, candidate_id, job_id)

    async def get_dashboard(self, org_id: uuid.UUID) -> RecruitmentDashboardResponse:
        return await self.dashboard_service.get_dashboard_metrics(org_id)
