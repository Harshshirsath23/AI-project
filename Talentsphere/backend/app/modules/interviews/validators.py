from datetime import datetime, timedelta
from typing import List, Optional, Any
import uuid
from fastapi import HTTPException, status

from app.modules.interviews.enums import (
    InterviewStatus, InterviewMode, FeedbackStatus, EvaluationType,
    DecisionType, AssessmentAttemptStatus, CompilationStatus
)
from app.modules.interviews.exceptions import (
    InvalidScheduleException, InterviewAlreadyCompletedException,
    InterviewCancelledException, ReschedulingNotAllowedException,
    InsufficientReschedulingNoticeException, IncompleteFeedbackException,
    InvalidInterviewStatusException, InvalidDecisionException,
    PanelValidationException
)


class InterviewValidator:
    """Validator for interview operations"""
    
    @staticmethod
    def validate_schedule_time(
        start_time: datetime,
        end_time: datetime,
        timezone: str = "UTC"
    ) -> None:
        """Validate interview schedule time"""
        if start_time >= end_time:
            raise InvalidScheduleException("Start time must be before end time")
        
        if start_time < datetime.now():
            raise InvalidScheduleException("Start time cannot be in the past")
        
        duration = (end_time - start_time).total_seconds() / 60
        if duration < 15:
            raise InvalidScheduleException("Interview duration must be at least 15 minutes")
        
        if duration > 480:  # 8 hours
            raise InvalidScheduleException("Interview duration cannot exceed 8 hours")
    
    @staticmethod
    def validate_rescheduling(
        current_status: str,
        scheduled_start: datetime,
        new_start: datetime,
        min_rescheduling_hours: int = 24
    ) -> None:
        """Validate interview rescheduling request"""
        if current_status in [InterviewStatus.COMPLETED, InterviewStatus.DECISION_PUBLISHED]:
            raise InterviewAlreadyCompletedException("Cannot reschedule completed interview")
        
        if current_status == InterviewStatus.CANCELLED:
            raise InterviewCancelledException("Cannot reschedule cancelled interview")
        
        if current_status == InterviewStatus.STARTED:
            raise InvalidScheduleException("Cannot reschedule interview that has already started")
        
        hours_until_scheduled = (scheduled_start - datetime.now()).total_seconds() / 3600
        if hours_until_scheduled < min_rescheduling_hours:
            raise InsufficientReschedulingNoticeException(min_rescheduling_hours)
        
        if new_start < datetime.now():
            raise InvalidScheduleException("New start time cannot be in the past")
    
    @staticmethod
    def validate_status_transition(
        current_status: str,
        new_status: str,
        allowed_transitions: Optional[dict] = None
    ) -> None:
        """Validate interview status transition"""
        if current_status == new_status:
            return
        
        if allowed_transitions is None:
            allowed_transitions = {
                InterviewStatus.PLANNED: [InterviewStatus.SCHEDULED, InterviewStatus.CANCELLED],
                InterviewStatus.SCHEDULED: [InterviewStatus.CONFIRMED, InterviewStatus.RESCHEDULED, InterviewStatus.CANCELLED],
                InterviewStatus.CONFIRMED: [InterviewStatus.STARTED, InterviewStatus.RESCHEDULED, InterviewStatus.CANCELLED],
                InterviewStatus.STARTED: [InterviewStatus.COMPLETED, InterviewStatus.NO_SHOW],
                InterviewStatus.COMPLETED: [InterviewStatus.FEEDBACK_SUBMITTED],
                InterviewStatus.FEEDBACK_SUBMITTED: [InterviewStatus.EVALUATION_COMPLETED],
                InterviewStatus.EVALUATION_COMPLETED: [InterviewStatus.DECISION_PUBLISHED],
                InterviewStatus.RESCHEDULED: [InterviewStatus.SCHEDULED],
                InterviewStatus.CANCELLED: [],  # Terminal state
                InterviewStatus.NO_SHOW: [InterviewStatus.RESCHEDULED, InterviewStatus.CANCELLED],
                InterviewStatus.DECISION_PUBLISHED: [],  # Terminal state
            }
        
        if current_status not in allowed_transitions:
            raise InvalidInterviewStatusException(current_status, "Unknown current status")
        
        if new_status not in allowed_transitions[current_status]:
            raise InvalidInterviewStatusException(current_status, new_status)
    
    @staticmethod
    def validate_cancellation(current_status: str) -> None:
        """Validate interview cancellation"""
        if current_status in [InterviewStatus.COMPLETED, InterviewStatus.DECISION_PUBLISHED]:
            raise InterviewAlreadyCompletedException("Cannot cancel completed interview")
        
        if current_status == InterviewStatus.CANCELLED:
            raise InterviewCancelledException("Interview is already cancelled")
        
        if current_status == InterviewStatus.STARTED:
            raise InvalidScheduleException("Cannot cancel interview that has already started")


class FeedbackValidator:
    """Validator for interview feedback operations"""
    
    @staticmethod
    def validate_feedback_submission(
        current_status: str,
        feedback_status: str,
        required_criteria_count: int,
        scored_criteria_count: int
    ) -> None:
        """Validate feedback submission"""
        if current_status != InterviewStatus.COMPLETED:
            raise InvalidInterviewStatusException(current_status, InterviewStatus.COMPLETED)
        
        if feedback_status == FeedbackStatus.SUBMITTED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Feedback has already been submitted"
            )
        
        if feedback_status == FeedbackStatus.LOCKED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Feedback is locked and cannot be modified"
            )
        
        if required_criteria_count > 0 and scored_criteria_count < required_criteria_count:
            raise IncompleteFeedbackException(
                f"Required {required_criteria_count} criteria, but only {scored_criteria_count} scored"
            )
    
    @staticmethod
    def validate_criterion_score(
        score: float,
        max_score: float,
        evaluation_type: str
    ) -> None:
        """Validate individual criterion score"""
        if evaluation_type == EvaluationType.PASS_FAIL:
            if score not in [0.0, 1.0]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Pass/Fail criteria must have score of 0.0 or 1.0"
                )
        else:
            if score < 0 or score > max_score:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Score must be between 0 and {max_score}"
                )
    
    @staticmethod
    def validate_recommendation(recommendation: str) -> None:
        """Validate interviewer recommendation"""
        valid_recommendations = ["Strong Hire", "Hire", "No Hire", "Strong No Hire"]
        if recommendation not in valid_recommendations:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid recommendation. Must be one of: {', '.join(valid_recommendations)}"
            )


class ScorecardValidator:
    """Validator for scorecard operations"""
    
    @staticmethod
    def validate_scorecard_creation(
        interview_status: str,
        required_feedback_count: int,
        received_feedback_count: int
    ) -> None:
        """Validate scorecard creation conditions"""
        if interview_status != InterviewStatus.FEEDBACK_SUBMITTED:
            raise InvalidInterviewStatusException(
                interview_status,
                InterviewStatus.FEEDBACK_SUBMITTED
            )
        
        if received_feedback_count < required_feedback_count:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient feedback for scorecard. Required: {required_feedback_count}, Received: {received_feedback_count}"
            )
    
    @staticmethod
    def validate_weighted_score(weights: List[float]) -> None:
        """Validate that weights sum to 1.0 (or close to it)"""
        total_weight = sum(weights)
        if abs(total_weight - 1.0) > 0.01:  # Allow small floating point errors
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Criterion weights must sum to 1.0. Current sum: {total_weight}"
            )


class AssessmentValidator:
    """Validator for assessment operations"""
    
    @staticmethod
    def validate_assessment_attempt(
        current_attempt_number: int,
        max_attempts: int,
        assessment_status: str,
        due_date: Optional[datetime] = None
    ) -> None:
        """Validate assessment attempt creation"""
        if current_attempt_number >= max_attempts:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Maximum assessment attempts ({max_attempts}) exceeded"
            )
        
        if assessment_status != "Active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assessment is not active"
            )
        
        if due_date and datetime.now() > due_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assessment has expired"
            )
    
    @staticmethod
    def validate_assessment_submission(
        attempt_status: str,
        submission_time: Optional[datetime] = None
    ) -> None:
        """Validate assessment submission"""
        if attempt_status == AssessmentAttemptStatus.SUBMITTED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assessment has already been submitted"
            )
        
        if attempt_status != AssessmentAttemptStatus.IN_PROGRESS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot submit assessment with status: {attempt_status}"
            )
    
    @staticmethod
    def validate_coding_submission(
        code: str,
        language: str,
        supported_languages: List[str]
    ) -> None:
        """Validate coding test submission"""
        if not code or len(code.strip()) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Code submission is too short or empty"
            )
        
        if language not in supported_languages:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Language {language} is not supported. Supported: {', '.join(supported_languages)}"
            )


class DecisionValidator:
    """Validator for interview decision operations"""
    
    @staticmethod
    def validate_decision_creation(
        interview_status: str,
        existing_decision: bool
    ) -> None:
        """Validate decision creation"""
        if interview_status != InterviewStatus.EVALUATION_COMPLETED:
            raise InvalidInterviewStatusException(
                interview_status,
                InterviewStatus.EVALUATION_COMPLETED
            )
        
        if existing_decision:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Decision has already been made for this interview"
            )
    
    @staticmethod
    def validate_decision_value(decision: str) -> None:
        """Validate decision value"""
        valid_decisions = [d.value for d in DecisionType]
        if decision not in valid_decisions:
            raise InvalidDecisionException(decision)
    
    @staticmethod
    def validate_decision_authority(
        user_role: str,
        required_roles: List[str]
    ) -> None:
        """Validate that user has authority to make decision"""
        if user_role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User role '{user_role}' is not authorized to make decisions. Required roles: {', '.join(required_roles)}"
            )


class PanelValidator:
    """Validator for interview panel operations"""
    
    @staticmethod
    def validate_panel_composition(
        panel_size: int,
        required_interviewers: int,
        primary_interviewer_count: int
    ) -> None:
        """Validate panel composition"""
        if panel_size < required_interviewers:
            raise PanelValidationException(
                f"Panel size ({panel_size}) is less than required interviewers ({required_interviewers})"
            )
        
        if primary_interviewer_count != 1:
            raise PanelValidationException(
                f"Panel must have exactly one primary interviewer. Current: {primary_interviewer_count}"
            )
    
    @staticmethod
    def validate_interviewer_availability(
        current_workload: int,
        max_capacity: int
    ) -> None:
        """Validate interviewer availability"""
        if current_workload >= max_capacity:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Interviewer has reached maximum capacity ({max_capacity})"
            )
    
    @staticmethod
    def validate_role_requirements(
        panel_roles: List[str],
        required_roles: List[str]
    ) -> None:
        """Validate that panel has required roles"""
        missing_roles = set(required_roles) - set(panel_roles)
        if missing_roles:
            raise PanelValidationException(
                f"Panel is missing required roles: {', '.join(missing_roles)}"
            )


class TemplateValidator:
    """Validator for interview template operations"""
    
    @staticmethod
    def validate_template_rounds(rounds: List[Any]) -> None:
        """Validate template rounds configuration"""
        if not rounds:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Template must have at least one round"
            )
        
        def get_val(item, key, default=None):
            return item.get(key, default) if isinstance(item, dict) else getattr(item, key, default)

        sequence_numbers = [get_val(r, 'sequence_number', 0) for r in rounds]
        if len(set(sequence_numbers)) != len(sequence_numbers):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Round sequence numbers must be unique"
            )
        
        for round_item in rounds:
            duration = get_val(round_item, 'duration_minutes', 0)
            if duration < 15:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Each round must be at least 15 minutes"
                )
            
            interviewers = get_val(round_item, 'required_interviewers', 0)
            if interviewers < 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Each round must require at least one interviewer"
                )
    
    @staticmethod
    def validate_criteria_configuration(criteria: List[Any]) -> None:
        """Validate evaluation criteria configuration"""
        if not criteria:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Round must have at least one evaluation criterion"
            )
        
        def get_val(item, key, default=None):
            return item.get(key, default) if isinstance(item, dict) else getattr(item, key, default)

        total_weight = sum(float(get_val(c, 'weight', 0)) for c in criteria)
        if abs(total_weight - 1.0) > 0.01:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Criterion weights must sum to 1.0. Current sum: {total_weight}"
            )
        
        for criterion in criteria:
            max_score = float(get_val(criterion, 'max_score', 0))
            if max_score <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Each criterion must have a positive max_score"
                )
            
            weight = float(get_val(criterion, 'weight', 0))
            if weight <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Each criterion must have a positive weight"
                )