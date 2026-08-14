from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Date, Float, TEXT, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import UserDefinedType
import uuid
from datetime import datetime
from app.core.models import Base, AuditMixin

# Custom type to support pgvector Vector type without external pgvector library requirement
class VectorType(UserDefinedType):
    def __init__(self, dim=1536):
        self.dim = dim
        
    def get_col_spec(self, **kw):
        return f"VECTOR({self.dim})"

# -------------------------
# Candidate Core
# -------------------------
class Candidate(AuditMixin, Base):
    __tablename__ = "candidates"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)

class CandidateProfile(AuditMixin, Base):
    __tablename__ = "candidate_profiles"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"), unique=True)
    gender: Mapped[str | None] = mapped_column(String(20), nullable=True)
    date_of_birth: Mapped[Date | None] = mapped_column(Date, nullable=True)
    marital_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    nationality: Mapped[str | None] = mapped_column(String(100), nullable=True)
    profile_photo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    summary: Mapped[str | None] = mapped_column(TEXT, nullable=True)

class CandidateAddress(AuditMixin, Base):
    __tablename__ = "candidate_addresses"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    address_type: Mapped[str] = mapped_column(String(30)) # Permanent, Current
    address_line_1: Mapped[str] = mapped_column(String(255))
    address_line_2: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # References City
    state_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # References State
    country_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # References Country
    postal_code: Mapped[str | None] = mapped_column(String(30), nullable=True)

class CandidatePreference(AuditMixin, Base):
    __tablename__ = "candidate_preferences"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"), unique=True)
    notice_period_days: Mapped[int] = mapped_column(Integer, default=0)
    preferred_locations: Mapped[str | None] = mapped_column(TEXT, nullable=True) # comma separated
    work_mode_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # References WorkMode
    employment_type_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # References EmploymentType
    is_open_to_relocate: Mapped[bool] = mapped_column(default=False)

class CandidateEmergencyContact(AuditMixin, Base):
    __tablename__ = "candidate_emergency_contacts"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    contact_name: Mapped[str] = mapped_column(String(150))
    relationship: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(30))
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)

# -------------------------
# Resume Management
# -------------------------
class CandidateResume(AuditMixin, Base):
    __tablename__ = "candidate_resumes"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(500))
    file_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_primary: Mapped[bool] = mapped_column(default=True)

class ResumeVersion(AuditMixin, Base):
    __tablename__ = "resume_versions"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    resume_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidate_resumes.id"))
    version_number: Mapped[int] = mapped_column(Integer, default=1)
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(500))

class ResumeParsingHistory(AuditMixin, Base):
    __tablename__ = "resume_parsing_history"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    resume_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidate_resumes.id"))
    parsed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    parser_status: Mapped[str] = mapped_column(String(30)) # Success, Failed
    parsed_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error_message: Mapped[str | None] = mapped_column(TEXT, nullable=True)

# -------------------------
# Professional Information
# -------------------------
class CandidateEducation(AuditMixin, Base):
    __tablename__ = "candidate_education"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    degree_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # References Degree
    degree_name: Mapped[str] = mapped_column(String(150))
    field_of_study: Mapped[str | None] = mapped_column(String(150), nullable=True)
    university_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # References University
    university_name: Mapped[str] = mapped_column(String(255))
    start_year: Mapped[int] = mapped_column(Integer)
    end_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    grade: Mapped[str | None] = mapped_column(String(30), nullable=True) # GPA or Percentage
    is_completed: Mapped[bool] = mapped_column(default=True)

class CandidateExperience(AuditMixin, Base):
    __tablename__ = "candidate_experience"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    company_name: Mapped[str] = mapped_column(String(255))
    designation_name: Mapped[str] = mapped_column(String(150))
    start_date: Mapped[Date] = mapped_column(Date)
    end_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    is_current: Mapped[bool] = mapped_column(default=False)
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    location: Mapped[str | None] = mapped_column(String(150), nullable=True)

class CandidateProject(AuditMixin, Base):
    __tablename__ = "candidate_projects"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    project_name: Mapped[str] = mapped_column(String(255))
    role_in_project: Mapped[str | None] = mapped_column(String(150), nullable=True)
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    project_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    start_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[Date | None] = mapped_column(Date, nullable=True)

class CandidateSkill(AuditMixin, Base):
    __tablename__ = "candidate_skills"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    skill_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("skills.id"))
    proficiency_level: Mapped[str | None] = mapped_column(String(50), nullable=True) # Beginner, Intermediate, Expert

class CandidateLanguage(AuditMixin, Base):
    __tablename__ = "candidate_languages"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    language_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # References Language
    language_name: Mapped[str] = mapped_column(String(100))
    proficiency: Mapped[str | None] = mapped_column(String(50), nullable=True) # Read, Write, Speak

class CandidateCertification(AuditMixin, Base):
    __tablename__ = "candidate_certifications"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    certification_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # References Certification
    certification_name: Mapped[str] = mapped_column(String(255))
    issuing_organization: Mapped[str] = mapped_column(String(255))
    issue_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    expiry_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    credential_id: Mapped[str | None] = mapped_column(String(100), nullable=True)

class CandidateAchievement(AuditMixin, Base):
    __tablename__ = "candidate_achievements"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    issued_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    issued_date: Mapped[Date | None] = mapped_column(Date, nullable=True)

class CandidatePublication(AuditMixin, Base):
    __tablename__ = "candidate_publications"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    title: Mapped[str] = mapped_column(String(255))
    publisher: Mapped[str | None] = mapped_column(String(255), nullable=True)
    publication_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    publication_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)

class CandidatePatent(AuditMixin, Base):
    __tablename__ = "candidate_patents"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    title: Mapped[str] = mapped_column(String(255))
    patent_number: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(50)) # Approved, Pending
    filed_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    issued_date: Mapped[Date | None] = mapped_column(Date, nullable=True)

# -------------------------
# Portfolio & References
# -------------------------
class CandidatePortfolio(AuditMixin, Base):
    __tablename__ = "candidate_portfolios"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    portfolio_name: Mapped[str] = mapped_column(String(150))
    portfolio_url: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)

class CandidateSocialProfile(AuditMixin, Base):
    __tablename__ = "candidate_social_profiles"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    social_platform: Mapped[str] = mapped_column(String(50)) # LinkedIn, GitHub, Behance
    profile_url: Mapped[str] = mapped_column(String(255))
    __table_args__ = (UniqueConstraint('candidate_id', 'social_platform', name='uq_candidate_social'),)

class CandidateReference(AuditMixin, Base):
    __tablename__ = "candidate_references"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    ref_name: Mapped[str] = mapped_column(String(150))
    relationship: Mapped[str] = mapped_column(String(100)) # e.g. Manager, Peer
    company: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)

# -------------------------
# Documents
# -------------------------
class CandidateDocumentType(AuditMixin, Base):
    __tablename__ = "candidate_document_types"
    type_name: Mapped[str] = mapped_column(String(100), unique=True) # Passport, Aadhaar, PAN, PaySlip

class CandidateDocument(AuditMixin, Base):
    __tablename__ = "candidate_documents"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    document_type_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidate_document_types.id"))
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(500))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

# -------------------------
# Recruitment Support
# -------------------------
class CandidateNote(AuditMixin, Base):
    __tablename__ = "candidate_notes"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    recruiter_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # References User
    note_content: Mapped[str] = mapped_column(TEXT)

class CandidateTag(AuditMixin, Base):
    __tablename__ = "candidate_tags"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    tag_name: Mapped[str] = mapped_column(String(100))

class CandidateTimeline(AuditMixin, Base):
    __tablename__ = "candidate_timeline"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    event_name: Mapped[str] = mapped_column(String(150)) # Resume Uploaded, Applied to Job, Scheduled Interview
    event_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    details: Mapped[str | None] = mapped_column(TEXT, nullable=True)

class CandidateActivity(AuditMixin, Base):
    __tablename__ = "candidate_activities"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    action_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # User ID
    action_type: Mapped[str] = mapped_column(String(100))
    action_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class CandidateOwnership(AuditMixin, Base):
    __tablename__ = "candidate_ownership"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    recruiter_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # References User
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

# -------------------------
# Privacy & Compliance
# -------------------------
class CandidateConsent(AuditMixin, Base):
    __tablename__ = "candidate_consents"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    consent_given: Mapped[bool] = mapped_column(default=True)
    consent_purpose: Mapped[str] = mapped_column(String(255)) # e.g. GDPR, Background Verification
    given_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class CandidateBlacklist(AuditMixin, Base):
    __tablename__ = "candidate_blacklist"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    reason: Mapped[str] = mapped_column(TEXT)
    blacklisted_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # References User
    blacklisted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class DuplicateCandidate(AuditMixin, Base):
    __tablename__ = "duplicate_candidates"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    primary_candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    duplicate_candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    match_score: Mapped[float] = mapped_column(Float) # Percentage matching
    detection_reason: Mapped[str | None] = mapped_column(String(255), nullable=True) # e.g. Same email, same phone

class CandidateMergeHistory(AuditMixin, Base):
    __tablename__ = "candidate_merge_history"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    master_candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    merged_candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    merged_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # References User
    merged_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

# -------------------------
# Availability
# -------------------------
class CandidateAvailability(AuditMixin, Base):
    __tablename__ = "candidate_availability"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"), unique=True)
    availability_status: Mapped[str] = mapped_column(String(50)) # Immediate, 1 Month, 3 Months
    last_checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class CandidateSalaryExpectation(AuditMixin, Base):
    __tablename__ = "candidate_salary_expectations"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"), unique=True)
    expected_salary: Mapped[float] = mapped_column(Float, default=0.0)
    currency_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # References Currency

# -------------------------
# Candidate Source
# -------------------------
class CandidateSource(AuditMixin, Base):
    __tablename__ = "candidate_sources"
    source_name: Mapped[str] = mapped_column(String(100), unique=True) # Referral, LinkedIn, Naukri, Indeed, Career Portal

class CandidateSourceHistory(AuditMixin, Base):
    __tablename__ = "candidate_source_history"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidate_sources.id"))
    referrer_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True) # If referral
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

# -------------------------
# AI
# -------------------------
class CandidateAiProfile(AuditMixin, Base):
    __tablename__ = "candidate_ai_profiles"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"), unique=True)
    ai_calculated_experience_years: Mapped[float | None] = mapped_column(Float, nullable=True)
    ai_top_skills: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    ai_profile_completeness: Mapped[float | None] = mapped_column(Float, nullable=True) # 0 to 100

class CandidateEmbedding(AuditMixin, Base):
    __tablename__ = "candidate_embeddings"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"), unique=True)
    resume_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("candidate_resumes.id"), nullable=True)
    embedding = Column(VectorType(1536), nullable=False) # OpenAI 1536-dim embedding

class CandidateAiSummary(AuditMixin, Base):
    __tablename__ = "candidate_ai_summaries"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"), unique=True)
    summary_text: Mapped[str] = mapped_column(TEXT)
    key_highlights: Mapped[str | None] = mapped_column(TEXT, nullable=True) # Bulleted key achievements
    potential_risks: Mapped[str | None] = mapped_column(TEXT, nullable=True) # Gap in employment, short stints

class CandidateAiRecommendation(AuditMixin, Base):
    __tablename__ = "candidate_ai_recommendations"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    recommended_job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # Job ID
    match_score: Mapped[float] = mapped_column(Float) # Matching percentage
    explanation: Mapped[str] = mapped_column(TEXT)

class CandidateAuditLog(AuditMixin, Base):
    __tablename__ = "candidate_audit_logs"
    candidate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidates.id"))
    changed_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    field_name: Mapped[str] = mapped_column(String(100))
    old_value: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    new_value: Mapped[str | None] = mapped_column(TEXT, nullable=True)
