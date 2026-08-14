from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid

from app.database.session import get_async_db
from app.modules.auth.dependencies import (
    get_current_organization, get_current_user, require_permission
)
from app.modules.offers.schemas import (
    OfferTemplateCreate, OfferTemplateResponse,
    OfferCreate, OfferUpdate, OfferResponse,
    OfferCompensationCreate, OfferCompensationResponse,
    OfferApprovalAction, NegotiationRequest, NegotiationResponse,
    BackgroundVerificationCreate, BackgroundVerificationResponse,
    OnboardingPlanCreate, OnboardingPlanResponse,
    EmployeeConversionCreate, EmployeeConversionResponse,
    OfferSearchRequest, SuccessResponse
)
from app.modules.offers.service import (
    OfferTemplateService, OfferService, SalaryBandService,
    NegotiationService, BGVService, OnboardingService,
    EmployeeConversionService
)

router = APIRouter(prefix="/offers", tags=["Offer & Hiring Management"])


# ==================== Template Endpoints ====================

@router.post("/templates", summary="Create Offer Template", dependencies=[Depends(require_permission("offer_template:manage"))])
async def create_offer_template(
    template_data: OfferTemplateCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new offer template"""
    service = OfferTemplateService(db)
    return await service.create_template(org_id, template_data)

@router.get("/templates", response_model=List[OfferTemplateResponse], summary="List Offer Templates", dependencies=[Depends(require_permission("offer:read"))])
async def get_offer_templates(
    skip: int = 0,
    limit: int = 100,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get all offer templates for the organization"""
    service = OfferTemplateService(db)
    return await service.get_templates(org_id, skip, limit)

@router.get("/templates/default", response_model=OfferTemplateResponse, summary="Get Default Template", dependencies=[Depends(require_permission("offer:read"))])
async def get_default_template(
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get the default offer template for the organization"""
    service = OfferTemplateService(db)
    template = await service.get_default_template(org_id)
    if not template:
        raise HTTPException(status_code=404, detail="No default template found")
    return template

@router.get("/templates/{template_id}", response_model=OfferTemplateResponse, summary="Get Template by ID", dependencies=[Depends(require_permission("offer:read"))])
async def get_offer_template(
    template_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get a specific offer template by ID"""
    service = OfferTemplateService(db)
    return await service.get_template(org_id, template_id)


# ==================== Offer Endpoints ====================

@router.post("/", summary="Create Offer", dependencies=[Depends(require_permission("offer:create"))])
async def create_offer(
    offer_data: OfferCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new offer"""
    service = OfferService(db)
    return await service.create_offer(org_id, offer_data, current_user["id"])

@router.get("/", response_model=List[OfferResponse], summary="List Offers", dependencies=[Depends(require_permission("offer:read"))])
async def get_offers(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    candidate_id: Optional[uuid.UUID] = None,
    job_id: Optional[uuid.UUID] = None,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get offers with optional filters"""
    service = OfferService(db)
    filters = {}
    if status:
        filters["status"] = status
    if candidate_id:
        filters["candidate_id"] = candidate_id
    if job_id:
        filters["job_id"] = job_id
    return await service.get_offers(org_id, filters, skip, limit)

@router.get("/{offer_id}", response_model=OfferResponse, summary="Get Offer by ID", dependencies=[Depends(require_permission("offer:read"))])
async def get_offer(
    offer_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get a specific offer by ID"""
    service = OfferService(db)
    return await service.get_offer(org_id, offer_id)

@router.post("/{offer_id}/submit-approval", summary="Submit Offer for Approval", dependencies=[Depends(require_permission("offer:submit"))])
async def submit_offer_for_approval(
    offer_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Submit offer for approval"""
    service = OfferService(db)
    return await service.submit_for_approval(org_id, offer_id, current_user["id"])

@router.post("/{offer_id}/approve", summary="Approve Offer", dependencies=[Depends(require_permission("offer:approve"))])
async def approve_offer(
    offer_id: uuid.UUID,
    approver_data: OfferApprovalAction,
    org_id: uuid.UUID = Depends(get_current_organization),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Approve an offer"""
    service = OfferService(db)
    return await service.approve_offer(org_id, offer_id, approver_data, current_user["id"])

@router.post("/{offer_id}/send", summary="Send Offer to Candidate", dependencies=[Depends(require_permission("offer:send"))])
async def send_offer(
    offer_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Send offer to candidate"""
    service = OfferService(db)
    return await service.send_offer(org_id, offer_id, current_user["id"])


# ==================== Negotiation Endpoints ====================

@router.post("/{offer_id}/negotiations", summary="Initiate Negotiation", dependencies=[Depends(require_permission("offer:negotiate"))])
async def initiate_negotiation(
    offer_id: uuid.UUID,
    negotiation_data: NegotiationRequest,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Initiate offer negotiation"""
    service = NegotiationService(db)
    return await service.initiate_negotiation(org_id, offer_id, negotiation_data)


# ==================== BGV Endpoints ====================

@router.post("/background-verifications", summary="Initiate Background Verification", dependencies=[Depends(require_permission("bgv:create"))])
async def initiate_bgv(
    bgv_data: BackgroundVerificationCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Initiate background verification"""
    service = BGVService(db)
    return await service.initiate_bgv(org_id, bgv_data, current_user["id"])

@router.post("/background-verifications/{bgv_id}/complete", summary="Complete Background Verification", dependencies=[Depends(require_permission("bgv:approve"))])
async def complete_bgv(
    bgv_id: uuid.UUID,
    overall_result: str,
    org_id: uuid.UUID = Depends(get_current_organization),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Complete background verification"""
    service = BGVService(db)
    return await service.complete_bgv(org_id, bgv_id, overall_result, current_user["id"])


# ==================== Onboarding Endpoints ====================

@router.post("/onboarding/plans", summary="Create Onboarding Plan", dependencies=[Depends(require_permission("onboarding:manage"))])
async def create_onboarding_plan(
    plan_data: OnboardingPlanCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new onboarding plan"""
    service = OnboardingService(db)
    return await service.create_onboarding_plan(org_id, plan_data)

@router.post("/onboarding/{candidate_id}/start", summary="Start Onboarding", dependencies=[Depends(require_permission("onboarding:manage"))])
async def start_onboarding(
    candidate_id: uuid.UUID,
    offer_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Start onboarding for a candidate"""
    service = OnboardingService(db)
    return await service.start_onboarding(org_id, candidate_id, offer_id, current_user["id"])


# ==================== Employee Conversion Endpoints ====================

@router.post("/employee-conversions", summary="Convert Candidate to Employee", dependencies=[Depends(require_permission("employee:convert"))])
async def convert_to_employee(
    conversion_data: EmployeeConversionCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Convert candidate to employee"""
    service = EmployeeConversionService(db)
    return await service.convert_to_employee(org_id, conversion_data, current_user["id"])


# ==================== Search Endpoints ====================

@router.post("/search", response_model=List[OfferResponse], summary="Search Offers", dependencies=[Depends(require_permission("offer:read"))])
async def search_offers(
    search_request: OfferSearchRequest,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Search offers with advanced filters"""
    service = OfferService(db)
    filters = search_request.dict(exclude_unset=True)
    return await service.get_offers(org_id, filters, search_request.skip, search_request.limit)