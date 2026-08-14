from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from datetime import datetime, date, timedelta

from app.modules.offers.models import (
    Offer, OfferTemplate, OfferCompensation, OfferTerms, OfferApproval,
    OfferNegotiation, BackgroundVerification, OnboardingPlan,
    OnboardingChecklist, EmployeeConversion
)
from app.modules.organizations.models import SalaryBand
from app.modules.offers.schemas import (
    OfferCreate, OfferUpdate, OfferCompensationCreate, OfferTermsCreate,
    OfferTemplateCreate, SalaryBandResponse, OfferCompensationResponse,
    OfferApprovalRequest, OfferApprovalAction, NegotiationRequest,
    BackgroundVerificationCreate, OnboardingPlanCreate, EmployeeConversionCreate
)
from app.modules.offers.enums import (
    OfferStatus, ApprovalStatus, EmploymentType, WorkMode,
    PayFrequency, NegotiationStatus, BGVStatus, OnboardingStatus,
    ApproverRole, TaskStatus
)
from app.modules.offers.validators import (
    OfferValidator, ApprovalValidator, NegotiationValidator,
    BGVValidator, OnboardingValidator, EmployeeConversionValidator
)
from app.modules.offers.exceptions import (
    OfferNotFoundException, InvalidOfferStatusException, CompensationValidationException,
    SalaryBandViolationException, OfferApprovalException, OfferAlreadyApprovedException,
    NegotiationException, BGVInitiationException, OnboardingException, EmployeeConversionException
)
from app.modules.offers.repository import (
    OfferTemplateRepository, OfferRepository, CompensationRepository,
    SalaryBandRepository, ApprovalRepository, NegotiationRepository,
    BGVRepository, OnboardingRepository, EmployeeConversionRepository
)


class OfferTemplateService:
    """Service for offer template management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.template_repo = OfferTemplateRepository(db)
    
    async def create_template(
        self, 
        org_id: uuid.UUID, 
        template_data: OfferTemplateCreate
    ) -> Dict[str, Any]:
        """Create offer template"""
        template_dict = template_data.model_dump()
        template = await self.template_repo.create_template(org_id, template_dict)
        
        return {
            "status": "success",
            "template_id": str(template.id),
            "message": "Offer template created successfully"
        }
    
    async def get_template(
        self, 
        org_id: uuid.UUID, 
        template_id: uuid.UUID
    ) -> Optional[OfferTemplate]:
        """Get template by ID"""
        template = await self.template_repo.get_template_by_id(org_id, template_id)
        if not template:
            raise OfferNotFoundException(str(template_id))
        return template
    
    async def get_templates(
        self, 
        org_id: uuid.UUID, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[OfferTemplate]:
        """Get all templates for organization"""
        return await self.template_repo.get_templates_by_org(org_id, skip, limit)
    
    async def get_default_template(
        self, 
        org_id: uuid.UUID
    ) -> Optional[OfferTemplate]:
        """Get default template for organization"""
        return await self.template_repo.get_default_template(org_id)


class OfferService:
    """Service for offer management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.offer_repo = OfferRepository(db)
        self.compensation_repo = CompensationRepository(db)
        self.salary_band_repo = SalaryBandRepository(db)
        self.approval_repo = ApprovalRepository(db)
        self.workflow_hooks = OfferWorkflowHooks(db)
    
    async def create_offer(
        self, 
        org_id: uuid.UUID, 
        offer_data: OfferCreate,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Create new offer"""
        # Validate dates
        OfferValidator.validate_offer_dates(
            offer_data.issue_date,
            offer_data.expiry_date,
            offer_data.start_date
        )
        
        # Validate compensation structure
        OfferValidator.validate_compensation_structure(offer_data.compensation.model_dump())
        
        # Validate salary band compliance
        salary_band = await self.salary_band_repo.get_salary_band(
            org_id, 
            offer_data.job_id, 
            offer_data.offered_designation_id
        )
        
        if salary_band:
            total_comp = (
                offer_data.compensation.base_salary + 
                offer_data.compensation.variable_compensation +
                offer_data.compensation.joining_bonus
            )
            # Use organizations module's field names: minimum_salary, maximum_salary
            OfferValidator.validate_salary_band_compliance(
                total_comp,
                salary_band.minimum_salary,
                salary_band.maximum_salary,
                requires_approval=True
            )
        
        # Create offer
        offer_dict = offer_data.model_dump()
        offer_dict["organization_id"] = org_id
        offer_dict["created_by"] = user_id
        offer = await self.offer_repo.create_offer(offer_dict)
        
        # Create compensation
        compensation_dict = offer_data.compensation.model_dump()
        compensation_dict["total_compensation"] = (
            compensation_dict["base_salary"] + 
            compensation_dict["variable_compensation"] +
            compensation_dict["joining_bonus"]
        )
        if salary_band:
            compensation_dict["salary_band_id"] = salary_band.id
            compensation_dict["within_salary_band"] = True
        
        await self.compensation_repo.create_compensation(offer.id, compensation_dict)
        
        # Create terms
        terms_dict = offer_data.terms.model_dump()
        terms = OfferTerms(
            offer_id=offer.id,
            **terms_dict
        )
        self.db.add(terms)
        await self.db.commit()
        
        # Trigger workflow hook
        await self.workflow_hooks.on_offer_created(offer.id, org_id, user_id)
        
        return {
            "status": "success",
            "offer_id": str(offer.id),
            "message": "Offer created successfully"
        }
    
    async def get_offer(
        self, 
        org_id: uuid.UUID, 
        offer_id: uuid.UUID
    ) -> Optional[Offer]:
        """Get offer by ID"""
        offer = await self.offer_repo.get_offer_by_id(org_id, offer_id)
        if not offer:
            raise OfferNotFoundException(str(offer_id))
        return offer
    
    async def get_offers(
        self, 
        org_id: uuid.UUID, 
        filters: Dict[str, Any] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Offer]:
        """Get offers with filters"""
        return await self.offer_repo.get_offers_by_org(org_id, filters, skip, limit)
    
    async def submit_for_approval(
        self, 
        org_id: uuid.UUID, 
        offer_id: uuid.UUID,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Submit offer for approval"""
        offer = await self.offer_repo.get_offer_by_id(org_id, offer_id)
        if not offer:
            raise OfferNotFoundException(str(offer_id))
        
        OfferValidator.validate_status_transition(offer.status, OfferStatus.PENDING_APPROVAL)
        
        await self.offer_repo.update_offer_status(offer_id, OfferStatus.PENDING_APPROVAL)
        
        # Trigger workflow hook
        await self.workflow_hooks.on_offer_submitted_for_approval(offer_id, org_id, user_id)
        
        return {
            "status": "success",
            "message": "Offer submitted for approval"
        }
    
    async def approve_offer(
        self, 
        org_id: uuid.UUID, 
        offer_id: uuid.UUID,
        approver_data: OfferApprovalAction,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Approve offer"""
        offer = await self.offer_repo.get_offer_by_id(org_id, offer_id)
        if not offer:
            raise OfferNotFoundException(str(offer_id))
        
        ApprovalValidator.validate_approval_eligibility(offer.status, offer.approval_status)
        
        # Update offer approval status
        await self.offer_repo.update_offer(offer_id, {
            "approval_status": ApprovalStatus.APPROVED,
            "approved_by": user_id,
            "approved_at": datetime.now()
        })
        
        # Update offer status
        await self.offer_repo.update_offer_status(offer_id, OfferStatus.APPROVED)
        
        # Trigger workflow hook
        await self.workflow_hooks.on_offer_approved(offer_id, org_id, user_id)
        
        return {
            "status": "success",
            "message": "Offer approved successfully"
        }
    
    async def send_offer(
        self, 
        org_id: uuid.UUID, 
        offer_id: uuid.UUID,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Send offer to candidate"""
        offer = await self.offer_repo.get_offer_by_id(org_id, offer_id)
        if not offer:
            raise OfferNotFoundException(str(offer_id))
        
        if offer.status != OfferStatus.APPROVED:
            raise InvalidOfferStatusException(offer.status, OfferStatus.APPROVED)
        
        await self.offer_repo.update_offer(offer_id, {
            "status": OfferStatus.SENT,
            "sent_at": datetime.now()
        })
        
        # Trigger workflow hook
        await self.workflow_hooks.on_offer_sent(offer_id, org_id, user_id)
        
        return {
            "status": "success",
            "message": "Offer sent to candidate"
        }


class SalaryBandService:
    """Service for salary band management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.salary_band_repo = SalaryBandRepository(db)
    
    async def get_salary_band(
        self, 
        org_id: uuid.UUID, 
        job_id: uuid.UUID,
        designation_id: uuid.UUID
    ) -> Optional[SalaryBand]:
        """Get salary band for job and designation"""
        return await self.salary_band_repo.get_salary_band(org_id, job_id, designation_id)


class NegotiationService:
    """Service for negotiation management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.offer_repo = OfferRepository(db)
        self.negotiation_repo = NegotiationRepository(db)
        self.compensation_repo = CompensationRepository(db)
    
    async def initiate_negotiation(
        self, 
        org_id: uuid.UUID, 
        offer_id: uuid.UUID,
        negotiation_data: NegotiationRequest
    ) -> Dict[str, Any]:
        """Initiate negotiation"""
        offer = await self.offer_repo.get_offer_by_id(org_id, offer_id)
        if not offer:
            raise OfferNotFoundException(str(offer_id))
        
        NegotiationValidator.validate_negotiation_eligibility(offer.status)
        
        # Get current compensation
        current_comp = await self.compensation_repo.get_compensation_by_offer(offer_id)
        current_total = current_comp.total_compensation if current_comp else 0
        
        NegotiationValidator.validate_compensation_request(
            negotiation_data.requested_total_compensation,
            current_total
        )
        
        # Create negotiation
        negotiation_dict = negotiation_data.model_dump()
        negotiation_dict["offer_id"] = offer_id
        negotiation = await self.negotiation_repo.create_negotiation(negotiation_dict)
        
        # Update offer status
        await self.offer_repo.update_offer_status(offer_id, OfferStatus.NEGOTIATING)
        
        return {
            "status": "success",
            "negotiation_id": str(negotiation.id),
            "message": "Negotiation initiated successfully"
        }


class BGVService:
    """Service for background verification management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.bgv_repo = BGVRepository(db)
        self.offer_repo = OfferRepository(db)
        self.workflow_hooks = OfferWorkflowHooks(db)
    
    async def initiate_bgv(
        self, 
        org_id: uuid.UUID, 
        bgv_data: BackgroundVerificationCreate,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Initiate background verification"""
        offer = await self.offer_repo.get_offer_by_id(org_id, bgv_data.offer_id)
        if not offer:
            raise OfferNotFoundException(str(bgv_data.offer_id))
        
        BGVValidator.validate_bgv_eligibility(offer.status)
        
        BGVValidator.validate_check_items(bgv_data.check_items)
        
        bgv_dict = bgv_data.model_dump()
        bgv_dict["organization_id"] = org_id
        bgv_dict["initiated_by"] = user_id
        bgv = await self.bgv_repo.create_bgv(bgv_dict)
        
        # Trigger workflow hook
        await self.workflow_hooks.on_bgv_initiated(bgv.id, org_id, user_id)
        
        return {
            "status": "success",
            "bgv_id": str(bgv.id),
            "message": "Background verification initiated"
        }
    
    async def complete_bgv(
        self, 
        org_id: uuid.UUID, 
        bgv_id: uuid.UUID,
        overall_result: str,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Complete background verification"""
        await self.bgv_repo.update_bgv_status(bgv_id, BGVStatus.COMPLETED, overall_result)
        
        # Trigger workflow hook
        await self.workflow_hooks.on_bgv_completed(bgv_id, org_id, user_id)
        
        return {
            "status": "success",
            "message": "Background verification completed"
        }


class OnboardingService:
    """Service for onboarding management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.onboarding_repo = OnboardingRepository(db)
        self.offer_repo = OfferRepository(db)
        self.bgv_repo = BGVRepository(db)
        self.workflow_hooks = OfferWorkflowHooks(db)
    
    async def create_onboarding_plan(
        self, 
        org_id: uuid.UUID, 
        plan_data: OnboardingPlanCreate
    ) -> Dict[str, Any]:
        """Create onboarding plan"""
        OnboardingValidator.validate_onboarding_plan(plan_data.tasks)
        
        plan_dict = plan_data.model_dump()
        plan = await self.onboarding_repo.create_onboarding_plan(org_id, plan_dict)
        
        return {
            "status": "success",
            "plan_id": str(plan.id),
            "message": "Onboarding plan created successfully"
        }
    
    async def start_onboarding(
        self, 
        org_id: uuid.UUID, 
        candidate_id: uuid.UUID,
        offer_id: uuid.UUID,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Start onboarding for candidate"""
        offer = await self.offer_repo.get_offer_by_id(org_id, offer_id)
        if not offer:
            raise OfferNotFoundException(str(offer_id))
        
        bgv = await self.bgv_repo.get_bgv_by_candidate(org_id, candidate_id)
        bgv_status = bgv.status if bgv else None
        
        OnboardingValidator.validate_onboarding_eligibility(offer.status, bgv_status)
        
        # Get default plan or assign plan based on job
        plan = await self.onboarding_repo.get_default_plan(org_id)
        if not plan:
            raise OnboardingException("No default onboarding plan found")
        
        # Create checklist
        checklist = await self.onboarding_repo.create_onboarding_checklist(candidate_id, plan.id)
        
        # Update checklist status
        checklist.status = OnboardingStatus.IN_PROGRESS
        checklist.started_at = datetime.now()
        await self.db.commit()
        
        # Create task assignments
        for task in plan.tasks:
            owner_id = user_id  # Placeholder - would get actual assignee
            due_date = date.today() + timedelta(days=task.due_days_after_joining)
            
            await self.onboarding_repo.create_task_assignment({
                "candidate_id": candidate_id,
                "onboarding_task_id": task.id,
                "owner_id": owner_id,
                "due_date": due_date
            })
        
        # Trigger workflow hook
        await self.workflow_hooks.on_onboarding_started(candidate_id, org_id, plan.id, user_id)
        
        return {
            "status": "success",
            "checklist_id": str(checklist.id),
            "message": "Onboarding started successfully"
        }


class EmployeeConversionService:
    """Service for employee conversion management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.conversion_repo = EmployeeConversionRepository(db)
        self.offer_repo = OfferRepository(db)
        self.bgv_repo = BGVRepository(db)
        self.onboarding_repo = OnboardingRepository(db)
        self.workflow_hooks = OfferWorkflowHooks(db)
    
    async def convert_to_employee(
        self, 
        org_id: uuid.UUID, 
        conversion_data: EmployeeConversionCreate,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Convert candidate to employee"""
        offer = await self.offer_repo.get_offer_by_id(org_id, conversion_data.offer_id)
        if not offer:
            raise OfferNotFoundException(str(conversion_data.offer_id))
        
        bgv = await self.bgv_repo.get_bgv_by_candidate(org_id, conversion_data.candidate_id)
        bgv_status = bgv.status if bgv else None
        
        checklist = await self.onboarding_repo.get_onboarding_checklist(conversion_data.candidate_id)
        onboarding_status = checklist.status if checklist else None
        
        EmployeeConversionValidator.validate_conversion_eligibility(
            offer.status, bgv_status, onboarding_status
        )
        
        # Check if employee already exists
        existing_conversion = await self.conversion_repo.get_conversion_by_candidate(
            conversion_data.candidate_id
        )
        EmployeeConversionValidator.validate_employee_not_exists(
            str(conversion_data.candidate_id),
            str(existing_conversion.employee_id) if existing_conversion else None
        )
        
        # Create conversion
        conversion_dict = conversion_data.model_dump()
        conversion = await self.conversion_repo.create_conversion(conversion_dict)
        
        # Update offer status
        await self.offer_repo.update_offer_status(offer.id, OfferStatus.JOINING_CONFIRMED)
        
        # Trigger workflow hook
        await self.workflow_hooks.on_employee_converted(
            conversion_data.candidate_id, 
            conversion_data.employee_user_id, 
            org_id, 
            user_id
        )
        
        return {
            "status": "success",
            "conversion_id": str(conversion.id),
            "employee_id": str(conversion.employee_id),
            "message": "Candidate converted to employee successfully"
        }


class OfferWorkflowHooks:
    """Integration hooks for offer workflow"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.offer_repo = OfferRepository(db)
    
    async def on_offer_created(
        self, 
        offer_id: uuid.UUID, 
        org_id: uuid.UUID,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Hook called when offer is created"""
        return {
            "status": "success",
            "offer_id": str(offer_id),
            "message": "Offer created hook processed"
        }
    
    async def on_offer_submitted_for_approval(
        self, 
        offer_id: uuid.UUID, 
        org_id: uuid.UUID,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Hook called when offer is submitted for approval"""
        return {
            "status": "success",
            "offer_id": str(offer_id),
            "message": "Offer submitted for approval hook processed"
        }
    
    async def on_offer_approved(
        self, 
        offer_id: uuid.UUID, 
        org_id: uuid.UUID,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Hook called when offer is approved"""
        return {
            "status": "success",
            "offer_id": str(offer_id),
            "message": "Offer approved hook processed"
        }
    
    async def on_offer_sent(
        self, 
        offer_id: uuid.UUID, 
        org_id: uuid.UUID,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Hook called when offer is sent"""
        return {
            "status": "success",
            "offer_id": str(offer_id),
            "message": "Offer sent hook processed"
        }
    
    async def on_bgv_initiated(
        self, 
        bgv_id: uuid.UUID, 
        org_id: uuid.UUID,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Hook called when BGV is initiated"""
        return {
            "status": "success",
            "bgv_id": str(bgv_id),
            "message": "BGV initiated hook processed"
        }
    
    async def on_bgv_completed(
        self, 
        bgv_id: uuid.UUID, 
        org_id: uuid.UUID,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Hook called when BGV is completed"""
        return {
            "status": "success",
            "bgv_id": str(bgv_id),
            "message": "BGV completed hook processed"
        }
    
    async def on_onboarding_started(
        self, 
        candidate_id: uuid.UUID, 
        org_id: uuid.UUID,
        plan_id: uuid.UUID,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Hook called when onboarding starts"""
        return {
            "status": "success",
            "candidate_id": str(candidate_id),
            "plan_id": str(plan_id),
            "message": "Onboarding started hook processed"
        }
    
    async def on_employee_converted(
        self, 
        candidate_id: uuid.UUID, 
        employee_id: uuid.UUID,
        org_id: uuid.UUID,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Hook called when candidate is converted to employee"""
        return {
            "status": "success",
            "candidate_id": str(candidate_id),
            "employee_id": str(employee_id),
            "message": "Employee conversion hook processed"
        }