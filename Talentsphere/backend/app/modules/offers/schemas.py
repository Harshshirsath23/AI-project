from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
import uuid

from app.modules.offers.enums import (
    OfferStatus, ApprovalStatus, EmploymentType, WorkMode,
    PayFrequency, NegotiationStatus, NegotiatorType, BGVStatus,
    CheckItemType, CheckItemStatus, RiskLevel, TaskType, TaskStatus,
    TaskPriority, OnboardingStatus, ApproverRole, DocumentType
)


# ==================== Offer Template Schemas ====================

class OfferTemplateCreate(BaseModel):
    template_name: str = Field(..., description="Name of the offer template")
    description: Optional[str] = Field(None, description="Template description")
    job_category: Optional[str] = Field(None, description="Job category for this template")
    is_default: bool = Field(default=False, description="Whether this is the default template")
    template_content: Optional[Dict[str, Any]] = Field(None, description="Template structure and content")

class OfferTemplateResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    template_name: str
    description: Optional[str]
    job_category: Optional[str]
    is_default: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Offer Schemas ====================

class OfferCompensationCreate(BaseModel):
    currency_id: uuid.UUID = Field(..., description="Currency ID")
    base_salary: float = Field(..., gt=0, description="Base annual salary")
    variable_compensation: float = Field(default=0.0, ge=0, description="Variable compensation")
    joining_bonus: float = Field(default=0.0, ge=0, description="One-time joining bonus")
    bonus_percentage: float = Field(default=0.0, ge=0, le=100, description="Bonus percentage")
    allowances: Optional[Dict[str, float]] = Field(None, description="Allowances breakdown")
    benefits: Optional[Dict[str, Any]] = Field(None, description="Benefits configuration")
    pay_frequency: str = Field(default="Monthly", description="Payment frequency")

class OfferTermsCreate(BaseModel):
    employment_type: str = Field(default="Full-time", description="Employment type")
    probation_period_months: int = Field(default=3, ge=0, description="Probation period in months")
    notice_period_days: int = Field(default=30, ge=0, description="Notice period in days")
    work_location: str = Field(..., description="Work location")
    work_mode: str = Field(default="On-site", description="Work mode")
    reporting_manager_id: Optional[uuid.UUID] = Field(None, description="Reporting manager user ID")
    department_id: Optional[uuid.UUID] = Field(None, description="Department ID")
    team_id: Optional[uuid.UUID] = Field(None, description="Team ID")
    additional_terms: Optional[Dict[str, Any]] = Field(None, description="Additional terms")

class OfferCreate(BaseModel):
    candidate_application_id: uuid.UUID = Field(..., description="Candidate application ID")
    candidate_id: uuid.UUID = Field(..., description="Candidate ID")
    job_id: uuid.UUID = Field(..., description="Job ID")
    offered_designation_id: uuid.UUID = Field(..., description="Designation ID")
    offer_template_id: Optional[uuid.UUID] = Field(None, description="Offer template ID")
    issue_date: date = Field(..., description="Offer issue date")
    expiry_date: date = Field(..., description="Offer expiry date")
    start_date: date = Field(..., description="Employee start date")
    compensation: OfferCompensationCreate
    terms: OfferTermsCreate
    internal_notes: Optional[str] = Field(None, description="Internal notes")

class OfferUpdate(BaseModel):
    expiry_date: Optional[date] = Field(None, description="Updated expiry date")
    start_date: Optional[date] = Field(None, description="Updated start date")
    internal_notes: Optional[str] = Field(None, description="Updated internal notes")
    compensation: Optional[OfferCompensationCreate] = Field(None, description="Updated compensation")
    terms: Optional[OfferTermsCreate] = Field(None, description="Updated terms")

class OfferResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    candidate_application_id: uuid.UUID
    candidate_id: uuid.UUID
    job_id: uuid.UUID
    offered_designation_id: uuid.UUID
    hiring_plan_id: Optional[uuid.UUID]
    offer_template_id: Optional[uuid.UUID]
    issue_date: date
    expiry_date: date
    start_date: date
    status: str
    approval_status: str
    rejection_reason: Optional[str]
    internal_notes: Optional[str]
    created_by: uuid.UUID
    approved_by: Optional[uuid.UUID]
    approved_at: Optional[datetime]
    sent_at: Optional[datetime]
    viewed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Compensation Schemas ====================

class SalaryBandResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    job_id: uuid.UUID
    designation_id: uuid.UUID
    experience_level_id: Optional[uuid.UUID]
    currency_id: uuid.UUID
    min_salary: float
    max_salary: float
    median_salary: float
    is_active: bool
    
    class Config:
        from_attributes = True


class OfferCompensationResponse(BaseModel):
    id: uuid.UUID
    offer_id: uuid.UUID
    currency_id: uuid.UUID
    base_salary: float
    variable_compensation: float
    joining_bonus: float
    bonus_percentage: float
    allowances: Optional[Dict[str, float]]
    benefits: Optional[Dict[str, Any]]
    total_compensation: float
    pay_frequency: str
    salary_band_id: Optional[uuid.UUID]
    within_salary_band: bool
    band_violation_reason: Optional[str]
    
    class Config:
        from_attributes = True


# ==================== Approval Schemas ====================

class OfferApprovalRequest(BaseModel):
    approver_id: uuid.UUID = Field(..., description="Approver user ID")
    approver_role: str = Field(..., description="Approver role")
    approval_level: int = Field(default=1, description="Approval level")
    comments: Optional[str] = Field(None, description="Approval comments")

class OfferApprovalAction(BaseModel):
    action: str = Field(..., description="Approve or Reject")
    comments: Optional[str] = Field(None, description="Action comments")

class OfferApprovalResponse(BaseModel):
    id: uuid.UUID
    offer_id: uuid.UUID
    approver_id: uuid.UUID
    approver_role: str
    approval_level: int
    status: str
    comments: Optional[str]
    approved_at: Optional[datetime]
    sequence_order: int
    
    class Config:
        from_attributes = True


# ==================== Negotiation Schemas ====================

class NegotiationRequest(BaseModel):
    negotiator_type: str = Field(..., description="Candidate or Recruiter")
    negotiator_id: Optional[uuid.UUID] = Field(None, description="Negotiator user ID if internal")
    requested_base_salary: float = Field(..., ge=0, description="Requested base salary")
    requested_total_compensation: float = Field(..., ge=0, description="Requested total compensation")
    comments: str = Field(..., description="Negotiation comments")
    reason: Optional[str] = Field(None, description="Reason for negotiation")

class NegotiationResponse(BaseModel):
    proposed_base_salary: Optional[float] = Field(None, description="Counter-offer base salary")
    proposed_total_compensation: Optional[float] = Field(None, description="Counter-offer total compensation")

class OfferNegotiationResponse(BaseModel):
    id: uuid.UUID
    offer_id: uuid.UUID
    negotiator_type: str
    negotiator_id: Optional[uuid.UUID]
    negotiation_round: int
    requested_base_salary: float
    requested_total_compensation: float
    comments: str
    proposed_base_salary: Optional[float]
    proposed_total_compensation: Optional[float]
    negotiation_status: str
    initiated_at: datetime
    responded_at: Optional[datetime]
    reason: Optional[str]
    
    class Config:
        from_attributes = True


# ==================== BGV Schemas ====================

class BackgroundCheckItemCreate(BaseModel):
    item_type: str = Field(..., description="Type of background check")
    item_name: str = Field(..., description="Name of the check item")
    description: Optional[str] = Field(None, description="Item description")
    provider: Optional[str] = Field(None, description="External provider if applicable")
    documents_required: bool = Field(default=False, description="Whether documents are required")

class BackgroundVerificationCreate(BaseModel):
    candidate_id: uuid.UUID = Field(..., description="Candidate ID")
    offer_id: uuid.UUID = Field(..., description="Offer ID")
    verification_provider: Optional[str] = Field(None, description="External provider")
    priority: str = Field(default="Normal", description="Verification priority")
    check_items: List[BackgroundCheckItemCreate] = Field(..., description="Background check items")

class BackgroundVerificationResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    candidate_id: uuid.UUID
    offer_id: uuid.UUID
    verification_provider: Optional[str]
    status: str
    initiated_at: datetime
    completed_at: Optional[datetime]
    initiated_by: uuid.UUID
    overall_result: Optional[str]
    priority: str
    case_reference: Optional[str]
    
    class Config:
        from_attributes = True


class BackgroundCheckItemResponse(BaseModel):
    id: uuid.UUID
    bg_verification_id: uuid.UUID
    item_type: str
    item_name: str
    description: Optional[str]
    status: str
    provider: Optional[str]
    initiated_at: datetime
    completed_at: Optional[datetime]
    result: Optional[str]
    risk_level: Optional[str]
    documents_required: bool
    documents_received: bool
    
    class Config:
        from_attributes = True


# ==================== Onboarding Schemas ====================

class OnboardingTaskCreate(BaseModel):
    task_name: str = Field(..., description="Task name")
    description: Optional[str] = Field(None, description="Task description")
    task_type: str = Field(..., description="Task type")
    assignee_role: str = Field(..., description="Role responsible for task")
    department_id: Optional[uuid.UUID] = Field(None, description="Department ID")
    priority: str = Field(default="Normal", description="Task priority")
    sequence_order: int = Field(default=0, description="Task order")
    due_days_after_joining: int = Field(default=1, description="Days after joining")
    is_required: bool = Field(default=True, description="Whether task is required")
    dependencies: Optional[Dict[str, Any]] = Field(None, description="Task dependencies")

class OnboardingPlanCreate(BaseModel):
    plan_name: str = Field(..., description="Plan name")
    description: Optional[str] = Field(None, description="Plan description")
    job_category: Optional[str] = Field(None, description="Job category")
    department_id: Optional[uuid.UUID] = Field(None, description="Department ID")
    duration_weeks: int = Field(default=4, description="Duration in weeks")
    is_default: bool = Field(default=False, description="Whether this is default plan")
    tasks: List[OnboardingTaskCreate] = Field(..., description="Onboarding tasks")

class OnboardingPlanResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    plan_name: str
    description: Optional[str]
    job_category: Optional[str]
    department_id: Optional[uuid.UUID]
    duration_weeks: int
    is_default: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class OnboardingTaskResponse(BaseModel):
    id: uuid.UUID
    onboarding_plan_id: uuid.UUID
    task_name: str
    description: Optional[str]
    task_type: str
    assignee_role: str
    department_id: Optional[uuid.UUID]
    priority: str
    sequence_order: int
    due_days_after_joining: int
    is_required: bool
    dependencies: Optional[Dict[str, Any]]
    
    class Config:
        from_attributes = True


class OnboardingChecklistResponse(BaseModel):
    id: uuid.UUID
    candidate_id: uuid.UUID
    onboarding_plan_id: uuid.UUID
    task_count: int
    completed_count: int
    overall_progress: float
    started_at: datetime
    estimated_completion: Optional[date]
    actual_completion: Optional[date]
    status: str
    
    class Config:
        from_attributes = True


# ==================== Employee Conversion Schemas ====================

class EmployeeConversionCreate(BaseModel):
    candidate_id: uuid.UUID = Field(..., description="Candidate ID")
    offer_id: uuid.UUID = Field(..., description="Offer ID")
    employee_user_id: uuid.UUID = Field(..., description="New employee user ID")
    conversion_notes: Optional[str] = Field(None, description="Conversion notes")

class EmployeeConversionResponse(BaseModel):
    id: uuid.UUID
    candidate_id: uuid.UUID
    employee_id: uuid.UUID
    converted_by: uuid.UUID
    converted_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Utility Schemas ====================

class SuccessResponse(BaseModel):
    status: str = Field(default="success", description="Operation status")
    message: str = Field(..., description="Success message")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional data")

class ValidationErrorResponse(BaseModel):
    status: str = Field(default="error", description="Error status")
    message: str = Field(..., description="Error message")
    errors: Optional[List[str]] = Field(None, description="Detailed validation errors")


# ==================== Search and Filter Schemas ====================

class OfferSearchRequest(BaseModel):
    status: Optional[str] = Field(None, description="Filter by status")
    candidate_id: Optional[uuid.UUID] = Field(None, description="Filter by candidate")
    job_id: Optional[uuid.UUID] = Field(None, description="Filter by job")
    date_from: Optional[date] = Field(None, description="Filter offers from this date")
    date_to: Optional[date] = Field(None, description="Filter offers until this date")
    skip: int = Field(default=0, ge=0, description="Number of records to skip")
    limit: int = Field(default=100, ge=1, le=1000, description="Number of records to return")


# ==================== Dashboard Schemas ====================

class OfferDashboardResponse(BaseModel):
    total_offers: int
    pending_approval: int
    approved_offers: int
    sent_offers: int
    accepted_offers: int
    rejected_offers: int
    negotiations_active: int
    bgv_pending: int
    onboarding_active: int
    recent_offers: List[OfferResponse]