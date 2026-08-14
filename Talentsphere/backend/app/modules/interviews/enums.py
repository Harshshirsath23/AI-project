from enum import Enum


class InterviewStatus(str, Enum):
    """Interview status lifecycle"""
    PLANNED = "Planned"
    SCHEDULED = "Scheduled"
    INVITATION_SENT = "Invitation Sent"
    CONFIRMED = "Confirmed"
    STARTED = "Started"
    COMPLETED = "Completed"
    FEEDBACK_SUBMITTED = "Feedback Submitted"
    EVALUATION_COMPLETED = "Evaluation Completed"
    DECISION_PUBLISHED = "Decision Published"
    CANCELLED = "Cancelled"
    RESCHEDULED = "Rescheduled"
    NO_SHOW = "No Show"
    EXPIRED = "Expired"


class InterviewMode(str, Enum):
    """Interview delivery modes"""
    ONLINE = "Online"
    IN_PERSON = "In-person"
    PHONE = "Phone"
    VIDEO = "Video"
    CUSTOM = "Custom"


class InterviewType(str, Enum):
    """Interview types"""
    VIRTUAL = "Virtual"
    ONSITE = "Onsite"
    PHONE = "Phone"
    VIDEO = "Video"
    ASSESSMENT = "Assessment"


class FeedbackStatus(str, Enum):
    """Feedback submission status"""
    PENDING = "Pending"
    SUBMITTED = "Submitted"
    LOCKED = "Locked"
    SKIPPED = "Skipped"


class EvaluationType(str, Enum):
    """Evaluation criterion types"""
    RATING = "Rating"  # 1-5 scale
    SCORE = "Score"  # Numerical score
    PASS_FAIL = "PassFail"  # Pass/Fail
    TEXT = "Text"  # Text comments only


class DecisionType(str, Enum):
    """Interview decision types"""
    PASS = "PASS"
    FAIL = "FAIL"
    HOLD = "HOLD"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class RecommendationType(str, Enum):
    """Interviewer recommendation types"""
    STRONG_HIRE = "Strong Hire"
    HIRE = "Hire"
    NO_HIRE = "No Hire"
    STRONG_NO_HIRE = "Strong No Hire"


class AssessmentStatus(str, Enum):
    """Assessment status"""
    ACTIVE = "Active"
    ARCHIVED = "Archived"


class AssessmentAttemptStatus(str, Enum):
    """Assessment attempt status"""
    IN_PROGRESS = "InProgress"
    SUBMITTED = "Submitted"
    EVALUATED = "Evaluated"
    PASSED = "Passed"
    FAILED = "Failed"


class QuestionType(str, Enum):
    """Assessment question types"""
    MULTIPLE_CHOICE = "MultipleChoice"
    CODING = "Coding"
    FREE_TEXT = "FreeText"
    TRUE_FALSE = "TrueFalse"
    ESSAY = "Essay"


class AssessmentType(str, Enum):
    """Assessment types"""
    INTERVIEW = "Interview"
    CODING = "Coding"
    WRITTEN = "Written"
    CUSTOM = "Custom"


class CompilationStatus(str, Enum):
    """Coding test compilation status"""
    SUCCESS = "Success"
    ERROR = "Error"
    TIMEOUT = "Timeout"
    MEMORY_LIMIT = "Memory Limit"


class InterviewerRole(str, Enum):
    """Interviewer roles in panel"""
    PRIMARY_INTERVIEWER = "Primary Interviewer"
    TECHNICAL_EXPERT = "Technical Expert"
    HIRING_MANAGER = "Hiring Manager"
    HR_INTERVIEWER = "HR Interviewer"
    OBSERVER = "Observer"
    PEER_INTERVIEWER = "Peer Interviewer"


class DecisionMakerRole(str, Enum):
    """Decision maker roles"""
    RECRUITER = "Recruiter"
    HIRING_MANAGER = "Hiring Manager"
    HR = "HR"
    PANEL_LEAD = "Panel Lead"


class TimelineEventType(str, Enum):
    """Interview timeline event types"""
    INTERVIEW_CREATED = "Interview Created"
    INTERVIEW_SCHEDULED = "Interview Scheduled"
    INTERVIEW_RESCHEDULED = "Interview Rescheduled"
    INTERVIEW_CANCELLED = "Interview Cancelled"
    INTERVIEW_STARTED = "Interview Started"
    INTERVIEW_COMPLETED = "Interview Completed"
    FEEDBACK_SUBMITTED = "Feedback Submitted"
    EVALUATION_GENERATED = "Evaluation Generated"
    DECISION_MADE = "Decision Made"
    NOTIFICATION_SENT = "Notification Sent"
    REMINDER_SENT = "Reminder Sent"


class NotificationType(str, Enum):
    """Interview notification types"""
    SCHEDULE = "Schedule"
    RESCHEDULE = "Reschedule"
    CANCELLATION = "Cancellation"
    REMINDER = "Reminder"
    FEEDBACK_REQUEST = "Feedback Request"
    DECISION_PUBLISHED = "Decision Published"


class AuditAction(str, Enum):
    """Interview audit actions"""
    CREATE = "Create"
    UPDATE = "Update"
    DELETE = "Delete"
    SCHEDULE = "Schedule"
    RESCHEDULE = "Reschedule"
    CANCEL = "Cancel"
    COMPLETE = "Complete"
    SUBMIT_FEEDBACK = "Submit Feedback"
    LOCK_FEEDBACK = "Lock Feedback"
    CALCULATE_SCORECARD = "Calculate Scorecard"
    MAKE_DECISION = "Make Decision"
    ASSIGN_INTERVIEWER = "Assign Interviewer"
    REMOVE_INTERVIEWER = "Remove Interviewer"
    ADD_PANEL_MEMBER = "Add Panel Member"
    REMOVE_PANEL_MEMBER = "Remove Panel Member"


class CriterionCategory(str, Enum):
    """Evaluation criterion categories"""
    TECHNICAL = "Technical"
    BEHAVIORAL = "Behavioral"
    CULTURAL_FIT = "Cultural Fit"
    COMMUNICATION = "Communication"
    LEADERSHIP = "Leadership"
    PROBLEM_SOLVING = "Problem Solving"
    DOMAIN_KNOWLEDGE = "Domain Knowledge"


class AIAnalysisType(str, Enum):
    """AI analysis types for future LangGraph integration"""
    TRANSCRIPT = "Transcript"
    SENTIMENT = "Sentiment"
    BEHAVIOR = "Behavior"
    RECOMMENDATION = "Recommendation"
    FEEDBACK_SUMMARY = "Feedback Summary"


class AIFeedbackType(str, Enum):
    """AI feedback types for future LangGraph integration"""
    STRENGTHS = "Strengths"
    WEAKNESSES = "Weaknesses"
    OVERALL = "Overall"
    RECOMMENDATION = "Recommendation"
    SCORE_BREAKDOWN = "Score Breakdown"