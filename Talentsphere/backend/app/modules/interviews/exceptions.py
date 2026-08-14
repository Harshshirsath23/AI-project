from typing import Optional
from fastapi import HTTPException, status


class InterviewException(Exception):
    """Base exception for interview module"""
    pass


class InterviewTemplateException(InterviewException):
    """Exception for interview template operations"""
    pass


class InterviewSchedulingException(InterviewException):
    """Exception for interview scheduling operations"""
    pass


class InterviewFeedbackException(InterviewException):
    """Exception for interview feedback operations"""
    pass


class AssessmentException(InterviewException):
    """Exception for assessment operations"""
    pass


class InterviewDecisionException(InterviewException):
    """Exception for interview decision operations"""
    pass


# Template Exceptions
class TemplateNotFound(HTTPException):
    def __init__(self, template_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Interview template with ID {template_id} not found"
        )


class TemplateValidationError(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Template validation failed: {message}"
        )


class TemplateInUseException(HTTPException):
    def __init__(self, template_id: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot delete template {template_id} as it is being used by active interviews"
        )


# Scheduling Exceptions
class InterviewNotFound(HTTPException):
    def __init__(self, interview_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Interview with ID {interview_id} not found"
        )


class InterviewerUnavailableException(HTTPException):
    def __init__(self, interviewer_id: str, message: str = "Interviewer is not available at the requested time"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Interviewer {interviewer_id}: {message}"
        )


class InvalidScheduleException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid schedule: {message}"
        )


class InterviewAlreadyCompletedException(HTTPException):
    def __init__(self, interview_id: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Interview {interview_id} is already completed and cannot be modified"
        )


class InterviewCancelledException(HTTPException):
    def __init__(self, interview_id: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Interview {interview_id} has been cancelled"
        )


class ReschedulingNotAllowedException(HTTPException):
    def __init__(self, message: str = "Rescheduling is not allowed for this interview"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )


class InsufficientReschedulingNoticeException(HTTPException):
    def __init__(self, min_hours: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Rescheduling requires at least {min_hours} hours notice"
        )


# Feedback Exceptions
class FeedbackAlreadySubmittedException(HTTPException):
    def __init__(self, interviewer_id: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Feedback from interviewer {interviewer_id} has already been submitted"
        )


class IncompleteFeedbackException(HTTPException):
    def __init__(self, message: str = "Feedback is incomplete. All required criteria must be scored"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )


class FeedbackLockedException(HTTPException):
    def __init__(self, feedback_id: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Feedback {feedback_id} is locked and cannot be modified"
        )


class InterviewerNotAssignedException(HTTPException):
    def __init__(self, interviewer_id: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Interviewer {interviewer_id} is not assigned to this interview"
        )


# Scorecard Exceptions
class ScorecardAlreadyExistsException(HTTPException):
    def __init__(self, interview_id: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Scorecard for interview {interview_id} already exists"
        )


class InsufficientFeedbackException(HTTPException):
    def __init__(self, required: int, received: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient feedback for scorecard calculation. Required: {required}, Received: {received}"
        )


class ScorecardCalculationException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Scorecard calculation failed: {message}"
        )


# Assessment Exceptions
class AssessmentNotFound(HTTPException):
    def __init__(self, assessment_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assessment with ID {assessment_id} not found"
        )


class AssessmentAttemptLimitExceededException(HTTPException):
    def __init__(self, max_attempts: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maximum assessment attempts ({max_attempts}) exceeded"
        )


class AssessmentExpiredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment has expired"
        )


class AssessmentAlreadySubmittedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment has already been submitted"
        )


class CodingTestExecutionException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Coding test execution failed: {message}"
        )


# Decision Exceptions
class DecisionAlreadyMadeException(HTTPException):
    def __init__(self, interview_id: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Decision for interview {interview_id} has already been made"
        )


class InvalidDecisionException(HTTPException):
    def __init__(self, decision: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid decision: {decision}. Must be one of: PASS, FAIL, HOLD, REVIEW_REQUIRED"
        )


class InsufficientPermissionsException(HTTPException):
    def __init__(self, action: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient permissions to perform action: {action}"
        )


class InterviewInProgressException(HTTPException):
    def __init__(self, interview_id: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Interview {interview_id} is currently in progress"
        )


class InvalidInterviewStatusException(HTTPException):
    def __init__(self, current_status: str, required_status: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid interview status transition. Current: {current_status}, Required: {required_status}"
        )


class CriterionNotFoundException(HTTPException):
    def __init__(self, criterion_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evaluation criterion with ID {criterion_id} not found"
        )


class PanelValidationException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Panel validation failed: {message}"
        )