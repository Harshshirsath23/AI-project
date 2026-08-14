from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, update, delete
from sqlalchemy.orm import selectinload
import uuid
from datetime import datetime, date

from app.modules.offers.models import (
    OfferTemplate, Offer, OfferVersion, OfferCompensation,
    OfferDocument, OfferAttachment, OfferTerms, OfferApproval,
    OfferApprovalHistory, OfferNegotiation, CompensationRevision,
    BackgroundVerification, BackgroundCheckItem, OnboardingPlan,
    OnboardingTask, OnboardingTaskAssignment, OnboardingChecklist,
    EmployeeConversion, EmployeeConversionLog
)
from app.modules.organizations.models import SalaryBand
from app.modules.offers.enums import OfferStatus, ApprovalStatus, NegotiationStatus, BGVStatus, TaskStatus, OnboardingStatus


class OfferTemplateRepository:
    """Repository for offer template operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_template(
        self, 
        org_id: uuid.UUID, 
        template_data: dict
    ) -> OfferTemplate:
        """Create offer template"""
        template = OfferTemplate(
            organization_id=org_id,
            template_name=template_data["template_name"],
            description=template_data.get("description"),
            job_category=template_data.get("job_category"),
            template_content=template_data.get("template_content"),
            is_default=template_data.get("is_default", False)
        )
        self.db.add(template)
        await self.db.commit()
        return template
    
    async def get_template_by_id(
        self, 
        org_id: uuid.UUID, 
        template_id: uuid.UUID
    ) -> Optional[OfferTemplate]:
        """Get template by ID"""
        query = select(OfferTemplate).where(
            and_(
                OfferTemplate.id == template_id,
                OfferTemplate.organization_id == org_id
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_templates_by_org(
        self, 
        org_id: uuid.UUID, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[OfferTemplate]:
        """Get all templates for organization"""
        query = select(OfferTemplate).where(
            and_(
                OfferTemplate.organization_id == org_id,
                OfferTemplate.is_active == True
            )
        ).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_default_template(
        self, 
        org_id: uuid.UUID
    ) -> Optional[OfferTemplate]:
        """Get default template for organization"""
        query = select(OfferTemplate).where(
            and_(
                OfferTemplate.organization_id == org_id,
                OfferTemplate.is_default == True
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


class OfferRepository:
    """Repository for offer operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_offer(self, offer_data: dict) -> Offer:
        """Create new offer"""
        offer = Offer(
            organization_id=offer_data["organization_id"],
            candidate_application_id=offer_data["candidate_application_id"],
            candidate_id=offer_data["candidate_id"],
            job_id=offer_data["job_id"],
            offered_designation_id=offer_data["offered_designation_id"],
            hiring_plan_id=offer_data.get("hiring_plan_id"),
            offer_template_id=offer_data.get("offer_template_id"),
            issue_date=offer_data["issue_date"],
            expiry_date=offer_data["expiry_date"],
            start_date=offer_data["start_date"],
            status=OfferStatus.DRAFT,
            approval_status=ApprovalStatus.PENDING,
            created_by=offer_data["created_by"]
        )
        self.db.add(offer)
        await self.db.flush()
        return offer
    
    async def get_offer_by_id(
        self, 
        org_id: uuid.UUID, 
        offer_id: uuid.UUID
    ) -> Optional[Offer]:
        """Get offer by ID"""
        query = select(Offer).where(
            and_(
                Offer.id == offer_id,
                Offer.organization_id == org_id
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_offers_by_org(
        self, 
        org_id: uuid.UUID, 
        filters: dict = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Offer]:
        """Get offers with filters"""
        conditions = [Offer.organization_id == org_id]
        
        if filters:
            if filters.get("status"):
                conditions.append(Offer.status == filters["status"])
            if filters.get("candidate_id"):
                conditions.append(Offer.candidate_id == filters["candidate_id"])
            if filters.get("job_id"):
                conditions.append(Offer.job_id == filters["job_id"])
        
        query = select(Offer).where(
            and_(*conditions)
        ).offset(skip).limit(limit).order_by(Offer.created_at.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_offer_status(
        self, 
        offer_id: uuid.UUID, 
        new_status: str
    ) -> None:
        """Update offer status"""
        query = update(Offer).where(
            Offer.id == offer_id
        ).values(status=new_status)
        await self.db.execute(query)
        await self.db.commit()
    
    async def update_offer(self, offer_id: uuid.UUID, update_data: dict) -> None:
        """Update offer"""
        query = update(Offer).where(
            Offer.id == offer_id
        ).values(**update_data)
        await self.db.execute(query)
        await self.db.commit()


class CompensationRepository:
    """Repository for compensation operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_compensation(
        self, 
        offer_id: uuid.UUID, 
        compensation_data: dict
    ) -> OfferCompensation:
        """Create offer compensation"""
        compensation = OfferCompensation(
            offer_id=offer_id,
            currency_id=compensation_data["currency_id"],
            base_salary=compensation_data["base_salary"],
            variable_compensation=compensation_data.get("variable_compensation", 0.0),
            joining_bonus=compensation_data.get("joining_bonus", 0.0),
            bonus_percentage=compensation_data.get("bonus_percentage", 0.0),
            allowances=compensation_data.get("allowances"),
            benefits=compensation_data.get("benefits"),
            total_compensation=compensation_data.get("total_compensation", 0.0),
            pay_frequency=compensation_data.get("pay_frequency", "Monthly"),
            salary_band_id=compensation_data.get("salary_band_id"),
            within_salary_band=compensation_data.get("within_salary_band", True)
        )
        self.db.add(compensation)
        await self.db.commit()
        return compensation
    
    async def get_compensation_by_offer(
        self, 
        offer_id: uuid.UUID
    ) -> Optional[OfferCompensation]:
        """Get compensation by offer ID"""
        query = select(OfferCompensation).where(
            OfferCompensation.offer_id == offer_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_compensation(
        self, 
        offer_id: uuid.UUID, 
        update_data: dict
    ) -> None:
        """Update compensation"""
        query = update(OfferCompensation).where(
            OfferCompensation.offer_id == offer_id
        ).values(**update_data)
        await self.db.execute(query)
        await self.db.commit()


class SalaryBandRepository:
    """Repository for salary band operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_salary_band(
        self, 
        org_id: uuid.UUID, 
        job_id: uuid.UUID,
        designation_id: uuid.UUID
    ) -> Optional[SalaryBand]:
        """Get salary band for job and designation"""
        # Using organizations module's SalaryBand model
        query = select(SalaryBand).where(
            and_(
                SalaryBand.organization_id == org_id,
                SalaryBand.currency_id.isnot(None)  # Filter for valid bands
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


class ApprovalRepository:
    """Repository for approval operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_approval(
        self, 
        approval_data: dict
    ) -> OfferApproval:
        """Create approval request"""
        approval = OfferApproval(
            offer_id=approval_data["offer_id"],
            approver_id=approval_data["approver_id"],
            approver_role=approval_data["approver_role"],
            approval_level=approval_data.get("approval_level", 1),
            status=ApprovalStatus.PENDING,
            comments=approval_data.get("comments"),
            sequence_order=approval_data.get("sequence_order", 0)
        )
        self.db.add(approval)
        await self.db.commit()
        return approval
    
    async def get_approvals_by_offer(
        self, 
        offer_id: uuid.UUID
    ) -> List[OfferApproval]:
        """Get all approvals for offer"""
        query = select(OfferApproval).where(
            OfferApproval.offer_id == offer_id
        ).order_by(OfferApproval.sequence_order)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_approval_status(
        self, 
        approval_id: uuid.UUID, 
        new_status: str,
        comments: Optional[str] = None
    ) -> None:
        """Update approval status"""
        update_data = {"status": new_status}
        if new_status == ApprovalStatus.APPROVED:
            update_data["approved_at"] = datetime.now()
        if comments:
            update_data["comments"] = comments
        
        query = update(OfferApproval).where(
            OfferApproval.id == approval_id
        ).values(**update_data)
        await self.db.execute(query)
        await self.db.commit()


class NegotiationRepository:
    """Repository for negotiation operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_negotiation(
        self, 
        negotiation_data: dict
    ) -> OfferNegotiation:
        """Create negotiation"""
        negotiation = OfferNegotiation(
            offer_id=negotiation_data["offer_id"],
            negotiator_type=negotiation_data["negotiator_type"],
            negotiator_id=negotiation_data.get("negotiator_id"),
            negotiation_round=negotiation_data.get("negotiation_round", 1),
            requested_base_salary=negotiation_data["requested_base_salary"],
            requested_total_compensation=negotiation_data["requested_total_compensation"],
            comments=negotiation_data["comments"],
            reason=negotiation_data.get("reason"),
            negotiation_status=NegotiationStatus.PENDING
        )
        self.db.add(negotiation)
        await self.db.commit()
        return negotiation
    
    async def get_negotiations_by_offer(
        self, 
        offer_id: uuid.UUID
    ) -> List[OfferNegotiation]:
        """Get all negotiations for offer"""
        query = select(OfferNegotiation).where(
            OfferNegotiation.offer_id == offer_id
        ).order_by(OfferNegotiation.initiated_at.desc())
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_negotiation(
        self, 
        negotiation_id: uuid.UUID, 
        update_data: dict
    ) -> None:
        """Update negotiation"""
        query = update(OfferNegotiation).where(
            OfferNegotiation.id == negotiation_id
        ).values(**update_data)
        await self.db.execute(query)
        await self.db.commit()


class BGVRepository:
    """Repository for background verification operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_bgv(
        self, 
        bgv_data: dict
    ) -> BackgroundVerification:
        """Create background verification"""
        bgv = BackgroundVerification(
            organization_id=bgv_data["organization_id"],
            candidate_id=bgv_data["candidate_id"],
            offer_id=bgv_data["offer_id"],
            verification_provider=bgv_data.get("verification_provider"),
            status=BGVStatus.INITIATED,
            initiated_by=bgv_data["initiated_by"],
            priority=bgv_data.get("priority", "Normal")
        )
        self.db.add(bgv)
        await self.db.flush()
        
        # Create check items
        for item_data in bgv_data["check_items"]:
            # Handle both dict and Pydantic models
            if isinstance(item_data, dict):
                item_dict = item_data
            else:
                item_dict = item_data.model_dump()
            
            check_item = BackgroundCheckItem(
                bg_verification_id=bgv.id,
                item_type=item_dict["item_type"],
                item_name=item_dict["item_name"],
                description=item_dict.get("description"),
                provider=item_dict.get("provider"),
                documents_required=item_dict.get("documents_required", False)
            )
            self.db.add(check_item)
        
        await self.db.commit()
        return bgv
    
    async def get_bgv_by_candidate(
        self, 
        org_id: uuid.UUID, 
        candidate_id: uuid.UUID
    ) -> Optional[BackgroundVerification]:
        """Get BGV by candidate"""
        query = select(BackgroundVerification).where(
            and_(
                BackgroundVerification.organization_id == org_id,
                BackgroundVerification.candidate_id == candidate_id
            )
        ).options(selectinload(BackgroundVerification.check_items))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_bgv_status(
        self, 
        bgv_id: uuid.UUID, 
        new_status: str,
        overall_result: Optional[str] = None
    ) -> None:
        """Update BGV status"""
        update_data = {"status": new_status}
        if new_status == BGVStatus.COMPLETED:
            update_data["completed_at"] = datetime.now()
        if overall_result:
            update_data["overall_result"] = overall_result
        
        query = update(BackgroundVerification).where(
            BackgroundVerification.id == bgv_id
        ).values(**update_data)
        await self.db.execute(query)
        await self.db.commit()


class OnboardingRepository:
    """Repository for onboarding operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_onboarding_plan(
        self, 
        org_id: uuid.UUID, 
        plan_data: dict
    ) -> OnboardingPlan:
        """Create onboarding plan"""
        plan = OnboardingPlan(
            organization_id=org_id,
            plan_name=plan_data["plan_name"],
            description=plan_data.get("description"),
            job_category=plan_data.get("job_category"),
            department_id=plan_data.get("department_id"),
            duration_weeks=plan_data["duration_weeks"],
            is_default=plan_data.get("is_default", False)
        )
        self.db.add(plan)
        await self.db.flush()
        
        # Create tasks
        for task_data in plan_data["tasks"]:
            # Handle both dict and Pydantic models
            if isinstance(task_data, dict):
                task_dict = task_data
            else:
                task_dict = task_data.model_dump()
            
            task = OnboardingTask(
                onboarding_plan_id=plan.id,
                task_name=task_dict["task_name"],
                description=task_dict.get("description"),
                task_type=task_dict["task_type"],
                assignee_role=task_dict["assignee_role"],
                department_id=task_dict.get("department_id"),
                priority=task_dict.get("priority", "Normal"),
                sequence_order=task_dict["sequence_order"],
                due_days_after_joining=task_dict["due_days_after_joining"],
                is_required=task_dict.get("is_required", True),
                dependencies=task_dict.get("dependencies")
            )
            self.db.add(task)
        
        await self.db.commit()
        return plan
    
    async def get_plan_by_id(
        self, 
        org_id: uuid.UUID, 
        plan_id: uuid.UUID
    ) -> Optional[OnboardingPlan]:
        """Get plan by ID"""
        query = select(OnboardingPlan).where(
            and_(
                OnboardingPlan.id == plan_id,
                OnboardingPlan.organization_id == org_id
            )
        ).options(selectinload(OnboardingPlan.tasks))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_default_plan(
        self, 
        org_id: uuid.UUID
    ) -> Optional[OnboardingPlan]:
        """Get default onboarding plan"""
        query = select(OnboardingPlan).where(
            and_(
                OnboardingPlan.organization_id == org_id,
                OnboardingPlan.is_default == True
            )
        ).options(selectinload(OnboardingPlan.tasks))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def create_onboarding_checklist(
        self, 
        candidate_id: uuid.UUID, 
        plan_id: uuid.UUID
    ) -> OnboardingChecklist:
        """Create onboarding checklist for candidate"""
        checklist = OnboardingChecklist(
            candidate_id=candidate_id,
            onboarding_plan_id=plan_id,
            task_count=0,
            completed_count=0,
            overall_progress=0.0,
            status="Not Started"
        )
        self.db.add(checklist)
        await self.db.commit()
        return checklist
    
    async def create_task_assignment(
        self, 
        assignment_data: dict
    ) -> OnboardingTaskAssignment:
        """Create task assignment"""
        assignment = OnboardingTaskAssignment(
            candidate_id=assignment_data["candidate_id"],
            onboarding_task_id=assignment_data["onboarding_task_id"],
            owner_id=assignment_data["owner_id"],
            due_date=assignment_data.get("due_date"),
            status=TaskStatus.PENDING
        )
        self.db.add(assignment)
        await self.db.commit()
        return assignment
    
    async def update_task_status(
        self, 
        assignment_id: uuid.UUID, 
        new_status: str
    ) -> None:
        """Update task status"""
        update_data = {"status": new_status}
        if new_status == TaskStatus.COMPLETED:
            update_data["completed_at"] = datetime.now()
        
        query = update(OnboardingTaskAssignment).where(
            OnboardingTaskAssignment.id == assignment_id
        ).values(**update_data)
        await self.db.execute(query)
        await self.db.commit()
    
    async def update_checklist_progress(
        self, 
        checklist_id: uuid.UUID, 
        completed_count: int,
        total_count: int
    ) -> None:
        """Update checklist progress"""
        progress = (completed_count / total_count * 100) if total_count > 0 else 0.0
        
        query = update(OnboardingChecklist).where(
            OnboardingChecklist.id == checklist_id
        ).values(
            completed_count=completed_count,
            overall_progress=progress
        )
        await self.db.execute(query)
        await self.db.commit()
    
    async def get_onboarding_checklist(
        self, 
        candidate_id: uuid.UUID
    ) -> Optional[OnboardingChecklist]:
        """Get onboarding checklist by candidate ID"""
        query = select(OnboardingChecklist).where(
            OnboardingChecklist.candidate_id == candidate_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


class EmployeeConversionRepository:
    """Repository for employee conversion operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_conversion(
        self, 
        conversion_data: dict
    ) -> EmployeeConversion:
        """Create employee conversion"""
        conversion = EmployeeConversion(
            candidate_id=conversion_data["candidate_id"],
            employee_id=conversion_data["employee_user_id"]
        )
        self.db.add(conversion)
        await self.db.commit()
        return conversion
    
    async def get_conversion_by_candidate(
        self, 
        candidate_id: uuid.UUID
    ) -> Optional[EmployeeConversion]:
        """Get conversion by candidate ID"""
        query = select(EmployeeConversion).where(
            EmployeeConversion.candidate_id == candidate_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()