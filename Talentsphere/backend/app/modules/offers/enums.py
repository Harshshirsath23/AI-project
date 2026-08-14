from enum import Enum


class OfferStatus(str, Enum):
    """Offer status lifecycle"""
    DRAFT = "Draft"
    PENDING_APPROVAL = "Pending Approval"
    APPROVED = "Approved"
    GENERATED = "Generated"
    SENT = "Sent"
    VIEWED = "Viewed"
    NEGOTIATING = "Negotiating"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    EXPIRED = "Expired"
    WITHDRAWN = "Withdrawn"
    JOINING_CONFIRMED = "Joining Confirmed"


class ApprovalStatus(str, Enum):
    """Offer approval status"""
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    SKIPPED = "Skipped"


class EmploymentType(str, Enum):
    """Employment types"""
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    INTERNSHIP = "Internship"
    FREELANCE = "Freelance"


class WorkMode(str, Enum):
    """Work location modes"""
    ON_SITE = "On-site"
    REMOTE = "Remote"
    HYBRID = "Hybrid"


class PayFrequency(str, Enum):
    """Payment frequency"""
    MONTHLY = "Monthly"
    BI_WEEKLY = "Bi-weekly"
    WEEKLY = "Weekly"
    DAILY = "Daily"


class NegotiationStatus(str, Enum):
    """Negotiation status"""
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    COUNTER_OFFER = "Counter-offer"


class NegotiatorType(str, Enum):
    """Negotiator types"""
    CANDIDATE = "Candidate"
    RECRUITER = "Recruiter"
    MANAGER = "Manager"
    HR = "HR"


class BGVStatus(str, Enum):
    """Background verification status"""
    INITIATED = "Initiated"
    IN_PROGRESS = "InProgress"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"


class CheckItemType(str, Enum):
    """Background check item types"""
    EMPLOYMENT = "Employment"
    EDUCATION = "Education"
    CRIMINAL = "Criminal"
    IDENTITY = "Identity"
    ADDRESS = "Address"
    REFERENCE = "Reference"
    DRUG_TEST = "Drug Test"
    CREDIT_CHECK = "Credit Check"


class CheckItemStatus(str, Enum):
    """Background check item status"""
    PENDING = "Pending"
    IN_PROGRESS = "InProgress"
    PASSED = "Passed"
    FAILED = "Failed"
    SKIPPED = "Skipped"


class RiskLevel(str, Enum):
    """Risk assessment levels"""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    NONE = "None"


class TaskType(str, Enum):
    """Onboarding task types"""
    DOCUMENTATION = "Documentation"
    TRAINING = "Training"
    MEETING = "Meeting"
    EQUIPMENT = "Equipment"
    ADMINISTRATIVE = "Administrative"
    ORIENTATION = "Orientation"
    SYSTEM_ACCESS = "System Access"


class TaskStatus(str, Enum):
    """Onboarding task status"""
    PENDING = "Pending"
    IN_PROGRESS = "InProgress"
    COMPLETED = "Completed"
    SKIPPED = "Skipped"
    OVERDUE = "Overdue"


class TaskPriority(str, Enum):
    """Task priority levels"""
    HIGH = "High"
    NORMAL = "Normal"
    LOW = "Low"


class OnboardingStatus(str, Enum):
    """Onboarding overall status"""
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "InProgress"
    COMPLETED = "Completed"
    DELAYED = "Delayed"
    CANCELLED = "Cancelled"


class ApprovalAction(str, Enum):
    """Approval action types"""
    SUBMIT = "Submit"
    APPROVE = "Approve"
    REJECT = "Reject"
    CANCEL = "Cancel"
    REQUEST_CHANGES = "Request Changes"


class ApproverRole(str, Enum):
    """Approver roles"""
    HR_MANAGER = "HR Manager"
    HIRING_MANAGER = "Hiring Manager"
    FINANCE_MANAGER = "Finance Manager"
    DEPARTMENT_HEAD = "Department Head"
    CEO = "CEO"


class DocumentType(str, Enum):
    """Offer document types"""
    OFFER_LETTER = "Offer Letter"
    EMPLOYMENT_AGREEMENT = "Employment Agreement"
    NDA = "NDA"
    CONFIDENTIALITY_AGREEMENT = "Confidentiality Agreement"
    IP_ASSIGNMENT = "IP Assignment"
    BONUS_AGREEMENT = "Bonus Agreement"


class AuditAction(str, Enum):
    """Audit action types"""
    OFFER_CREATED = "Offer Created"
    OFFER_UPDATED = "Offer Updated"
    OFFER_APPROVED = "Offer Approved"
    OFFER_REJECTED = "Offer Rejected"
    OFFER_SENT = "Offer Sent"
    OFFER_VIEWED = "Offer Viewed"
    OFFER_ACCEPTED = "Offer Accepted"
    OFFER_REJECTED_BY_CANDIDATE = "Offer Rejected by Candidate"
    OFFER_EXPIRED = "Offer Expired"
    OFFER_WITHDRAWN = "Offer Withdrawn"
    COMPENSATION_REVISED = "Compensation Revised"
    NEGOTIATION_INITIATED = "Negotiation Initiated"
    BGV_INITIATED = "BGV Initiated"
    BGV_COMPLETED = "BGV Completed"
    ONBOARDING_STARTED = "Onboarding Started"
    ONBOARDING_COMPLETED = "Onboarding Completed"
    EMPLOYEE_CONVERTED = "Employee Converted"


class AIAnalysisType(str, Enum):
    """AI analysis types for future LangGraph integration"""
    COMPENSATION_INTELLIGENCE = "Compensation Intelligence"
    OFFER_DOCUMENT_GENERATION = "Offer Document Generation"
    NEGOTIATION_INTELLIGENCE = "Negotiation Intelligence"
    BGV_REVIEW = "BGV Review"
    ONBOARDING_PLANNING = "Onboarding Planning"
    RISK_ASSESSMENT = "Risk Assessment"