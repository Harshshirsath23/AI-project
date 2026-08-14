from enum import Enum


class CommunicationChannel(str, Enum):
    """Communication channels"""
    EMAIL = "Email"
    SMS = "SMS"
    WHATSAPP = "WhatsApp"
    IN_APP = "In-App"
    PUSH = "Push"
    WEBHOOK = "Webhook"


class MessageStatus(str, Enum):
    """Message lifecycle status"""
    QUEUED = "Queued"
    PROCESSING = "Processing"
    SENT = "Sent"
    DELIVERED = "Delivered"
    READ = "Read"
    FAILED = "Failed"
    RETRY = "Retry"
    BOUNCED = "Bounced"
    CANCELLED = "Cancelled"


class NotificationType(str, Enum):
    """Notification types"""
    INTERVIEW_SCHEDULED = "Interview Scheduled"
    INTERVIEW_RESCHEDULED = "Interview Rescheduled"
    INTERVIEW_CANCELLED = "Interview Cancelled"
    OFFER_SENT = "Offer Sent"
    OFFER_ACCEPTED = "Offer Accepted"
    OFFER_REJECTED = "Offer ReJECTED"
    CANDIDATE_RESPONDED = "Candidate Responded"
    APPLICATION_RECEIVED = "Application Received"
    SCREENING_COMPLETED = "Screening Completed"
    BGV_INITIATED = "BGV Initiated"
    BGV_COMPLETED = "BGV Completed"
    ONBOARDING_STARTED = "Onboarding Started"
    SYSTEM_ALERT = "System Alert"
    REMINDER = "Reminder"


class NotificationPriority(str, Enum):
    """Notification priority levels"""
    LOW = "Low"
    NORMAL = "Normal"
    HIGH = "High"
    URGENT = "Urgent"


class ConversationType(str, Enum):
    """Conversation types based on entity association"""
    CANDIDATE = "Candidate"
    APPLICATION = "Application"
    JOB = "Job"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    GENERAL = "General"


class MessageDirection(str, Enum):
    """Message direction"""
    OUTBOUND = "Outbound"  # From system to recipient
    INBOUND = "Inbound"  # From recipient to system
    INTERNAL = "Internal"  # Internal team communication


class WebhookEvent(str, Enum):
    """Webhook event types from external providers"""
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    REPLIED = "replied"
    BOUNCED = "bounced"
    CLICKED = "clicked"
    UNSUBSCRIBED = "unsubscribed"


class WebhookStatus(str, Enum):
    """Webhook processing status"""
    RECEIVED = "Received"
    PROCESSED = "Processed"
    FAILED = "Failed"
    RETRY = "Retry"


class AutomationPolicy(str, Enum):
    """Automation policy for communication"""
    AUTO_SEND = "Auto Send"
    HUMAN_APPROVAL = "Human Approval"
    MANUAL = "Manual"
    CONDITIONAL = "Conditional"


class NotificationChannelPreference(str, Enum):
    """User notification channel preferences"""
    ENABLED = "Enabled"
    DISABLED = "Disabled"
    EMAIL_ONLY = "Email Only"
    IN_APP_ONLY = "In-App Only"


class AuditAction(str, Enum):
    """Communication audit action types"""
    TEMPLATE_CREATED = "Template Created"
    TEMPLATE_MODIFIED = "Template Modified"
    TEMPLATE_DELETED = "Template Deleted"
    MESSAGE_QUEUED = "Message Queued"
    MESSAGE_SENT = "Message Sent"
    MESSAGE_DELIVERED = "Message Delivered"
    MESSAGE_FAILED = "Message Failed"
    MESSAGE_RETRIED = "Message Retried"
    CONVERSATION_CREATED = "Conversation Created"
    CONVERSATION_UPDATED = "Conversation Updated"
    WEBHOOK_RECEIVED = "Webhook Received"
    WEBHOOK_PROCESSED = "Webhook Processed"
    NOTIFICATION_PREFERENCES_UPDATED = "Notification Preferences Updated"
    AUTOMATION_POLICY_CHANGED = "Automation Policy Changed"


class AIAnalysisType(str, Enum):
    """AI analysis types for future LangGraph integration"""
    MESSAGE_DRAFTING = "Message Drafting"
    CONVERSATION_SUMMARY = "Conversation Summary"
    SENTIMENT_ANALYSIS = "Sentiment Analysis"
    COMMUNICATION_TIMING = "Communication Timing"
    ROUTINE_QUESTION_ANSWERING = "Routine Question Answering"
    FOLLOW_UP_RECOMMENDATION = "Follow-up Recommendation"
    COMMUNICATION_CLASSIFICATION = "Communication Classification"