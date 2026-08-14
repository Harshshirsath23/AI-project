from enum import Enum


class AgentStatus(str, Enum):
    """Agent lifecycle status"""
    DRAFT = "Draft"
    ACTIVE = "Active"
    DEPRECATED = "Deprecated"
    ARCHIVED = "Archived"


class AgentType(str, Enum):
    """Agent type classification"""
    PARSER = "Parser"
    SCREENING = "Screening"
    RANKING = "Ranking"
    COORDINATION = "Coordination"
    ANALYSIS = "Analysis"
    COMMUNICATION = "Communication"
    KNOWLEDGE = "Knowledge"
    SUPERVISOR = "Supervisor"


class ExecutionStatus(str, Enum):
    """AI execution lifecycle status"""
    QUEUED = "Queued"
    RUNNING = "Running"
    WAITING_HITL = "Waiting_HITL"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"
    TIMED_OUT = "Timed_Out"


class ToolRisk(str, Enum):
    """Tool risk level for authorization"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class HITLRequirement(str, Enum):
    """HITL requirement level"""
    NOT_REQUIRED = "Not_Required"
    RECOMMENDED = "Recommended"
    REQUIRED = "Required"
    ALWAYS = "Always"


class PromptStatus(str, Enum):
    """Prompt template status"""
    DRAFT = "Draft"
    ACTIVE = "Active"
    ARCHIVED = "Archived"


class DocumentType(str, Enum):
    """Knowledge document type"""
    POLICY = "Policy"
    GUIDELINE = "Guideline"
    JOB_DESCRIPTION = "Job_Description"
    INTERVIEW_GUIDE = "Interview_Guide"
    HR_DOCUMENT = "HR_Document"
    COMPENSATION_POLICY = "Compensation_Policy"
    TRAINING_MATERIAL = "Training_Material"
    INTERNAL_DOCUMENT = "Internal_Document"
    RECRUITMENT_KNOWLEDGE = "Recruitment_Knowledge"


class EmbeddingStatus(str, Enum):
    """Embedding processing status"""
    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"


class WorkflowStatus(str, Enum):
    """Workflow status"""
    DRAFT = "Draft"
    ACTIVE = "Active"
    PAUSED = "Paused"
    ARCHIVED = "Archived"


class HITLDecision(str, Enum):
    """Human-in-the-loop decision types"""
    APPROVE = "Approve"
    REJECT = "Reject"
    MODIFY = "Modify"
    ESCALATE = "Escalate"


class GuardrailType(str, Enum):
    """AI guardrail type"""
    INPUT_VALIDATION = "Input_Validation"
    OUTPUT_VALIDATION = "Output_Validation"
    TOOL_AUTHORIZATION = "Tool_Authorization"
    TENANT_ISOLATION = "Tenant_Isolation"
    RATE_LIMITING = "Rate_Limiting"
    CONTENT_FILTERING = "Content_Filtering"


class ModelProvider(str, Enum):
    """Model provider"""
    OPENAI = "OpenAI"
    ANTHROPIC = "Anthropic"
    AZURE_OPENAI = "Azure_OpenAI"
    GOOGLE = "Google"
    LOCAL = "Local"
    CUSTOM = "Custom"