from sqlalchemy import Column, String, Integer, ForeignKey, Date, Float, TEXT, Boolean, DateTime, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import UserDefinedType
import uuid
from datetime import datetime
from app.core.models import Base, AuditMixin

# Custom type to support pgvector Vector type
class VectorType(UserDefinedType):
    def __init__(self, dim=1536):
        self.dim = dim
        
    def get_col_spec(self, **kw):
        return f"VECTOR({self.dim})"

# -------------------------
# Workforce Planning
# -------------------------
class HiringPlan(AuditMixin, Base):
    __tablename__ = "hiring_plans"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    plan_name: Mapped[str] = mapped_column(String(150))
    budget: Mapped[float] = mapped_column(Float, default=0.0)
    currency_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    start_date: Mapped[Date] = mapped_column(Date)
    end_date: Mapped[Date] = mapped_column(Date)

class HiringRequest(AuditMixin, Base):
    __tablename__ = "hiring_requests"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    hiring_plan_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("hiring_plans.id"), nullable=True)
    requisition_number: Mapped[str] = mapped_column(String(50)) # unique code
    title: Mapped[str] = mapped_column(String(200))
    department_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # references departments
    designation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # references designations
    requested_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # references users
    open_positions: Mapped[int] = mapped_column(Integer, default=1)
    target_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(30)) # Draft, Submitted, Pending Approval, Approved, Rejected, Converted to Job
    justification: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    __table_args__ = (UniqueConstraint('organization_id', 'requisition_number', name='uq_org_requisition'),)

class HiringRequestAttachment(AuditMixin, Base):
    __tablename__ = "hiring_request_attachments"
    hiring_request_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("hiring_requests.id"))
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(500))

class HiringRequestComment(AuditMixin, Base):
    __tablename__ = "hiring_request_comments"
    hiring_request_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("hiring_requests.id"))
    commented_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # user
    comment_text: Mapped[str] = mapped_column(TEXT)
    commented_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

# -------------------------
# Job Management
# -------------------------
class JobTemplate(AuditMixin, Base):
    __tablename__ = "job_templates"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(TEXT)
    requirements: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    benefits: Mapped[str | None] = mapped_column(TEXT, nullable=True)

class Job(AuditMixin, Base):
    __tablename__ = "jobs"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    hiring_request_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("hiring_requests.id"), nullable=True)
    job_code: Mapped[str] = mapped_column(String(50)) # unique code
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(TEXT)
    department_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # References Department
    designation_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # References Designation
    employment_type_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # References EmploymentType
    work_mode_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # References WorkMode
    experience_level_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # References ExperienceLevel
    open_positions: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[str] = mapped_column(String(30)) # Draft, Approved, Published, Open, Paused, Filled, Closed
    opening_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    closing_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    application_deadline: Mapped[Date | None] = mapped_column(Date, nullable=True)
    embedding = Column(VectorType(1536), nullable=True) # JD embedding for pgvector matches
    __table_args__ = (UniqueConstraint('organization_id', 'job_code', name='uq_org_job_code'),)

class JobVersion(AuditMixin, Base):
    __tablename__ = "job_versions"
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id"))
    version_number: Mapped[int] = mapped_column(Integer, default=1)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(TEXT)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    changed_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))

class JobSkill(AuditMixin, Base):
    __tablename__ = "job_skills"
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id"))
    skill_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # references Skill
    is_mandatory: Mapped[bool] = mapped_column(default=True)
    proficiency_required: Mapped[str | None] = mapped_column(String(50), nullable=True)

class JobResponsibility(AuditMixin, Base):
    __tablename__ = "job_responsibilities"
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id"))
    responsibility_text: Mapped[str] = mapped_column(TEXT)

class JobQualification(AuditMixin, Base):
    __tablename__ = "job_qualifications"
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id"))
    degree_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # References Degree
    qualification_text: Mapped[str] = mapped_column(String(255))
    is_mandatory: Mapped[bool] = mapped_column(default=True)

class JobBenefit(AuditMixin, Base):
    __tablename__ = "job_benefits"
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id"))
    benefit_text: Mapped[str] = mapped_column(String(255))

class JobLocation(AuditMixin, Base):
    __tablename__ = "job_locations"
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id"))
    location_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # References Location

class JobSalaryRange(AuditMixin, Base):
    __tablename__ = "job_salary_ranges"
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id"), unique=True)
    minimum_salary: Mapped[float] = mapped_column(Float, default=0.0)
    maximum_salary: Mapped[float] = mapped_column(Float, default=0.0)
    currency_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # References Currency

# -------------------------
# Recruitment Ownership
# -------------------------
class JobRecruiter(AuditMixin, Base):
    __tablename__ = "job_recruiters"
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id"))
    recruiter_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # references users
    is_primary: Mapped[bool] = mapped_column(default=True)
    __table_args__ = (UniqueConstraint('job_id', 'recruiter_id', name='uq_job_recruiter'),)

class JobHiringManager(AuditMixin, Base):
    __tablename__ = "job_hiring_managers"
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id"))
    hiring_manager_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # references users
    is_primary: Mapped[bool] = mapped_column(default=True)
    __table_args__ = (UniqueConstraint('job_id', 'hiring_manager_id', name='uq_job_hiring_manager'),)

class RecruiterWorkload(AuditMixin, Base):
    __tablename__ = "recruiter_workloads"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    recruiter_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True)
    active_jobs_count: Mapped[int] = mapped_column(Integer, default=0)
    allocated_capacity: Mapped[int] = mapped_column(Integer, default=10) # limit

# -------------------------
# Approval Workflow
# -------------------------
class RequisitionApproval(AuditMixin, Base):
    __tablename__ = "requisition_approvals"
    hiring_request_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("hiring_requests.id"))
    approver_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # User
    approval_level: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[str] = mapped_column(String(30)) # Pending, Approved, Rejected
    comments: Mapped[str | None] = mapped_column(TEXT, nullable=True)

class ApprovalHistory(AuditMixin, Base):
    __tablename__ = "approval_history"
    hiring_request_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("hiring_requests.id"))
    action_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # User
    action_type: Mapped[str] = mapped_column(String(50)) # Submit, Approve, Reject
    action_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    comments: Mapped[str | None] = mapped_column(TEXT, nullable=True)

# -------------------------
# Job Publishing
# -------------------------
class PublicationChannel(AuditMixin, Base):
    __tablename__ = "publication_channels"
    channel_name: Mapped[str] = mapped_column(String(100), unique=True) # Career Site, LinkedIn, Naukri, Indeed

class JobPublication(AuditMixin, Base):
    __tablename__ = "job_publications"
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id"))
    channel_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("publication_channels.id"))
    external_job_id: Mapped[str | None] = mapped_column(String(100), nullable=True) # Third-party ID
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(30)) # Active, Expired, Removed

class PublicationHistory(AuditMixin, Base):
    __tablename__ = "publication_history"
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id"))
    channel_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("publication_channels.id"))
    action: Mapped[str] = mapped_column(String(50)) # Publish, Unpublish, Expire
    action_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    action_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))

# -------------------------
# Candidate Applications
# -------------------------
class RecruitmentPipeline(AuditMixin, Base):
    __tablename__ = "recruitment_pipelines"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    pipeline_name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

class RecruitmentStage(AuditMixin, Base):
    __tablename__ = "recruitment_stages"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    stage_name: Mapped[str] = mapped_column(String(100)) # Applied, Screening, Technical Interview, HR Interview, Offer, Hired
    sequence_number: Mapped[int] = mapped_column(Integer)

class PipelineStageMapping(AuditMixin, Base):
    __tablename__ = "pipeline_stage_mapping"
    pipeline_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("recruitment_pipelines.id"))
    stage_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("recruitment_stages.id"))
    sequence_number: Mapped[int] = mapped_column(Integer)

class CandidateApplication(AuditMixin, Base):
    __tablename__ = "candidate_applications"
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id"))
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    pipeline_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("recruitment_pipelines.id"), nullable=True)
    current_stage_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("recruitment_stages.id"), nullable=True)
    application_status: Mapped[str] = mapped_column(String(30)) # Applied, Screening, Shortlisted, Interview, Selected, Offer, Hired, Rejected, Withdrawn, Closed
    applied_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    __table_args__ = (UniqueConstraint('candidate_id', 'job_id', name='uq_candidate_job_application'),)

class ApplicationDocument(AuditMixin, Base):
    __tablename__ = "application_documents"
    application_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidate_applications.id"))
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(500))

class ApplicationScreening(AuditMixin, Base):
    __tablename__ = "application_screening"
    application_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidate_applications.id"), unique=True)
    screening_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    screening_status: Mapped[str] = mapped_column(String(50)) # Pass, Fail, Manual Review
    comments: Mapped[str | None] = mapped_column(TEXT, nullable=True)

class ApplicationStageHistory(AuditMixin, Base):
    __tablename__ = "application_stage_history"
    application_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidate_applications.id"))
    from_stage_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("recruitment_stages.id"), nullable=True)
    to_stage_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("recruitment_stages.id"))
    entered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    left_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    changed_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))

class ApplicationNote(AuditMixin, Base):
    __tablename__ = "application_notes"
    application_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidate_applications.id"))
    recruiter_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # User
    note_text: Mapped[str] = mapped_column(TEXT)

class ApplicationTag(AuditMixin, Base):
    __tablename__ = "application_tags"
    application_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidate_applications.id"))
    tag_name: Mapped[str] = mapped_column(String(100))

class StageSla(AuditMixin, Base):
    __tablename__ = "stage_sla"
    pipeline_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("recruitment_pipelines.id"))
    stage_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("recruitment_stages.id"))
    max_days: Mapped[int] = mapped_column(Integer, default=5) # Maximum expected days in stage

# -------------------------
# AI Recruitment
# -------------------------
class AiScreeningResult(AuditMixin, Base):
    __tablename__ = "ai_screening_results"
    application_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidate_applications.id"), unique=True)
    calculated_match_score: Mapped[float] = mapped_column(Float)
    bias_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    screening_summary: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    analyzed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class AiCandidateRanking(AuditMixin, Base):
    __tablename__ = "ai_candidate_rankings"
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id"))
    application_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidate_applications.id"))
    ranking_score: Mapped[float] = mapped_column(Float)
    rank_position: Mapped[int] = mapped_column(Integer)

class AiJobRecommendation(AuditMixin, Base):
    __tablename__ = "ai_job_recommendations"
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # candidate
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id"))
    recommendation_strength: Mapped[float] = mapped_column(Float)
    justification: Mapped[str] = mapped_column(TEXT)

class AiRecruitmentInsight(AuditMixin, Base):
    __tablename__ = "ai_recruitment_insights"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    insight_type: Mapped[str] = mapped_column(String(100)) # e.g. Sourcing bottleneck, High Drop-off
    insight_text: Mapped[str] = mapped_column(TEXT)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

# -------------------------
# Metrics & Audit
# -------------------------
class RecruitmentMetric(AuditMixin, Base):
    __tablename__ = "recruitment_metrics"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    metric_name: Mapped[str] = mapped_column(String(100)) # Time to Hire, Cost per Hire, Recruiter SLA
    metric_value: Mapped[float] = mapped_column(Float)
    calculated_date: Mapped[Date] = mapped_column(Date)

class RecruitmentAuditLog(AuditMixin, Base):
    __tablename__ = "recruitment_audit_logs"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    job_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("jobs.id"), nullable=True)
    application_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("candidate_applications.id"), nullable=True)
    action: Mapped[str] = mapped_column(String(100))
    action_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    action_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    details: Mapped[str | None] = mapped_column(TEXT, nullable=True)

class RecruitmentClosure(AuditMixin, Base):
    __tablename__ = "recruitment_closures"
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id"), unique=True)
    closed_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    closed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    closure_reason: Mapped[str] = mapped_column(String(255)) # Sourced successfully, Budget cut, Cancelled
    total_hires: Mapped[int] = mapped_column(Integer, default=0)
