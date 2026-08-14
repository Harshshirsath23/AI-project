from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid

from app.database.session import get_async_db
from app.modules.auth.dependencies import (
    get_current_organization, get_current_user, require_permission
)
from app.modules.interviews.schemas import (
    InterviewTemplateCreate, InterviewTemplateResponse,
    InterviewCreate, InterviewUpdate, InterviewResponse,
    InterviewRescheduleRequest, InterviewCancelRequest,
    InterviewPanelCreate, InterviewPanelResponse,
    FeedbackCreate, FeedbackResponse,
    DecisionCreate, DecisionResponse,
    AssessmentTemplateCreate, AssessmentCreate, AssessmentResponse,
    EvaluationCriterionCreate, EvaluationCriterionResponse,
    InterviewSearchRequest, SuccessResponse
)
from app.modules.interviews.service import (
    InterviewTemplateService, InterviewService, PanelService,
    FeedbackService, ScorecardService, DecisionService,
    AssessmentService, EvaluationCriterionService
)

router = APIRouter(prefix="/interviews", tags=["Interview & Assessment Management"])

# ==================== Template Endpoints ====================

@router.post("/templates", summary="Create Interview Template", dependencies=[Depends(require_permission("interview_template:manage"))])
async def create_interview_template(
    template_data: InterviewTemplateCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new interview template with rounds and criteria"""
    service = InterviewTemplateService(db)
    return await service.create_template(org_id, template_data)

@router.get("/templates", response_model=List[InterviewTemplateResponse], summary="List Interview Templates", dependencies=[Depends(require_permission("interview:read"))])
async def get_interview_templates(
    skip: int = 0,
    limit: int = 100,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get all interview templates for the organization"""
    service = InterviewTemplateService(db)
    return await service.get_templates(org_id, skip, limit)

@router.get("/templates/default", response_model=InterviewTemplateResponse, summary="Get Default Template", dependencies=[Depends(require_permission("interview:read"))])
async def get_default_template(
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get the default interview template for the organization"""
    service = InterviewTemplateService(db)
    template = await service.get_default_template(org_id)
    if not template:
        raise HTTPException(status_code=404, detail="No default template found")
    return template

@router.get("/templates/{template_id}", response_model=InterviewTemplateResponse, summary="Get Template by ID", dependencies=[Depends(require_permission("interview:read"))])
async def get_interview_template(
    template_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get a specific interview template by ID"""
    service = InterviewTemplateService(db)
    return await service.get_template(org_id, template_id)

@router.delete("/templates/{template_id}", summary="Delete Template", dependencies=[Depends(require_permission("interview_template:manage"))])
async def delete_interview_template(
    template_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Delete an interview template"""
    service = InterviewTemplateService(db)
    return await service.delete_template(org_id, template_id)

# ==================== Interview Endpoints ====================

@router.post("/", summary="Create Interview", dependencies=[Depends(require_permission("interview:create"))])
async def create_interview(
    interview_data: InterviewCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new interview and schedule it"""
    service = InterviewService(db)
    return await service.create_interview(org_id, interview_data)

@router.get("/", response_model=List[InterviewResponse], summary="List Interviews", dependencies=[Depends(require_permission("interview:read"))])
async def get_interviews(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    job_id: Optional[uuid.UUID] = None,
    candidate_id: Optional[uuid.UUID] = None,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get interviews with optional filters"""
    service = InterviewService(db)
    filters = {}
    if status:
        filters["status"] = status
    if job_id:
        filters["job_id"] = job_id
    if candidate_id:
        filters["candidate_id"] = candidate_id
    return await service.get_interviews(org_id, filters, skip, limit)

@router.get("/{interview_id}", response_model=InterviewResponse, summary="Get Interview by ID", dependencies=[Depends(require_permission("interview:read"))])
async def get_interview(
    interview_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get a specific interview by ID"""
    service = InterviewService(db)
    return await service.get_interview(org_id, interview_id)

@router.put("/{interview_id}", summary="Update Interview", dependencies=[Depends(require_permission("interview:update"))])
async def update_interview(
    interview_id: uuid.UUID,
    update_data: InterviewUpdate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Update interview details"""
    service = InterviewService(db)
    return await service.update_interview(org_id, interview_id, update_data)

@router.post("/{interview_id}/reschedule", summary="Reschedule Interview", dependencies=[Depends(require_permission("interview:schedule"))])
async def reschedule_interview(
    interview_id: uuid.UUID,
    reschedule_data: InterviewRescheduleRequest,
    org_id: uuid.UUID = Depends(get_current_organization),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Reschedule an interview to a new time"""
    service = InterviewService(db)
    return await service.reschedule_interview(
        org_id, interview_id, reschedule_data, current_user["id"]
    )

@router.post("/{interview_id}/cancel", summary="Cancel Interview", dependencies=[Depends(require_permission("interview:cancel"))])
async def cancel_interview(
    interview_id: uuid.UUID,
    cancel_data: InterviewCancelRequest,
    org_id: uuid.UUID = Depends(get_current_organization),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Cancel an interview"""
    service = InterviewService(db)
    return await service.cancel_interview(
        org_id, interview_id, cancel_data, current_user["id"]
    )

@router.post("/{interview_id}/start", summary="Start Interview", dependencies=[Depends(require_permission("interview:update"))])
async def start_interview(
    interview_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Mark interview as started"""
    service = InterviewService(db)
    return await service.start_interview(org_id, interview_id)

@router.post("/{interview_id}/complete", summary="Complete Interview", dependencies=[Depends(require_permission("interview:update"))])
async def complete_interview(
    interview_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Mark interview as completed"""
    service = InterviewService(db)
    return await service.complete_interview(org_id, interview_id)

# ==================== Panel Endpoints ====================

@router.post("/{interview_id}/panels", summary="Create Interview Panel", dependencies=[Depends(require_permission("interview:assign"))])
async def create_interview_panel(
    interview_id: uuid.UUID,
    panel_data: InterviewPanelCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Create an interview panel with members"""
    service = PanelService(db)
    return await service.create_panel(interview_id, panel_data)

@router.get("/{interview_id}/panels", response_model=InterviewPanelResponse, summary="Get Interview Panel", dependencies=[Depends(require_permission("interview:read"))])
async def get_interview_panel(
    interview_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get the panel for an interview"""
    service = PanelService(db)
    panel = await service.get_panel(interview_id)
    if not panel:
        raise HTTPException(status_code=404, detail="Panel not found")
    return panel

@router.post("/panels/{panel_id}/members", summary="Add Panel Member", dependencies=[Depends(require_permission("interview:assign"))])
async def add_panel_member(
    panel_id: uuid.UUID,
    member_data: dict,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Add a member to an interview panel"""
    service = PanelService(db)
    return await service.add_panel_member(panel_id, member_data)

# ==================== Feedback Endpoints ====================

@router.post("/{interview_id}/feedback", summary="Submit Interview Feedback", dependencies=[Depends(require_permission("interview:feedback"))])
async def submit_feedback(
    interview_id: uuid.UUID,
    feedback_data: FeedbackCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Submit structured feedback for an interview"""
    service = FeedbackService(db)
    return await service.submit_feedback(org_id, interview_id, feedback_data)

@router.get("/{interview_id}/feedback", response_model=List[FeedbackResponse], summary="Get Interview Feedback", dependencies=[Depends(require_permission("interview:read"))])
async def get_interview_feedback(
    interview_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get all feedback for an interview"""
    service = FeedbackService(db)
    return await service.get_feedback(interview_id)

# ==================== Scorecard Endpoints ====================

@router.post("/{interview_id}/scorecard", summary="Calculate Scorecard", dependencies=[Depends(require_permission("interview:evaluate"))])
async def calculate_scorecard(
    interview_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Calculate interview scorecard from all feedback"""
    service = ScorecardService(db)
    return await service.calculate_scorecard(org_id, interview_id)

@router.get("/{interview_id}/scorecard", summary="Get Scorecard", dependencies=[Depends(require_permission("interview:read"))])
async def get_scorecard(
    interview_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get the scorecard for an interview"""
    service = ScorecardService(db)
    scorecard = await service.get_scorecard(interview_id)
    if not scorecard:
        raise HTTPException(status_code=404, detail="Scorecard not found")
    return scorecard

# ==================== Decision Endpoints ====================

@router.post("/{interview_id}/decision", summary="Make Hiring Decision", dependencies=[Depends(require_permission("interview:decision"))])
async def make_decision(
    interview_id: uuid.UUID,
    decision_data: DecisionCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Make final hiring decision for the interview"""
    service = DecisionService(db)
    return await service.make_decision(
        org_id, interview_id, decision_data, current_user["id"]
    )

@router.get("/{interview_id}/decision", response_model=DecisionResponse, summary="Get Decision", dependencies=[Depends(require_permission("interview:read"))])
async def get_decision(
    interview_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get the decision for an interview"""
    service = DecisionService(db)
    decision = await service.get_decision(interview_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    return decision

# ==================== Assessment Endpoints ====================

@router.post("/assessments/templates", summary="Create Assessment Template", dependencies=[Depends(require_permission("interview_template:manage"))])
async def create_assessment_template(
    template_data: AssessmentTemplateCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new assessment template"""
    service = AssessmentService(db)
    return await service.create_assessment_template(org_id, template_data)

@router.post("/assessments", summary="Create Assessment", dependencies=[Depends(require_permission("interview:create"))])
async def create_assessment(
    assessment_data: AssessmentCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new assessment"""
    service = AssessmentService(db)
    return await service.create_assessment(org_id, assessment_data)

@router.get("/assessments", response_model=List[AssessmentResponse], summary="List Assessments", dependencies=[Depends(require_permission("interview:read"))])
async def get_assessments(
    skip: int = 0,
    limit: int = 100,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get all assessments for the organization"""
    service = AssessmentService(db)
    assessments = await service.assessment_repo.get_assessments_by_org(org_id, skip, limit)
    return assessments

# ==================== Evaluation Criterion Endpoints ====================

@router.post("/criteria", summary="Create Evaluation Criterion", dependencies=[Depends(require_permission("interview_template:manage"))])
async def create_evaluation_criterion(
    criterion_data: EvaluationCriterionCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new evaluation criterion"""
    service = EvaluationCriterionService(db)
    return await service.create_criterion(org_id, criterion_data)

@router.get("/criteria", response_model=List[EvaluationCriterionResponse], summary="List Evaluation Criteria", dependencies=[Depends(require_permission("interview:read"))])
async def get_evaluation_criteria(
    category: Optional[str] = None,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get evaluation criteria for the organization"""
    service = EvaluationCriterionService(db)
    return await service.get_criteria(org_id, category)

# ==================== Search and Filter Endpoints ====================

@router.post("/search", response_model=List[InterviewResponse], summary="Search Interviews", dependencies=[Depends(require_permission("interview:read"))])
async def search_interviews(
    search_request: InterviewSearchRequest,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Search interviews with advanced filters"""
    service = InterviewService(db)
    filters = search_request.dict(exclude_unset=True)
    return await service.get_interviews(org_id, filters, search_request.skip, search_request.limit)

# ==================== Utility Endpoints ====================

@router.get("/dashboard/summary", summary="Interview Dashboard Summary", dependencies=[Depends(require_permission("interview:read"))])
async def get_interview_dashboard(
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get interview dashboard summary with key metrics"""
    service = InterviewService(db)
    
    # Get upcoming interviews
    upcoming = await service.interview_repo.get_upcoming_interviews(org_id, hours=24)
    
    # Get interview counts by status
    # This would need additional repository methods
    
    return {
        "upcoming_interviews_count": len(upcoming),
        "upcoming_interviews": upcoming,
        "status": "success"
    }