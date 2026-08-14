import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func, or_

from app.modules.recruitment.models import (
    HiringPlan, HiringRequest, Job, JobSkill, JobSalaryRange, JobRecruiter, JobHiringManager,
    RecruitmentPipeline, RecruitmentStage, PipelineStageMapping,
    CandidateApplication, ApplicationStageHistory, ApplicationNote, RecruitmentAuditLog
)
from app.modules.recruitment.schemas import (
    HiringPlanCreate, HiringRequestCreate, JobCreate, PipelineCreate, StageCreate, CandidateApplicationCreate
)

class HiringPlanRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_plan(self, org_id: uuid.UUID, data: HiringPlanCreate) -> HiringPlan:
        plan = HiringPlan(**data.model_dump(), organization_id=org_id)
        self.db.add(plan)
        await self.db.flush()
        return plan

    async def get_plans(self, org_id: uuid.UUID) -> List[HiringPlan]:
        stmt = select(HiringPlan).where(HiringPlan.organization_id == org_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def create_request(self, org_id: uuid.UUID, user_id: uuid.UUID, data: HiringRequestCreate) -> HiringRequest:
        req = HiringRequest(
            **data.model_dump(),
            organization_id=org_id,
            requested_by=user_id,
            status="Approved" # Default approved for testing
        )
        self.db.add(req)
        await self.db.flush()
        return req


class JobRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_job(self, org_id: uuid.UUID, data: JobCreate) -> Job:
        job_data = data.model_dump(exclude={"skills", "salary_range", "recruiter_ids", "hiring_manager_ids"})
        job = Job(**job_data, organization_id=org_id, status="Published")
        self.db.add(job)
        await self.db.flush()

        # Add Skills
        for s in data.skills:
            js = JobSkill(job_id=job.id, skill_id=s.skill_id, is_mandatory=s.is_mandatory, proficiency_required=s.proficiency_required)
            self.db.add(js)

        # Add Salary Range
        if data.salary_range:
            sr = JobSalaryRange(job_id=job.id, **data.salary_range.model_dump())
            self.db.add(sr)

        # Add Recruiters
        for r_id in data.recruiter_ids:
            jr = JobRecruiter(job_id=job.id, recruiter_id=r_id, is_primary=True)
            self.db.add(jr)

        await self.db.flush()
        return job

    async def get_by_id(self, org_id: uuid.UUID, job_id: uuid.UUID) -> Optional[Job]:
        stmt = select(Job).where(Job.id == job_id, Job.organization_id == org_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_all_jobs(self, org_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Job]:
        stmt = select(Job).where(Job.organization_id == org_id).offset(skip).limit(limit)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def get_job_skills(self, job_id: uuid.UUID) -> List[JobSkill]:
        stmt = select(JobSkill).where(JobSkill.job_id == job_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())


class PipelineRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_stage(self, org_id: uuid.UUID, data: StageCreate) -> RecruitmentStage:
        stage = RecruitmentStage(**data.model_dump(), organization_id=org_id)
        self.db.add(stage)
        await self.db.flush()
        return stage

    async def get_stages(self, org_id: uuid.UUID) -> List[RecruitmentStage]:
        stmt = select(RecruitmentStage).where(RecruitmentStage.organization_id == org_id).order_by(RecruitmentStage.sequence_number)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def create_pipeline(self, org_id: uuid.UUID, data: PipelineCreate) -> RecruitmentPipeline:
        pipeline = RecruitmentPipeline(
            organization_id=org_id,
            pipeline_name=data.pipeline_name,
            description=data.description
        )
        self.db.add(pipeline)
        await self.db.flush()

        for idx, stage_id in enumerate(data.stage_ids):
            mapping = PipelineStageMapping(
                pipeline_id=pipeline.id,
                stage_id=stage_id,
                sequence_number=idx + 1
            )
            self.db.add(mapping)
        await self.db.flush()
        return pipeline

    async def get_pipeline(self, org_id: uuid.UUID, pipeline_id: uuid.UUID) -> Optional[RecruitmentPipeline]:
        stmt = select(RecruitmentPipeline).where(RecruitmentPipeline.id == pipeline_id, RecruitmentPipeline.organization_id == org_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_pipeline_stages(self, pipeline_id: uuid.UUID) -> List[RecruitmentStage]:
        stmt = select(RecruitmentStage).join(PipelineStageMapping).where(
            PipelineStageMapping.pipeline_id == pipeline_id
        ).order_by(PipelineStageMapping.sequence_number)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())


class ApplicationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_application(self, data: CandidateApplicationCreate, first_stage_id: Optional[uuid.UUID] = None) -> CandidateApplication:
        app = CandidateApplication(
            job_id=data.job_id,
            candidate_id=data.candidate_id,
            pipeline_id=data.pipeline_id,
            current_stage_id=first_stage_id,
            application_status="Applied"
        )
        self.db.add(app)
        await self.db.flush()

        if first_stage_id:
            history = ApplicationStageHistory(
                application_id=app.id,
                from_stage_id=None,
                to_stage_id=first_stage_id,
                changed_by=uuid.UUID("00000000-0000-0000-0000-000000000000") # System
            )
            self.db.add(history)
            await self.db.flush()

        return app

    async def get_by_id(self, application_id: uuid.UUID) -> Optional[CandidateApplication]:
        stmt = select(CandidateApplication).where(CandidateApplication.id == application_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def update_stage(self, application_id: uuid.UUID, from_stage_id: Optional[uuid.UUID], to_stage_id: uuid.UUID, status: str, user_id: uuid.UUID) -> CandidateApplication:
        stmt = update(CandidateApplication).where(CandidateApplication.id == application_id).values(
            current_stage_id=to_stage_id,
            application_status=status
        )
        await self.db.execute(stmt)

        history = ApplicationStageHistory(
            application_id=application_id,
            from_stage_id=from_stage_id,
            to_stage_id=to_stage_id,
            changed_by=user_id
        )
        self.db.add(history)
        await self.db.flush()
        return await self.get_by_id(application_id)

    async def count_by_stage(self, org_id: uuid.UUID) -> List[Dict[str, Any]]:
        stmt = select(
            RecruitmentStage.stage_name,
            func.count(CandidateApplication.id).label("count")
        ).join(
            CandidateApplication, CandidateApplication.current_stage_id == RecruitmentStage.id
        ).where(
            RecruitmentStage.organization_id == org_id
        ).group_by(RecruitmentStage.stage_name)
        res = await self.db.execute(stmt)
        return [{"stage_name": r[0], "candidate_count": r[1]} for r in res.all()]

    async def get_metrics(self, org_id: uuid.UUID) -> Dict[str, int]:
        jobs_stmt = select(func.count(Job.id)).where(Job.organization_id == org_id)
        apps_stmt = select(func.count(CandidateApplication.id)).join(Job).where(Job.organization_id == org_id)
        
        jobs_res = await self.db.execute(jobs_stmt)
        apps_res = await self.db.execute(apps_stmt)
        
        return {
            "total_open_jobs": jobs_res.scalar() or 0,
            "total_applications": apps_res.scalar() or 0
        }
