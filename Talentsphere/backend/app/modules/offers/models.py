from sqlalchemy import Column, String, Integer, ForeignKey, Date, Float, TEXT, Boolean, DateTime, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.models import Base, AuditMixin

# -------------------------
# Offer Management
# -------------------------
class OfferTemplate(AuditMixin, Base):
    __tablename__ = "offer_templates"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    template_name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    job_category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    template_content: Mapped[dict | None] = mapped_column(JSON, nullable=True) # Template structure
    is_default: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)

class Offer(AuditMixin, Base):
    __tablename__ = "offers"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    candidate_application_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # references recruitment.candidate_applications
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # references candidates
    job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # references recruitment.jobs
    offered_designation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # references designations
    hiring_plan_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # references hiring_plans
    offer_template_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("offer_templates.id"), nullable=True)
    issue_date: Mapped[Date] = mapped_column(Date)
    expiry_date: Mapped[Date] = mapped_column(Date)
    start_date: Mapped[Date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(30)) # Draft, Pending Approval, Approved, Generated, Sent, Viewed, Negotiating, Accepted, Rejected, Expired, Withdrawn, Joining Confirmed
    approval_status: Mapped[str] = mapped_column(String(30), default="Pending") # Pending, Approved, Rejected
    rejection_reason: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    internal_notes: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # User who created the offer
    approved_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # User who approved
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    viewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    __table_args__ = (UniqueConstraint('candidate_application_id', name='uq_active_offer_per_app'),)

class OfferVersion(AuditMixin, Base):
    __tablename__ = "offer_versions"
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("offers.id"))
    version_number: Mapped[int] = mapped_column(Integer, default=1)
    compensation_details: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    terms_details: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    change_reason: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    changed_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # User who made the change
    __table_args__ = (UniqueConstraint('offer_id', 'version_number', name='uq_offer_version'),)

class OfferCompensation(AuditMixin, Base):
    __tablename__ = "offer_compensation"
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("offers.id"), unique=True)
    currency_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # references currencies
    base_salary: Mapped[float] = mapped_column(Float, default=0.0)
    variable_compensation: Mapped[float] = mapped_column(Float, default=0.0)
    joining_bonus: Mapped[float] = mapped_column(Float, default=0.0)
    bonus_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    allowances: Mapped[dict | None] = mapped_column(JSON, nullable=True) # {"housing": 5000, "transport": 2000}
    benefits: Mapped[dict | None] = mapped_column(JSON, nullable=True) # {"health_insurance": true, "retirement": true}
    total_compensation: Mapped[float] = mapped_column(Float, default=0.0)
    pay_frequency: Mapped[str] = mapped_column(String(50), default="Monthly") # Monthly, Bi-weekly, Weekly
    salary_band_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("salary_bands.id"), nullable=True)
    within_salary_band: Mapped[bool] = mapped_column(default=True)
    band_violation_reason: Mapped[str | None] = mapped_column(TEXT, nullable=True)

class OfferDocument(AuditMixin, Base):
    __tablename__ = "offer_documents"
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("offers.id"))
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(500))
    file_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    document_type: Mapped[str] = mapped_column(String(50), default="Offer Letter") # Offer Letter, Employment Agreement, NDA
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    storage_path: Mapped[str] = mapped_column(String(500)) # Organized storage path

class OfferAttachment(AuditMixin, Base):
    __tablename__ = "offer_attachments"
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("offers.id"))
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(500))
    file_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    uploaded_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # User who uploaded
    attachment_type: Mapped[str] = mapped_column(String(50)) # Resume, Portfolio, Certificate

# -------------------------
# Offer Terms
# -------------------------
class OfferTerms(AuditMixin, Base):
    __tablename__ = "offer_terms"
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("offers.id"), unique=True)
    employment_type: Mapped[str] = mapped_column(String(50)) # Full-time, Part-time, Contract
    probation_period_months: Mapped[int] = mapped_column(Integer, default=3)
    notice_period_days: Mapped[int] = mapped_column(Integer, default=30)
    work_location: Mapped[str] = mapped_column(String(255))
    work_mode: Mapped[str] = mapped_column(String(50)) # On-site, Remote, Hybrid
    reporting_manager_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    department_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    team_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    additional_terms: Mapped[dict | None] = mapped_column(JSON, nullable=True)

# -------------------------
# Approval Workflow
# -------------------------
class OfferApproval(AuditMixin, Base):
    __tablename__ = "offer_approvals"
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("offers.id"))
    approver_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # User
    approver_role: Mapped[str] = mapped_column(String(100)) # HR Manager, Hiring Manager, Finance
    approval_level: Mapped[int] = mapped_column(Integer, default=1) # Multi-level approval
    status: Mapped[str] = mapped_column(String(30)) # Pending, Approved, Rejected, Skipped
    comments: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    sequence_order: Mapped[int] = mapped_column(Integer, default=0) # Order in approval chain
    __table_args__ = (UniqueConstraint('offer_id', 'approver_id', name='uq_offer_approver'),)

class OfferApprovalHistory(AuditMixin, Base):
    __tablename__ = "offer_approval_history"
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("offers.id"))
    action_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    action_type: Mapped[str] = mapped_column(String(50)) # Submit, Approve, Reject, Cancel
    previous_status: Mapped[str] = mapped_column(String(30))
    new_status: Mapped[str] = mapped_column(String(30))
    comments: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    action_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

# -------------------------
# Negotiation
# -------------------------
class OfferNegotiation(AuditMixin, Base):
    __tablename__ = "offer_negotiations"
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("offers.id"))
    negotiator_type: Mapped[str] = mapped_column(String(50)) # Candidate, Recruiter, Manager
    negotiator_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # User ID if internal
    negotiation_round: Mapped[int] = mapped_column(Integer, default=1)
    requested_base_salary: Mapped[float] = mapped_column(Float, default=0.0)
    requested_total_compensation: Mapped[float] = mapped_column(Float, default=0.0)
    comments: Mapped[str] = mapped_column(TEXT)
    proposed_base_salary: Mapped[float | None] = mapped_column(Float, nullable=True)
    proposed_total_compensation: Mapped[float | None] = mapped_column(Float, nullable=True)
    negotiation_status: Mapped[str] = mapped_column(String(30), default="Pending") # Pending, Accepted, Rejected, Counter-offer
    initiated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    responded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    reason: Mapped[str | None] = mapped_column(TEXT, nullable=True)

class CompensationRevision(AuditMixin, Base):
    __tablename__ = "compensation_revisions"
    negotiation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("offer_negotiations.id"))
    previous_base: Mapped[float] = mapped_column(Float)
    revised_base: Mapped[float] = mapped_column(Float)
    revision_type: Mapped[str] = mapped_column(String(50)) # Increase, Decrease, Same
    approved_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

# -------------------------
# Offer Response
# -------------------------
class OfferAcceptance(AuditMixin, Base):
    __tablename__ = "offer_acceptance"
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("offers.id"), unique=True)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)

class OfferRejection(AuditMixin, Base):
    __tablename__ = "offer_rejections"
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("offers.id"), unique=True)
    rejected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    reason: Mapped[str] = mapped_column(TEXT)

class JoiningConfirmation(AuditMixin, Base):
    __tablename__ = "joining_confirmations"
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("offers.id"), unique=True)
    expected_joining_date: Mapped[Date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(50)) # Confirmed, Delayed, Risk of Ghosting

# -------------------------
# Verification
# -------------------------
class BackgroundVerification(AuditMixin, Base):
    __tablename__ = "background_verifications"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # references candidates
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("offers.id"))
    verification_provider: Mapped[str | None] = mapped_column(String(100), nullable=True) # External provider if used
    status: Mapped[str] = mapped_column(String(30)) # Initiated, InProgress, Completed, Failed, Cancelled
    initiated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    initiated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # User who initiated
    overall_result: Mapped[str | None] = mapped_column(String(30), nullable=True) # Pass, Fail, Pending
    priority: Mapped[str] = mapped_column(String(20), default="Normal") # High, Normal, Low
    case_reference: Mapped[str | None] = mapped_column(String(100), nullable=True) # External reference number

class BackgroundCheckItem(AuditMixin, Base):
    __tablename__ = "background_check_items"
    bg_verification_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("background_verifications.id"))
    item_type: Mapped[str] = mapped_column(String(50)) # Employment, Education, Criminal, Identity, Address, Reference
    item_name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="Pending") # Pending, InProgress, Passed, Failed, Skipped
    provider: Mapped[str | None] = mapped_column(String(100), nullable=True)
    initiated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    result: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    risk_level: Mapped[str | None] = mapped_column(String(20), nullable=True) # High, Medium, Low, None
    documents_required: Mapped[bool] = mapped_column(default=False)
    documents_received: Mapped[bool] = mapped_column(default=False)

class MedicalVerification(AuditMixin, Base):
    __tablename__ = "medical_verifications"
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True)
    status: Mapped[str] = mapped_column(String(30)) # Pending, Passed, Failed

class DocumentVerification(AuditMixin, Base):
    __tablename__ = "document_verifications"
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True)
    status: Mapped[str] = mapped_column(String(30)) # Pending, Passed, Failed

# -------------------------
# Document Collection
# -------------------------
class OnboardingDocument(AuditMixin, Base):
    __tablename__ = "onboarding_documents"
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    document_name: Mapped[str] = mapped_column(String(150))

class OnboardingDocumentSubmission(AuditMixin, Base):
    __tablename__ = "onboarding_document_submissions"
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    onboarding_document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("onboarding_documents.id"))
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(500))

class OnboardingDocumentReview(AuditMixin, Base):
    __tablename__ = "onboarding_document_reviews"
    submission_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("onboarding_document_submissions.id"))
    reviewed_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # User
    status: Mapped[str] = mapped_column(String(30)) # Approved, Rejected

# -------------------------
# Employee Conversion
# -------------------------
class EmployeeConversion(AuditMixin, Base):
    __tablename__ = "employee_conversions"
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True)
    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True) # References users.id (new created employee account)

class EmployeeConversionLog(AuditMixin, Base):
    __tablename__ = "employee_conversion_logs"
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    converted_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # User

# -------------------------
# Onboarding
# -------------------------
class OnboardingPlan(AuditMixin, Base):
    __tablename__ = "onboarding_plans"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    plan_name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    job_category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    department_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    duration_weeks: Mapped[int] = mapped_column(Integer, default=4)
    is_default: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)

class OnboardingTask(AuditMixin, Base):
    __tablename__ = "onboarding_tasks"
    onboarding_plan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("onboarding_plans.id"))
    task_name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    task_type: Mapped[str] = mapped_column(String(50)) # Documentation, Training, Meeting, Equipment, Administrative
    assignee_role: Mapped[str] = mapped_column(String(100)) # HR, IT, Manager, Team Lead
    department_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    priority: Mapped[str] = mapped_column(String(20), default="Normal") # High, Normal, Low
    sequence_order: Mapped[int] = mapped_column(Integer, default=0)
    due_days_after_joining: Mapped[int] = mapped_column(Integer, default=1)
    is_required: Mapped[bool] = mapped_column(default=True)
    dependencies: Mapped[dict | None] = mapped_column(JSON, nullable=True) # Task dependencies

class OnboardingTaskAssignment(AuditMixin, Base):
    __tablename__ = "onboarding_task_assignments"
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # references candidates
    onboarding_task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("onboarding_tasks.id"))
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # User responsible
    due_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="Pending") # Pending, InProgress, Completed, Skipped, Overdue
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    __table_args__ = (UniqueConstraint('candidate_id', 'onboarding_task_id', name='uq_candidate_onboarding_task'),)

class OnboardingChecklist(AuditMixin, Base):
    __tablename__ = "onboarding_checklists"
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # references candidates
    onboarding_plan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("onboarding_plans.id"))
    task_count: Mapped[int] = mapped_column(Integer, default=0)
    completed_count: Mapped[int] = mapped_column(Integer, default=0)
    overall_progress: Mapped[float] = mapped_column(Float, default=0.0) # Percentage
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    estimated_completion: Mapped[Date | None] = mapped_column(Date, nullable=True)
    actual_completion: Mapped[Date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="Not Started") # Not Started, InProgress, Completed, Delayed

class WelcomeKit(AuditMixin, Base):
    __tablename__ = "welcome_kits"
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    kit_type: Mapped[str] = mapped_column(String(100)) # Standard, IT, Executive

class ProbationSetup(AuditMixin, Base):
    __tablename__ = "probation_setups"
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True)
    duration_months: Mapped[int] = mapped_column(Integer, default=3)

class JoiningAudit(AuditMixin, Base):
    __tablename__ = "joining_audits"
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True)
    checks_passed: Mapped[bool] = mapped_column(default=True)

class HiringCompletion(AuditMixin, Base):
    __tablename__ = "hiring_completions"
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class OfferAudit(AuditMixin, Base):
    __tablename__ = "offer_audits"
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("offers.id"))
    details: Mapped[str] = mapped_column(TEXT)
