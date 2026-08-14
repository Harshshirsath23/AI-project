from sqlalchemy import Column, String, Integer, ForeignKey, Date, Float, TEXT, Boolean, DateTime, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.models import Base, AuditMixin

# -------------------------
# Interview Configuration
# -------------------------
class InterviewTemplate(AuditMixin, Base):
    __tablename__ = "interview_templates"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    template_name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    job_category: Mapped[str | None] = mapped_column(String(100), nullable=True) # e.g. Engineering, Sales, Design
    is_active: Mapped[bool] = mapped_column(default=True)
    is_default: Mapped[bool] = mapped_column(default=False)

class InterviewTemplateRound(AuditMixin, Base):
    __tablename__ = "interview_template_rounds"
    template_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interview_templates.id"))
    round_name: Mapped[str] = mapped_column(String(100)) # e.g. Screening, Technical, HR, Manager
    sequence_number: Mapped[int] = mapped_column(Integer)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=30)
    interview_mode: Mapped[str] = mapped_column(String(50)) # Online, In-person, Phone, Video
    required_interviewers: Mapped[int] = mapped_column(Integer, default=1)
    panel_required: Mapped[bool] = mapped_column(default=False)
    interviewer_role_requirements: Mapped[dict | None] = mapped_column(JSON, nullable=True) # e.g. {"roles": ["Tech Lead", "Senior Engineer"]}
    rescheduling_allowed: Mapped[bool] = mapped_column(default=True)
    min_rescheduling_hours: Mapped[int] = mapped_column(Integer, default=24)
    passing_threshold: Mapped[float] = mapped_column(Float, default=70.0) # Minimum score to pass
    feedback_required: Mapped[bool] = mapped_column(default=True)
    __table_args__ = (UniqueConstraint('template_id', 'sequence_number', name='uq_template_round_sequence'),)

class InterviewTemplateCriterion(AuditMixin, Base):
    __tablename__ = "interview_template_criteria"
    round_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interview_template_rounds.id"))
    criterion_name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    weight: Mapped[float] = mapped_column(Float, default=1.0) # Weight for overall score calculation
    max_score: Mapped[float] = mapped_column(Float, default=10.0)
    is_required: Mapped[bool] = mapped_column(default=True)
    evaluation_type: Mapped[str] = mapped_column(String(50)) # Rating, Score, PassFail, Text

class InterviewType(AuditMixin, Base):
    __tablename__ = "interview_types"
    type_name: Mapped[str] = mapped_column(String(50), unique=True) # e.g. Virtual, Onsite, Phone
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)

class InterviewMode(AuditMixin, Base):
    __tablename__ = "interview_modes"
    mode_name: Mapped[str] = mapped_column(String(50), unique=True) # Online, In-person, Phone, Video
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)

# -------------------------
# Interview Scheduling
# -------------------------
class Interview(AuditMixin, Base):
    __tablename__ = "interviews"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    candidate_application_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # References recruitment.candidate_applications
    template_round_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interview_template_rounds.id"))
    interview_type_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interview_types.id"))
    interview_mode_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interview_modes.id"))
    job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # References recruitment.jobs
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # References candidates
    scheduled_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    scheduled_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    actual_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    actual_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    timezone: Mapped[str] = mapped_column(String(50), default="UTC")
    location: Mapped[str | None] = mapped_column(String(255), nullable=True) # Physical address or meeting link
    meeting_url: Mapped[str | None] = mapped_column(String(500), nullable=True) # Video conferencing link
    meeting_password: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(30)) # Planned, Scheduled, Invitation Sent, Confirmed, Started, Completed, Feedback Submitted, Evaluation Completed, Decision Published, Cancelled, Rescheduled, No Show, Expired
    notes: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    internal_notes: Mapped[str | None] = mapped_column(TEXT, nullable=True) # Private notes for interviewers

class InterviewSchedule(AuditMixin, Base):
    __tablename__ = "interview_schedules"
    interview_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interviews.id"))
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    timezone: Mapped[str] = mapped_column(String(50), default="UTC")

class InterviewReschedule(AuditMixin, Base):
    __tablename__ = "interview_reschedules"
    interview_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interviews.id"))
    rescheduled_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # User
    rescheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    previous_start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    new_start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    reason: Mapped[str] = mapped_column(TEXT)

class InterviewCancellation(AuditMixin, Base):
    __tablename__ = "interview_cancellations"
    interview_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interviews.id"))
    cancelled_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # User
    cancelled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    reason: Mapped[str] = mapped_column(TEXT)

class InterviewCalendarEvent(AuditMixin, Base):
    __tablename__ = "interview_calendar_events"
    interview_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interviews.id"))
    calendar_provider: Mapped[str] = mapped_column(String(50)) # Google, Outlook
    event_id: Mapped[str] = mapped_column(String(255))
    meeting_link: Mapped[str | None] = mapped_column(String(500), nullable=True)

# -------------------------
# Interview Participants
# -------------------------
class InterviewPanel(AuditMixin, Base):
    __tablename__ = "interview_panels"
    interview_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interviews.id"))
    panel_name: Mapped[str] = mapped_column(String(150))
    is_active: Mapped[bool] = mapped_column(default=True)

class InterviewPanelMember(AuditMixin, Base):
    __tablename__ = "interview_panel_members"
    panel_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interview_panels.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # references users.id
    role: Mapped[str] = mapped_column(String(100)) # Primary Interviewer, Technical Expert, Hiring Manager, Observer
    is_primary: Mapped[bool] = mapped_column(default=False)
    feedback_status: Mapped[str] = mapped_column(String(30), default="Pending") # Pending, Submitted, Skipped
    feedback_submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    __table_args__ = (UniqueConstraint('panel_id', 'user_id', name='uq_interview_panel_member'),)

class InterviewerAssignment(AuditMixin, Base):
    __tablename__ = "interviewer_assignments"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # Job
    interviewer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # User
    role: Mapped[str] = mapped_column(String(100)) # Technical Interviewer, HR Interviewer, Hiring Manager
    is_active: Mapped[bool] = mapped_column(default=True)
    workload_capacity: Mapped[int] = mapped_column(Integer, default=10) # Max concurrent interviews
    current_workload: Mapped[int] = mapped_column(Integer, default=0)
    __table_args__ = (UniqueConstraint('job_id', 'interviewer_id', name='uq_job_interviewer'),)

# -------------------------
# Interview Evaluation
# -------------------------
class EvaluationCriterion(AuditMixin, Base):
    __tablename__ = "evaluation_criteria"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    criterion_name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True) # Technical, Behavioral, Cultural Fit
    evaluation_type: Mapped[str] = mapped_column(String(50)) # Rating, Score, PassFail, Text
    default_weight: Mapped[float] = mapped_column(Float, default=1.0)
    default_max_score: Mapped[float] = mapped_column(Float, default=10.0)
    is_active: Mapped[bool] = mapped_column(default=True)

class InterviewFeedback(AuditMixin, Base):
    __tablename__ = "interview_feedback"
    interview_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interviews.id"))
    interviewer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # user
    panel_member_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("interview_panel_members.id"), nullable=True)
    overall_rating: Mapped[int | None] = mapped_column(Integer, nullable=True) # 1 to 5
    overall_score: Mapped[float | None] = mapped_column(Float, nullable=True) # Calculated weighted score
    recommendation: Mapped[str | None] = mapped_column(String(50), nullable=True) # Strong Hire, Hire, No Hire, Strong No Hire
    strengths: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    weaknesses: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    detailed_comments: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="Pending") # Pending, Submitted, Locked
    is_complete: Mapped[bool] = mapped_column(default=False)
    __table_args__ = (UniqueConstraint('interview_id', 'interviewer_id', name='uq_interview_feedback'),)

class FeedbackCriterionScore(AuditMixin, Base):
    __tablename__ = "feedback_criterion_scores"
    feedback_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interview_feedback.id"))
    criterion_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("evaluation_criteria.id"))
    score: Mapped[float] = mapped_column(Float)
    max_score: Mapped[float] = mapped_column(Float)
    weight: Mapped[float] = mapped_column(Float, default=1.0)
    comments: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    evidence: Mapped[str | None] = mapped_column(TEXT, nullable=True) # Specific examples/evidence
    is_required: Mapped[bool] = mapped_column(default=True)
    passes_threshold: Mapped[bool] = mapped_column(default=True)

class InterviewScorecard(AuditMixin, Base):
    __tablename__ = "interview_scorecards"
    interview_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interviews.id"), unique=True)
    template_round_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interview_template_rounds.id"))
    overall_score: Mapped[float] = mapped_column(Float, default=0.0)
    max_possible_score: Mapped[float] = mapped_column(Float, default=100.0)
    percentage_score: Mapped[float] = mapped_column(Float, default=0.0)
    recommendation: Mapped[str] = mapped_column(String(50)) # Pass, Hold, Reject
    recommendation_confidence: Mapped[float] = mapped_column(Float, default=0.0) # 0.0 to 1.0
    summary: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    is_final: Mapped[bool] = mapped_column(default=False)
    required_feedback_count: Mapped[int] = mapped_column(Integer, default=1)
    received_feedback_count: Mapped[int] = mapped_column(Integer, default=0)

class InterviewDecision(AuditMixin, Base):
    __tablename__ = "interview_decisions"
    interview_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interviews.id"), unique=True)
    decision: Mapped[str] = mapped_column(String(50)) # PASS, FAIL, HOLD, REVIEW_REQUIRED
    decision_maker_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # User who made the decision
    decision_maker_role: Mapped[str] = mapped_column(String(100)) # Recruiter, Hiring Manager, HR
    decision_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    justification: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    ai_recommendation: Mapped[str | None] = mapped_column(String(50), nullable=True) # AI recommendation for reference
    ai_confidence: Mapped[float | None] = mapped_column(Float, nullable=True) # AI confidence score
    ai_evidence: Mapped[dict | None] = mapped_column(JSON, nullable=True) # AI supporting evidence
    overrides_ai: Mapped[bool] = mapped_column(default=False) # Human overrode AI recommendation
    next_step: Mapped[str | None] = mapped_column(String(100), nullable=True) # Next action in recruitment workflow

# -------------------------
# Assessments
# -------------------------
class AssessmentType(AuditMixin, Base):
    __tablename__ = "assessment_types"
    type_name: Mapped[str] = mapped_column(String(50), unique=True) # Interview, Coding, Written, Custom
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)

class AssessmentTemplate(AuditMixin, Base):
    __tablename__ = "assessment_templates"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    assessment_type_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assessment_types.id"))
    template_name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60)
    passing_score: Mapped[float] = mapped_column(Float, default=70.0)
    max_attempts: Mapped[int] = mapped_column(Integer, default=3)
    instructions: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    configuration: Mapped[dict | None] = mapped_column(JSON, nullable=True) # Type-specific configuration

class Assessment(AuditMixin, Base):
    __tablename__ = "assessments"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    assessment_template_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assessment_templates.id"))
    assessment_name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    interview_round_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("interview_template_rounds.id"), nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60)
    status: Mapped[str] = mapped_column(String(30), default="Active") # Active, Archived
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class AssessmentQuestion(AuditMixin, Base):
    __tablename__ = "assessment_questions"
    template_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assessment_templates.id"))
    question_text: Mapped[str] = mapped_column(TEXT)
    question_type: Mapped[str] = mapped_column(String(50)) # MultipleChoice, Coding, FreeText, TrueFalse
    options: Mapped[dict | None] = mapped_column(JSON, nullable=True) # For multiple choice
    correct_answer: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    points: Mapped[float] = mapped_column(Float, default=1.0)
    sequence_order: Mapped[int] = mapped_column(Integer, default=0)
    explanation: Mapped[str | None] = mapped_column(TEXT, nullable=True) # Explanation for correct answer
    is_required: Mapped[bool] = mapped_column(default=True)

class AssessmentAttempt(AuditMixin, Base):
    __tablename__ = "assessment_attempts"
    assessment_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assessments.id"))
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    attempt_number: Mapped[int] = mapped_column(Integer, default=1)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    time_spent_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    percentage_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="InProgress") # InProgress, Submitted, Evaluated, Passed, Failed
    ip_address: Mapped[str | None] = mapped_column(String(50), nullable=True)
    browser_info: Mapped[str | None] = mapped_column(String(255), nullable=True)
    __table_args__ = (UniqueConstraint('assessment_id', 'candidate_id', 'attempt_number', name='uq_assessment_attempt'),)

class AssessmentAnswer(AuditMixin, Base):
    __tablename__ = "assessment_answers"
    attempt_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assessment_attempts.id"))
    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assessment_questions.id"))
    answer_text: Mapped[str] = mapped_column(TEXT)
    is_correct: Mapped[bool] = mapped_column(default=False)
    score: Mapped[float] = mapped_column(Float, default=0.0)
    time_spent_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    answered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class CodingTest(AuditMixin, Base):
    __tablename__ = "coding_tests"
    assessment_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assessments.id"))
    language: Mapped[str] = mapped_column(String(50)) # Python, JavaScript, Java, C++
    problem_statement: Mapped[str] = mapped_column(TEXT)
    input_format: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    output_format: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    constraints: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    test_cases: Mapped[dict | None] = mapped_column(JSON, nullable=True) # Array of test cases
    starter_code: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    time_limit_seconds: Mapped[int] = mapped_column(Integer, default=300)
    memory_limit_mb: Mapped[int] = mapped_column(Integer, default=256)

class CodingSubmission(AuditMixin, Base):
    __tablename__ = "coding_submissions"
    attempt_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assessment_attempts.id"))
    coding_test_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("coding_tests.id"))
    code: Mapped[str] = mapped_column(TEXT)
    language: Mapped[str] = mapped_column(String(50))
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    execution_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    memory_used_mb: Mapped[int | None] = mapped_column(Integer, nullable=True)
    test_cases_passed: Mapped[int] = mapped_column(Integer, default=0)
    total_test_cases: Mapped[int] = mapped_column(Integer, default=0)
    compilation_status: Mapped[str] = mapped_column(String(30)) # Success, Error, Timeout
    compilation_error: Mapped[str | None] = mapped_column(TEXT, nullable=True)

class AssignmentSubmission(AuditMixin, Base):
    __tablename__ = "assignment_submissions"
    attempt_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assessment_attempts.id"))
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(500))
    file_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    plagiarism_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    evaluation_comments: Mapped[str | None] = mapped_column(TEXT, nullable=True)

# -------------------------
# AI Evaluation Hooks (for future LangGraph integration)
# -------------------------
class AiInterviewAnalysis(AuditMixin, Base):
    __tablename__ = "ai_interview_analysis"
    interview_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interviews.id"), unique=True)
    analysis_type: Mapped[str] = mapped_column(String(50)) # Transcript, Sentiment, Behavior, Recommendation
    analysis_text: Mapped[str] = mapped_column(TEXT)
    confidence_score: Mapped[float] = mapped_column(Float)
    model_version: Mapped[str | None] = mapped_column(String(100), nullable=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    is_used: Mapped[bool] = mapped_column(default=False) # Whether human used this analysis

class AiCandidateFeedback(AuditMixin, Base):
    __tablename__ = "ai_candidate_feedback"
    interview_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interviews.id"))
    feedback_type: Mapped[str] = mapped_column(String(50)) # Strengths, Weaknesses, Overall, Recommendation
    feedback_text: Mapped[str] = mapped_column(TEXT)
    confidence_score: Mapped[float] = mapped_column(Float)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class AiInterviewSummary(AuditMixin, Base):
    __tablename__ = "ai_interview_summary"
    interview_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interviews.id"), unique=True)
    summary_text: Mapped[str] = mapped_column(TEXT)
    key_points: Mapped[dict | None] = mapped_column(JSON, nullable=True) # Key insights extracted
    sentiment_analysis: Mapped[dict | None] = mapped_column(JSON, nullable=True) # Sentiment breakdown
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class AiInterviewScore(AuditMixin, Base):
    __tablename__ = "ai_interview_scores"
    interview_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interviews.id"), unique=True)
    overall_score: Mapped[float] = mapped_column(Float)
    component_scores: Mapped[dict | None] = mapped_column(JSON, nullable=True) # Breakdown by category
    recommendation: Mapped[str] = mapped_column(String(50)) # Strong Hire, Hire, No Hire, Strong No Hire
    confidence: Mapped[float] = mapped_column(Float)
    evidence: Mapped[dict | None] = mapped_column(JSON, nullable=True) # Supporting evidence
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class AiBehaviorAnalysis(AuditMixin, Base):
    __tablename__ = "ai_behavior_analysis"
    interview_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interviews.id"), unique=True)
    trait_scores: Mapped[dict | None] = mapped_column(JSON, nullable=True) # JSON trait scoring
    communication_style: Mapped[str | None] = mapped_column(String(100), nullable=True)
    confidence_level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    problem_solving_approach: Mapped[str | None] = mapped_column(String(100), nullable=True)
    cultural_fit_indicators: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

# -------------------------
# Support
# -------------------------
class InterviewAttachment(AuditMixin, Base):
    __tablename__ = "interview_attachments"
    interview_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interviews.id"))
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(500))

class InterviewRecording(AuditMixin, Base):
    __tablename__ = "interview_recordings"
    interview_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interviews.id"), unique=True)
    recording_url: Mapped[str] = mapped_column(String(500))
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)

class InterviewNotification(AuditMixin, Base):
    __tablename__ = "interview_notifications"
    interview_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interviews.id"))
    notification_type: Mapped[str] = mapped_column(String(50)) # Schedule, Reschedule, Cancellation, Reminder
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class InterviewTimeline(AuditMixin, Base):
    __tablename__ = "interview_timelines"
    interview_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interviews.id"))
    event_name: Mapped[str] = mapped_column(String(150))
    event_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class InterviewAuditLog(AuditMixin, Base):
    __tablename__ = "interview_audit_logs"
    interview_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("interviews.id"))
    action: Mapped[str] = mapped_column(String(100))
    action_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    action_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

class InterviewAnalytics(AuditMixin, Base):
    __tablename__ = "interview_analytics"
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    metric_name: Mapped[str] = mapped_column(String(100)) # e.g. Feedback Latency, Score Distribution
    metric_value: Mapped[float] = mapped_column(Float)
