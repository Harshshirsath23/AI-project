from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any
import uuid
from datetime import date, datetime

# -------------------------
# Hiring Plans & Requisitions
# -------------------------
class HiringPlanBase(BaseModel):
    plan_name: str = Field(..., max_length=150)
    budget: float = Field(default=0.0, ge=0.0)
    currency_id: Optional[uuid.UUID] = None
    start_date: date
    end_date: date

class HiringPlanCreate(HiringPlanBase):
    pass

class HiringPlanResponse(HiringPlanBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class HiringRequestBase(BaseModel):
    requisition_number: str = Field(..., max_length=50)
    title: str = Field(..., max_length=200)
    department_id: uuid.UUID
    designation_id: uuid.UUID
    open_positions: int = Field(default=1, ge=1)
    target_date: Optional[date] = None
    justification: Optional[str] = None
    hiring_plan_id: Optional[uuid.UUID] = None

class HiringRequestCreate(HiringRequestBase):
    pass

class HiringRequestResponse(HiringRequestBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    status: str
    requested_by: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# -------------------------
# Job Management
# -------------------------
class JobSkillCreate(BaseModel):
    skill_id: uuid.UUID
    is_mandatory: bool = True
    proficiency_required: Optional[str] = None

class JobSalaryRangeCreate(BaseModel):
    minimum_salary: float = 0.0
    maximum_salary: float = 0.0
    currency_id: Optional[uuid.UUID] = None

class JobBase(BaseModel):
    title: str = Field(..., max_length=200)
    job_code: str = Field(..., max_length=50)
    description: str
    department_id: Optional[uuid.UUID] = None
    designation_id: Optional[uuid.UUID] = None
    employment_type_id: Optional[uuid.UUID] = None
    work_mode_id: Optional[uuid.UUID] = None
    experience_level_id: Optional[uuid.UUID] = None
    open_positions: int = 1
    opening_date: Optional[date] = None
    closing_date: Optional[date] = None
    application_deadline: Optional[date] = None

class JobCreate(JobBase):
    hiring_request_id: Optional[uuid.UUID] = None
    skills: List[JobSkillCreate] = []
    salary_range: Optional[JobSalaryRangeCreate] = None
    recruiter_ids: List[uuid.UUID] = []
    hiring_manager_ids: List[uuid.UUID] = []

class JobResponse(JobBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class FullJobDetailsResponse(BaseModel):
    job: JobResponse
    skills: List[JobSkillCreate] = []
    salary_range: Optional[JobSalaryRangeCreate] = None
    recruiters: List[uuid.UUID] = []
    hiring_managers: List[uuid.UUID] = []

# -------------------------
# Recruitment Pipelines & Stages
# -------------------------
class RecruitmentStageBase(BaseModel):
    stage_name: str = Field(..., max_length=100)
    sequence_number: int

class RecruitmentStageCreate(RecruitmentStageBase):
    pass

class StageCreate(RecruitmentStageCreate):
    pass

class RecruitmentStageResponse(RecruitmentStageBase):
    id: uuid.UUID
    organization_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

class RecruitmentPipelineBase(BaseModel):
    pipeline_name: str = Field(..., max_length=150)
    description: Optional[str] = None

class RecruitmentPipelineCreate(RecruitmentPipelineBase):
    stage_ids: List[uuid.UUID] = []

class PipelineCreate(RecruitmentPipelineCreate):
    pass

class RecruitmentPipelineResponse(RecruitmentPipelineBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    stages: List[RecruitmentStageResponse] = []

    model_config = ConfigDict(from_attributes=True)

class PipelineResponse(RecruitmentPipelineResponse):
    pass

# -------------------------
# Candidate Applications & Transitions
# -------------------------
class CandidateApplicationCreate(BaseModel):
    job_id: uuid.UUID
    candidate_id: uuid.UUID
    pipeline_id: Optional[uuid.UUID] = None

class CandidateApplicationResponse(BaseModel):
    id: uuid.UUID
    job_id: uuid.UUID
    candidate_id: uuid.UUID
    pipeline_id: Optional[uuid.UUID] = None
    current_stage_id: Optional[uuid.UUID] = None
    application_status: str
    applied_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ApplicationTransitionRequest(BaseModel):
    to_stage_id: uuid.UUID
    notes: Optional[str] = None
    trigger_automation_hook: bool = True

class ApplicationTransitionResponse(BaseModel):
    application_id: uuid.UUID
    from_stage_id: Optional[uuid.UUID] = None
    to_stage_id: uuid.UUID
    application_status: str
    transitioned_at: datetime
    automation_hook_status: Optional[str] = "HOOK_DISPATCHED_TO_LANGGRAPH"

# -------------------------
# Rule-Based Candidate Matching
# -------------------------
class MatchScoreBreakdown(BaseModel):
    skill_score: float
    experience_score: float
    education_score: float
    location_score: float
    overall_match_score: float

class CandidateMatchRequest(BaseModel):
    candidate_id: uuid.UUID
    job_id: uuid.UUID

class CandidateMatchResponse(BaseModel):
    candidate_id: uuid.UUID
    job_id: uuid.UUID
    compatibility_score: float
    breakdown: MatchScoreBreakdown
    passed_rules: bool

# -------------------------
# Recruitment Dashboard & Metrics
# -------------------------
class StageCountMetric(BaseModel):
    stage_name: str
    candidate_count: int

class RecruitmentDashboardResponse(BaseModel):
    total_open_jobs: int
    total_applications: int
    total_hires: int
    pipeline_distribution: List[StageCountMetric] = []
    average_time_to_hire_days: float = 0.0
