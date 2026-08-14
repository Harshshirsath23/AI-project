from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

from app.modules.interviews.enums import (
    InterviewStatus, InterviewMode, InterviewType, FeedbackStatus,
    EvaluationType, DecisionType, RecommendationType,
    AssessmentStatus, AssessmentAttemptStatus, QuestionType,
    AssessmentType, CompilationStatus, InterviewerRole,
    DecisionMakerRole, TimelineEventType, NotificationType,
    CriterionCategory, AIAnalysisType, AIFeedbackType
)


# ==================== Template Schemas ====================

class InterviewTemplateRoundCreate(BaseModel):
    round_name: str = Field(..., description="Name of the interview round")
    sequence_number: int = Field(..., ge=1, description="Order of this round in the sequence")
    duration_minutes: int = Field(default=30, ge=15, le=480, description="Duration in minutes")
    interview_mode: str = Field(default="Online", description="Mode of interview")
    required_interviewers: int = Field(default=1, ge=1, description="Number of interviewers required")
    panel_required: bool = Field(default=False, description="Whether panel interview is required")
    interviewer_role_requirements: Optional[Dict[str, Any]] = Field(None, description="Required interviewer roles")
    rescheduling_allowed: bool = Field(default=True, description="Whether rescheduling is allowed")
    min_rescheduling_hours: int = Field(default=24, ge=0, description="Minimum hours for rescheduling notice")
    passing_threshold: float = Field(default=70.0, ge=0, le=100, description="Passing score threshold")
    feedback_required: bool = Field(default=True, description="Whether feedback is required")

class InterviewTemplateCriterionCreate(BaseModel):
    criterion_name: str = Field(..., description="Name of the evaluation criterion")
    description: Optional[str] = Field(None, description="Description of the criterion")
    weight: float = Field(default=1.0, ge=0, le=1, description="Weight for overall score calculation")
    max_score: float = Field(default=10.0, gt=0, description="Maximum score for this criterion")
    is_required: bool = Field(default=True, description="Whether this criterion is required")
    evaluation_type: str = Field(default="Score", description="Type of evaluation")

class InterviewTemplateCreate(BaseModel):
    template_name: str = Field(..., description="Name of the interview template")
    description: Optional[str] = Field(None, description="Description of the template")
    job_category: Optional[str] = Field(None, description="Job category for this template")
    is_default: bool = Field(default=False, description="Whether this is the default template")
    rounds: List[InterviewTemplateRoundCreate] = Field(..., description="Interview rounds in this template")

class InterviewTemplateRoundResponse(BaseModel):
    id: uuid.UUID
    round_name: str
    sequence_number: int
    duration_minutes: int
    interview_mode: str
    required_interviewers: int
    panel_required: bool
    interviewer_role_requirements: Optional[Dict[str, Any]]
    rescheduling_allowed: bool
    min_rescheduling_hours: int
    passing_threshold: float
    feedback_required: bool
    
    class Config:
        from_attributes = True

class InterviewTemplateCriterionResponse(BaseModel):
    id: uuid.UUID
    criterion_name: str
    description: Optional[str]
    weight: float
    max_score: float
    is_required: bool
    evaluation_type: str
    
    class Config:
        from_attributes = True

class InterviewTemplateResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    template_name: str
    description: Optional[str]
    job_category: Optional[str]
    is_active: bool
    is_default: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Interview Schemas ====================

class InterviewSchedule(BaseModel):
    scheduled_start: datetime = Field(..., description="Start time of the interview")
    scheduled_end: datetime = Field(..., description="End time of the interview")
    timezone: str = Field(default="UTC", description="Timezone for the interview")
    location: Optional[str] = Field(None, description="Physical location or meeting details")
    meeting_url: Optional[str] = Field(None, description="Video conferencing link")
    meeting_password: Optional[str] = Field(None, description="Meeting password if applicable")

class InterviewCreate(BaseModel):
    candidate_application_id: uuid.UUID = Field(..., description="Candidate application ID")
    template_round_id: uuid.UUID = Field(..., description="Template round ID")
    interview_type_id: uuid.UUID = Field(..., description="Interview type ID")
    interview_mode_id: uuid.UUID = Field(..., description="Interview mode ID")
    job_id: uuid.UUID = Field(..., description="Job ID")
    candidate_id: uuid.UUID = Field(..., description="Candidate ID")
    schedule: InterviewSchedule = Field(..., description="Interview schedule details")
    notes: Optional[str] = Field(None, description="Interview notes")
    internal_notes: Optional[str] = Field(None, description="Internal notes for interviewers")

class InterviewUpdate(BaseModel):
    scheduled_start: Optional[datetime] = Field(None, description="Updated start time")
    scheduled_end: Optional[datetime] = Field(None, description="Updated end time")
    location: Optional[str] = Field(None, description="Updated location")
    meeting_url: Optional[str] = Field(None, description="Updated meeting URL")
    notes: Optional[str] = Field(None, description="Updated notes")
    internal_notes: Optional[str] = Field(None, description="Updated internal notes")

class InterviewRescheduleRequest(BaseModel):
    new_start_time: datetime = Field(..., description="New start time")
    new_end_time: datetime = Field(..., description="New end time")
    reason: str = Field(..., description="Reason for rescheduling")

class InterviewCancelRequest(BaseModel):
    reason: str = Field(..., description="Reason for cancellation")

class InterviewResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    candidate_application_id: uuid.UUID
    template_round_id: uuid.UUID
    interview_type_id: uuid.UUID
    interview_mode_id: uuid.UUID
    job_id: uuid.UUID
    candidate_id: uuid.UUID
    scheduled_start: datetime
    scheduled_end: datetime
    actual_start: Optional[datetime]
    actual_end: Optional[datetime]
    timezone: str
    location: Optional[str]
    meeting_url: Optional[str]
    meeting_password: Optional[str]
    status: str
    notes: Optional[str]
    internal_notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Panel Schemas ====================

class PanelMemberCreate(BaseModel):
    user_id: uuid.UUID = Field(..., description="User ID of the panel member")
    role: str = Field(default="Interviewer", description="Role in the panel")
    is_primary: bool = Field(default=False, description="Whether this is the primary interviewer")

class PanelMemberResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    role: str
    is_primary: bool
    feedback_status: str
    feedback_submitted_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class InterviewPanelCreate(BaseModel):
    panel_name: str = Field(..., description="Name of the interview panel")
    members: List[PanelMemberCreate] = Field(..., description="Panel members")

class InterviewPanelResponse(BaseModel):
    id: uuid.UUID
    interview_id: uuid.UUID
    panel_name: str
    is_active: bool
    members: List[PanelMemberResponse]
    
    class Config:
        from_attributes = True


# ==================== Feedback Schemas ====================

class CriterionScoreCreate(BaseModel):
    criterion_id: uuid.UUID = Field(..., description="Evaluation criterion ID")
    score: float = Field(..., ge=0, description="Score for this criterion")
    max_score: Optional[float] = Field(None, description="Maximum score for criterion")
    weight: Optional[float] = Field(None, description="Weight of criterion")
    is_required: bool = Field(default=True, description="Whether criterion is required")
    passes_threshold: Optional[bool] = Field(None, description="Whether criterion passes threshold")
    comments: Optional[str] = Field(None, description="Comments for this criterion")
    evidence: Optional[str] = Field(None, description="Specific examples/evidence")

class FeedbackCreate(BaseModel):
    interviewer_id: uuid.UUID = Field(..., description="Interviewer user ID")
    panel_member_id: Optional[uuid.UUID] = Field(None, description="Panel member ID if applicable")
    overall_rating: Optional[int] = Field(None, ge=1, le=5, description="Overall rating 1-5")
    recommendation: Optional[str] = Field(None, description="Overall recommendation")
    strengths: Optional[str] = Field(None, description="Candidate strengths")
    weaknesses: Optional[str] = Field(None, description="Candidate weaknesses")
    detailed_comments: Optional[str] = Field(None, description="Detailed feedback comments")
    criterion_scores: List[CriterionScoreCreate] = Field(..., description="Scores for each criterion")

class FeedbackUpdate(BaseModel):
    overall_rating: Optional[int] = Field(None, ge=1, le=5)
    recommendation: Optional[str] = Field(None)
    strengths: Optional[str] = Field(None)
    weaknesses: Optional[str] = Field(None)
    detailed_comments: Optional[str] = Field(None)
    criterion_scores: Optional[List[CriterionScoreCreate]] = Field(None)

class CriterionScoreResponse(BaseModel):
    id: uuid.UUID
    criterion_id: uuid.UUID
    score: float
    max_score: float
    weight: float
    comments: Optional[str]
    evidence: Optional[str]
    is_required: bool
    passes_threshold: bool
    
    class Config:
        from_attributes = True

class FeedbackResponse(BaseModel):
    id: uuid.UUID
    interview_id: uuid.UUID
    interviewer_id: uuid.UUID
    panel_member_id: Optional[uuid.UUID]
    overall_rating: Optional[int]
    overall_score: Optional[float]
    recommendation: Optional[str]
    strengths: Optional[str]
    weaknesses: Optional[str]
    detailed_comments: Optional[str]
    submitted_at: Optional[datetime]
    status: str
    is_complete: bool
    criterion_scores: List[CriterionScoreResponse]
    
    class Config:
        from_attributes = True


# ==================== Scorecard Schemas ====================

class ScorecardResponse(BaseModel):
    id: uuid.UUID
    interview_id: uuid.UUID
    template_round_id: uuid.UUID
    overall_score: float
    max_possible_score: float
    percentage_score: float
    recommendation: str
    recommendation_confidence: float
    summary: Optional[str]
    calculated_at: datetime
    is_final: bool
    required_feedback_count: int
    received_feedback_count: int
    
    class Config:
        from_attributes = True


# ==================== Decision Schemas ====================

class DecisionCreate(BaseModel):
    decision: str = Field(..., description="Final decision: PASS, FAIL, HOLD, REVIEW_REQUIRED")
    decision_maker_role: str = Field(..., description="Role of the decision maker")
    justification: Optional[str] = Field(None, description="Justification for the decision")
    next_step: Optional[str] = Field(None, description="Next step in recruitment workflow")

class DecisionResponse(BaseModel):
    id: uuid.UUID
    interview_id: uuid.UUID
    decision: str
    decision_maker_id: uuid.UUID
    decision_maker_role: str
    decision_at: datetime
    justification: Optional[str]
    ai_recommendation: Optional[str]
    ai_confidence: Optional[float]
    ai_evidence: Optional[Dict[str, Any]]
    overrides_ai: bool
    next_step: Optional[str]
    
    class Config:
        from_attributes = True


# ==================== Assessment Schemas ====================

class AssessmentQuestionCreate(BaseModel):
    question_text: str = Field(..., description="Question text")
    question_type: str = Field(..., description="Type of question")
    options: Optional[Dict[str, Any]] = Field(None, description="Options for multiple choice")
    correct_answer: Optional[str] = Field(None, description="Correct answer")
    points: float = Field(default=1.0, gt=0, description="Points for this question")
    sequence_order: int = Field(default=0, ge=0, description="Order in the assessment")
    explanation: Optional[str] = Field(None, description="Explanation for correct answer")
    is_required: bool = Field(default=True, description="Whether this question is required")

class AssessmentTemplateCreate(BaseModel):
    assessment_type_id: uuid.UUID = Field(..., description="Assessment type ID")
    template_name: str = Field(..., description="Template name")
    description: Optional[str] = Field(None, description="Template description")
    duration_minutes: int = Field(default=60, ge=15, le=480, description="Duration in minutes")
    passing_score: float = Field(default=70.0, ge=0, le=100, description="Passing score percentage")
    max_attempts: int = Field(default=3, ge=1, le=10, description="Maximum allowed attempts")
    instructions: Optional[str] = Field(None, description="Assessment instructions")
    configuration: Optional[Dict[str, Any]] = Field(None, description="Type-specific configuration")
    questions: List[AssessmentQuestionCreate] = Field(..., description="Assessment questions")

class AssessmentCreate(BaseModel):
    job_id: uuid.UUID = Field(..., description="Job ID")
    assessment_template_id: uuid.UUID = Field(..., description="Assessment template ID")
    assessment_name: str = Field(..., description="Assessment name")
    description: Optional[str] = Field(None, description="Assessment description")
    interview_round_id: Optional[uuid.UUID] = Field(None, description="Interview round ID if linked")
    duration_minutes: int = Field(default=60, ge=15, le=480, description="Duration in minutes")
    due_date: Optional[datetime] = Field(None, description="Due date for the assessment")

class AssessmentAttemptCreate(BaseModel):
    candidate_id: uuid.UUID = Field(..., description="Candidate ID")

class AssessmentAnswerCreate(BaseModel):
    question_id: uuid.UUID = Field(..., description="Question ID")
    answer_text: str = Field(..., description="Answer text")
    time_spent_seconds: Optional[int] = Field(None, ge=0, description="Time spent on this question")

class AssessmentAttemptResponse(BaseModel):
    id: uuid.UUID
    assessment_id: uuid.UUID
    candidate_id: uuid.UUID
    attempt_number: int
    started_at: datetime
    submitted_at: Optional[datetime]
    time_spent_seconds: Optional[int]
    score: Optional[float]
    percentage_score: Optional[float]
    status: str
    ip_address: Optional[str]
    browser_info: Optional[str]
    
    class Config:
        from_attributes = True

class AssessmentResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    job_id: uuid.UUID
    assessment_template_id: uuid.UUID
    assessment_name: str
    description: Optional[str]
    interview_round_id: Optional[uuid.UUID]
    duration_minutes: int
    status: str
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Coding Test Schemas ====================

class CodingTestCreate(BaseModel):
    language: str = Field(..., description="Programming language")
    problem_statement: str = Field(..., description="Problem statement")
    input_format: Optional[str] = Field(None, description="Input format specification")
    output_format: Optional[str] = Field(None, description="Output format specification")
    constraints: Optional[str] = Field(None, description="Constraints description")
    test_cases: Optional[Dict[str, Any]] = Field(None, description="Test cases as JSON")
    starter_code: Optional[str] = Field(None, description="Starter code for candidates")
    time_limit_seconds: int = Field(default=300, ge=1, description="Time limit in seconds")
    memory_limit_mb: int = Field(default=256, ge=1, description="Memory limit in MB")

class CodingSubmissionCreate(BaseModel):
    coding_test_id: uuid.UUID = Field(..., description="Coding test ID")
    code: str = Field(..., description="Submitted code")
    language: str = Field(..., description="Programming language")

class CodingSubmissionResponse(BaseModel):
    id: uuid.UUID
    attempt_id: uuid.UUID
    coding_test_id: uuid.UUID
    language: str
    submitted_at: datetime
    execution_time_ms: Optional[int]
    memory_used_mb: Optional[int]
    test_cases_passed: int
    total_test_cases: int
    compilation_status: str
    compilation_error: Optional[str]
    
    class Config:
        from_attributes = True


# ==================== Evaluation Criterion Schemas ====================

class EvaluationCriterionCreate(BaseModel):
    criterion_name: str = Field(..., description="Name of the criterion")
    description: Optional[str] = Field(None, description="Description of the criterion")
    category: Optional[str] = Field(None, description="Category of the criterion")
    evaluation_type: str = Field(default="Score", description="Type of evaluation")
    default_weight: float = Field(default=1.0, ge=0, le=1, description="Default weight")
    default_max_score: float = Field(default=10.0, gt=0, description="Default maximum score")

class EvaluationCriterionResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    criterion_name: str
    description: Optional[str]
    category: Optional[str]
    evaluation_type: str
    default_weight: float
    default_max_score: float
    is_active: bool
    
    class Config:
        from_attributes = True


# ==================== Timeline and Audit Schemas ====================

class TimelineEventResponse(BaseModel):
    id: uuid.UUID
    interview_id: uuid.UUID
    event_name: str
    event_time: datetime
    
    class Config:
        from_attributes = True

class AuditLogResponse(BaseModel):
    id: uuid.UUID
    interview_id: uuid.UUID
    action: str
    action_by: uuid.UUID
    action_at: datetime
    
    class Config:
        from_attributes = True


# ==================== AI Hook Schemas (for future LangGraph integration) ====================

class AIAnalysisRequest(BaseModel):
    interview_id: uuid.UUID = Field(..., description="Interview ID")
    analysis_type: str = Field(..., description="Type of AI analysis")

class AIAnalysisResponse(BaseModel):
    id: uuid.UUID
    interview_id: uuid.UUID
    analysis_type: str
    analysis_text: str
    confidence_score: float
    model_version: Optional[str]
    generated_at: datetime
    is_used: bool
    
    class Config:
        from_attributes = True


# ==================== Dashboard and Analytics Schemas ====================

class InterviewDashboardResponse(BaseModel):
    total_interviews: int
    scheduled_interviews: int
    completed_interviews: int
    pending_feedback: int
    average_score: Optional[float]
    pass_rate: Optional[float]
    upcoming_interviews: List[InterviewResponse]
    recent_decisions: List[DecisionResponse]


# ==================== Search and Filter Schemas ====================

class InterviewSearchRequest(BaseModel):
    status: Optional[str] = Field(None, description="Filter by status")
    job_id: Optional[uuid.UUID] = Field(None, description="Filter by job")
    candidate_id: Optional[uuid.UUID] = Field(None, description="Filter by candidate")
    date_from: Optional[datetime] = Field(None, description="Filter interviews from this date")
    date_to: Optional[datetime] = Field(None, description="Filter interviews until this date")
    interviewer_id: Optional[uuid.UUID] = Field(None, description="Filter by interviewer")
    skip: int = Field(default=0, ge=0, description="Number of records to skip")
    limit: int = Field(default=100, ge=1, le=1000, description="Number of records to return")


# ==================== Utility Response Schemas ====================

class SuccessResponse(BaseModel):
    status: str = Field(default="success", description="Operation status")
    message: str = Field(..., description="Success message")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional data if applicable")

class ValidationErrorResponse(BaseModel):
    status: str = Field(default="error", description="Error status")
    message: str = Field(..., description="Error message")
    errors: Optional[List[str]] = Field(None, description="Detailed validation errors")