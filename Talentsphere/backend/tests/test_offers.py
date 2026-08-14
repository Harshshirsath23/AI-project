"""
Comprehensive tests for Offer & Hiring Management Module

This test suite covers:
- Offer template validation and CRUD operations
- Offer lifecycle management (create, approve, send, negotiate, accept)
- Compensation validation and salary band compliance
- Approval workflow with HITL architecture
- Negotiation tracking and validation
- Background verification operations
- Onboarding plan and task management
- Employee conversion process
- Workflow integration hooks
- AI hooks (for future LangGraph integration)
"""

import pytest
from datetime import datetime, date, timedelta
from unittest.mock import Mock, AsyncMock
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.offers.models import (
    OfferTemplate, Offer, OfferCompensation, OfferTerms,
    BackgroundVerification, OnboardingPlan
)
from app.modules.organizations.models import SalaryBand
from app.modules.offers.schemas import (
    OfferTemplateCreate, OfferCreate, OfferCompensationCreate, OfferTermsCreate,
    OfferApprovalAction, NegotiationRequest, BackgroundVerificationCreate,
    OnboardingPlanCreate, EmployeeConversionCreate
)
from app.modules.offers.enums import (
    OfferStatus, ApprovalStatus, EmploymentType, WorkMode,
    PayFrequency, NegotiationStatus, BGVStatus, OnboardingStatus
)
from app.modules.offers.validators import (
    OfferValidator, ApprovalValidator, NegotiationValidator,
    BGVValidator, OnboardingValidator, EmployeeConversionValidator
)
from app.modules.offers.exceptions import (
    OfferNotFoundException, InvalidOfferStatusException, CompensationValidationException,
    SalaryBandViolationException, OfferApprovalException, NegotiationException,
    BGVInitiationException, OnboardingException, EmployeeConversionException
)
from app.modules.offers.service import (
    OfferTemplateService, OfferService, SalaryBandService,
    NegotiationService, BGVService, OnboardingService,
    EmployeeConversionService, OfferWorkflowHooks
)
from app.modules.offers.ai_hooks import OfferAIHooks, HiringWorkflowAIHooks


# ==================== Fixtures ====================

@pytest.fixture
def mock_db():
    """Mock database session"""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def sample_org_id():
    """Sample organization ID"""
    return uuid.uuid4()


@pytest.fixture
def sample_user_id():
    """Sample user ID"""
    return uuid.uuid4()


@pytest.fixture
def sample_offer_id():
    """Sample offer ID"""
    return uuid.uuid4()


@pytest.fixture
def sample_template_data():
    """Sample offer template data"""
    return OfferTemplateCreate(
        template_name="Software Engineer Offer",
        description="Standard offer template for software engineers",
        job_category="Engineering",
        is_default=False,
        template_content={
            "sections": ["Introduction", "Compensation", "Benefits", "Terms"]
        }
    )


@pytest.fixture
def sample_compensation_data():
    """Sample compensation data"""
    return OfferCompensationCreate(
        currency_id=uuid.uuid4(),
        base_salary=1200000.0,
        variable_compensation=200000.0,
        joining_bonus=50000.0,
        bonus_percentage=10.0,
        allowances={"housing": 5000, "transport": 2000},
        benefits={"health_insurance": True, "retirement": True},
        pay_frequency="Monthly"
    )


@pytest.fixture
def sample_terms_data():
    """Sample offer terms data"""
    return OfferTermsCreate(
        employment_type="Full-time",
        probation_period_months=3,
        notice_period_days=30,
        work_location="Bangalore",
        work_mode="On-site",
        reporting_manager_id=uuid.uuid4(),
        department_id=uuid.uuid4()
    )


@pytest.fixture
def sample_offer_data(sample_compensation_data, sample_terms_data):
    """Sample offer creation data"""
    return OfferCreate(
        candidate_application_id=uuid.uuid4(),
        candidate_id=uuid.uuid4(),
        job_id=uuid.uuid4(),
        offered_designation_id=uuid.uuid4(),
        offer_template_id=uuid.uuid4(),
        issue_date=date.today(),
        expiry_date=date.today() + timedelta(days=15),
        start_date=date.today() + timedelta(days=30),
        compensation=sample_compensation_data,
        terms=sample_terms_data,
        internal_notes="Strong candidate, team match"
    )


@pytest.fixture
def sample_negotiation_data():
    """Sample negotiation data"""
    return NegotiationRequest(
        negotiator_type="Candidate",
        requested_base_salary=1400000.0,
        requested_total_compensation=1700000.0,
        comments="Based on market research and current offer from competitor",
        reason="Competitive offer"
    )


@pytest.fixture
def sample_bgv_data():
    """Sample BGV data"""
    return BackgroundVerificationCreate(
        candidate_id=uuid.uuid4(),
        offer_id=uuid.uuid4(),
        verification_provider=None,
        priority="Normal",
        check_items=[
            {
                "item_type": "Employment",
                "item_name": "Previous Employment Verification",
                "description": "Verify last 3 years employment",
                "provider": None,
                "documents_required": True
            },
            {
                "item_type": "Education",
                "item_name": "Education Verification",
                "description": "Verify degree from listed institution",
                "provider": None,
                "documents_required": True
            }
        ]
    )


@pytest.fixture
def sample_onboarding_plan_data():
    """Sample onboarding plan data"""
    return OnboardingPlanCreate(
        plan_name="Engineering Onboarding",
        description="Standard onboarding for engineering roles",
        job_category="Engineering",
        department_id=uuid.uuid4(),
        duration_weeks=4,
        is_default=False,
        tasks=[
            {
                "task_name": "HR Documentation",
                "description": "Complete all HR documentation",
                "task_type": "Documentation",
                "assignee_role": "HR",
                "department_id": uuid.uuid4(),
                "priority": "High",
                "sequence_order": 1,
                "due_days_after_joining": 1,
                "is_required": True
            },
            {
                "task_name": "IT Account Setup",
                "description": "Setup IT accounts and equipment",
                "task_type": "Equipment",
                "assignee_role": "IT",
                "department_id": uuid.uuid4(),
                "priority": "High",
                "sequence_order": 2,
                "due_days_after_joining": 1,
                "is_required": True
            }
        ]
    )


# ==================== Offer Validator Tests ====================

class TestOfferValidator:
    """Test suite for offer validation"""
    
    def test_validate_offer_dates_success(self):
        """Test successful offer date validation"""
        issue_date = date.today()
        expiry_date = date.today() + timedelta(days=15)
        start_date = date.today() + timedelta(days=30)
        # Should not raise exception
        OfferValidator.validate_offer_dates(issue_date, expiry_date, start_date)
    
    def test_validate_offer_dates_invalid_sequence(self):
        """Test validation fails with invalid date sequence"""
        issue_date = date.today()
        expiry_date = date.today() - timedelta(days=1)
        start_date = date.today() + timedelta(days=30)
        with pytest.raises(CompensationValidationException):
            OfferValidator.validate_offer_dates(issue_date, expiry_date, start_date)
    
    def test_validate_offer_dates_too_short_validity(self):
        """Test validation fails with too short validity period"""
        issue_date = date.today()
        expiry_date = date.today() + timedelta(days=5)
        start_date = date.today() + timedelta(days=10)
        with pytest.raises(CompensationValidationException):
            OfferValidator.validate_offer_dates(issue_date, expiry_date, start_date)
    
    def test_validate_status_transition_success(self):
        """Test successful status transition"""
        OfferValidator.validate_status_transition(OfferStatus.DRAFT, OfferStatus.PENDING_APPROVAL)
    
    def test_validate_status_transition_invalid(self):
        """Test validation fails with invalid transition"""
        with pytest.raises(InvalidOfferStatusException):
            OfferValidator.validate_status_transition(OfferStatus.ACCEPTED, OfferStatus.DRAFT)
    
    def test_validate_compensation_structure_success(self):
        """Test successful compensation structure validation"""
        compensation = {
            "base_salary": 1200000.0,
            "variable_compensation": 200000.0,
            "joining_bonus": 50000.0
        }
        # Should not raise exception
        OfferValidator.validate_compensation_structure(compensation)
    
    def test_validate_compensation_structure_negative(self):
        """Test validation fails with negative values"""
        compensation = {
            "base_salary": -100000.0,
            "variable_compensation": 200000.0,
            "joining_bonus": 50000.0
        }
        with pytest.raises(CompensationValidationException):
            OfferValidator.validate_compensation_structure(compensation)
    
    def test_validate_salary_band_compliance_within_band(self):
        """Test validation passes when within salary band"""
        # Should not raise exception
        OfferValidator.validate_salary_band_compliance(1200000.0, 1000000.0, 1500000.0)
    
    def test_validate_salary_band_compliance_violation(self):
        """Test validation fails when exceeding salary band"""
        with pytest.raises(SalaryBandViolationException):
            OfferValidator.validate_salary_band_compliance(1600000.0, 1000000.0, 1500000.0)


# ==================== Approval Validator Tests ====================

class TestApprovalValidator:
    """Test suite for approval validation"""
    
    def test_validate_approval_eligibility_success(self):
        """Test successful approval eligibility validation"""
        ApprovalValidator.validate_approval_eligibility(
            OfferStatus.PENDING_APPROVAL,
            ApprovalStatus.PENDING
        )
    
    def test_validate_approval_eligibility_wrong_status(self):
        """Test validation fails with wrong offer status"""
        with pytest.raises(OfferApprovalException):
            ApprovalValidator.validate_approval_eligibility(
                OfferStatus.DRAFT,
                ApprovalStatus.PENDING
            )


# ==================== Negotiation Validator Tests ====================

class TestNegotiationValidator:
    """Test suite for negotiation validation"""
    
    def test_validate_negotiation_eligibility_success(self):
        """Test successful negotiation eligibility validation"""
        NegotiationValidator.validate_negotiation_eligibility(OfferStatus.SENT)
    
    def test_validate_negotiation_eligibility_wrong_status(self):
        """Test validation fails with wrong offer status"""
        with pytest.raises(NegotiationException):
            NegotiationValidator.validate_negotiation_eligibility(OfferStatus.DRAFT)
    
    def test_validate_compensation_request_success(self):
        """Test successful compensation request validation"""
        NegotiationValidator.validate_compensation_request(1400000.0, 1200000.0)
    
    def test_validate_compensation_request_decrease(self):
        """Test validation fails with decrease request"""
        with pytest.raises(NegotiationException):
            NegotiationValidator.validate_compensation_request(1000000.0, 1200000.0)
    
    def test_validate_compensation_request_excessive_increase(self):
        """Test validation fails with excessive increase"""
        with pytest.raises(NegotiationException):
            NegotiationValidator.validate_compensation_request(2000000.0, 1200000.0)


# ==================== BGV Validator Tests ====================

class TestBGVValidator:
    """Test suite for BGV validation"""
    
    def test_validate_bgv_eligibility_success(self):
        """Test successful BGV eligibility validation"""
        BGVValidator.validate_bgv_eligibility(OfferStatus.ACCEPTED)
    
    def test_validate_bgv_eligibility_wrong_status(self):
        """Test validation fails with wrong offer status"""
        with pytest.raises(BGVInitiationException):
            BGVValidator.validate_bgv_eligibility(OfferStatus.SENT)
    
    def test_validate_check_items_success(self):
        """Test successful check items validation"""
        items = [
            {"item_type": "Employment", "item_name": "Employment Check"},
            {"item_type": "Education", "item_name": "Education Check"}
        ]
        # Should not raise exception
        BGVValidator.validate_check_items(items)
    
    def test_validate_check_items_empty(self):
        """Test validation fails with empty items"""
        with pytest.raises(BGVInitiationException):
            BGVValidator.validate_check_items([])


# ==================== Onboarding Validator Tests ====================

class TestOnboardingValidator:
    """Test suite for onboarding validation"""
    
    def test_validate_onboarding_eligibility_success(self):
        """Test successful onboarding eligibility validation"""
        OnboardingValidator.validate_onboarding_eligibility(
            OfferStatus.ACCEPTED,
            BGVStatus.COMPLETED
        )
    
    def test_validate_onboarding_eligibility_wrong_status(self):
        """Test validation fails with wrong offer status"""
        with pytest.raises(OnboardingException):
            OnboardingValidator.validate_onboarding_eligibility(
                OfferStatus.SENT,
                BGVStatus.COMPLETED
            )
    
    def test_validate_onboarding_plan_success(self):
        """Test successful onboarding plan validation"""
        tasks = [
            {"sequence_order": 1, "task_name": "Task 1"},
            {"sequence_order": 2, "task_name": "Task 2"}
        ]
        # Should not raise exception
        OnboardingValidator.validate_onboarding_plan(tasks)
    
    def test_validate_onboarding_plan_empty(self):
        """Test validation fails with empty tasks"""
        with pytest.raises(OnboardingException):
            OnboardingValidator.validate_onboarding_plan([])


# ==================== Employee Conversion Validator Tests ====================

class TestEmployeeConversionValidator:
    """Test suite for employee conversion validation"""
    
    def test_validate_conversion_eligibility_success(self):
        """Test successful conversion eligibility validation"""
        EmployeeConversionValidator.validate_conversion_eligibility(
            OfferStatus.ACCEPTED,
            BGVStatus.COMPLETED,
            OnboardingStatus.COMPLETED
        )
    
    def test_validate_conversion_eligibility_wrong_status(self):
        """Test validation fails with wrong offer status"""
        with pytest.raises(EmployeeConversionException):
            EmployeeConversionValidator.validate_conversion_eligibility(
                OfferStatus.SENT,
                BGVStatus.COMPLETED,
                OnboardingStatus.COMPLETED
            )


# ==================== Service Tests ====================

class TestOfferTemplateService:
    """Test suite for offer template service"""
    
    @pytest.mark.asyncio
    async def test_create_template_success(self, mock_db, sample_template_data, sample_org_id):
        """Test successful template creation"""
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        
        service = OfferTemplateService(mock_db)
        result = await service.create_template(sample_org_id, sample_template_data)
        
        assert result["status"] == "success"
        assert "template_id" in result


class TestOfferService:
    """Test suite for offer service"""
    
    @pytest.mark.asyncio
    async def test_create_offer_success(self, mock_db, sample_offer_data, sample_org_id, sample_user_id):
        """Test successful offer creation"""
        mock_db.add = Mock()
        mock_db.flush = AsyncMock()
        mock_db.commit = AsyncMock()
        
        service = OfferService(mock_db)
        service.salary_band_repo.get_salary_band = AsyncMock(return_value=None)
        service.workflow_hooks.on_offer_created = AsyncMock(return_value={"status": "success"})
        
        result = await service.create_offer(sample_org_id, sample_offer_data, sample_user_id)
        
        assert result["status"] == "success"
        assert "offer_id" in result
    
    @pytest.mark.asyncio
    async def test_submit_for_approval_success(self, mock_db, sample_org_id, sample_offer_id, sample_user_id):
        """Test successful offer submission for approval"""
        mock_offer = Mock(status=OfferStatus.DRAFT)
        
        mock_db.execute = AsyncMock()
        mock_db.commit = AsyncMock()
        
        service = OfferService(mock_db)
        service.offer_repo.get_offer_by_id = AsyncMock(return_value=mock_offer)
        service.offer_repo.update_offer_status = AsyncMock()
        service.workflow_hooks.on_offer_submitted_for_approval = AsyncMock(return_value={"status": "success"})
        
        result = await service.submit_for_approval(sample_org_id, sample_offer_id, sample_user_id)
        
        assert result["status"] == "success"


class TestNegotiationService:
    """Test suite for negotiation service"""
    
    @pytest.mark.asyncio
    async def test_initiate_negotiation_success(self, mock_db, sample_org_id, sample_offer_id, sample_negotiation_data):
        """Test successful negotiation initiation"""
        mock_offer = Mock(status=OfferStatus.SENT)
        mock_comp = Mock(total_compensation=1450000.0)
        
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        
        service = NegotiationService(mock_db)
        service.offer_repo.get_offer_by_id = AsyncMock(return_value=mock_offer)
        service.compensation_repo.get_compensation_by_offer = AsyncMock(return_value=mock_comp)
        service.negotiation_repo.create_negotiation = AsyncMock(return_value=Mock(id=uuid.uuid4()))
        service.offer_repo.update_offer_status = AsyncMock()
        
        result = await service.initiate_negotiation(sample_org_id, sample_offer_id, sample_negotiation_data)
        
        assert result["status"] == "success"
        assert "negotiation_id" in result


class TestBGVService:
    """Test suite for BGV service"""
    
    @pytest.mark.asyncio
    async def test_initiate_bgv_success(self, mock_db, sample_org_id, sample_bgv_data, sample_user_id):
        """Test successful BGV initiation"""
        mock_offer = Mock(status=OfferStatus.ACCEPTED)
        
        mock_db.add = Mock()
        mock_db.flush = AsyncMock()
        mock_db.commit = AsyncMock()
        
        service = BGVService(mock_db)
        service.offer_repo.get_offer_by_id = AsyncMock(return_value=mock_offer)
        service.bgv_repo.create_bgv = AsyncMock(return_value=Mock(id=uuid.uuid4()))
        service.workflow_hooks.on_bgv_initiated = AsyncMock(return_value={"status": "success"})
        
        result = await service.initiate_bgv(sample_org_id, sample_bgv_data, sample_user_id)
        
        assert result["status"] == "success"
        assert "bgv_id" in result


class TestOnboardingService:
    """Test suite for onboarding service"""
    
    @pytest.mark.asyncio
    async def test_create_onboarding_plan_success(self, mock_db, sample_org_id, sample_onboarding_plan_data):
        """Test successful onboarding plan creation"""
        mock_db.add = Mock()
        mock_db.flush = AsyncMock()
        mock_db.commit = AsyncMock()
        
        service = OnboardingService(mock_db)
        result = await service.create_onboarding_plan(sample_org_id, sample_onboarding_plan_data)
        
        assert result["status"] == "success"
        assert "plan_id" in result


class TestEmployeeConversionService:
    """Test suite for employee conversion service"""
    
    @pytest.mark.asyncio
    async def test_convert_to_employee_success(self, mock_db, sample_org_id, sample_user_id):
        """Test successful employee conversion"""
        mock_offer = Mock(status=OfferStatus.ACCEPTED, id=uuid.uuid4())
        mock_bgv = Mock(status=BGVStatus.COMPLETED)
        mock_checklist = Mock(status=OnboardingStatus.COMPLETED)
        
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        
        conversion_data = EmployeeConversionCreate(
            candidate_id=uuid.uuid4(),
            offer_id=uuid.uuid4(),
            employee_user_id=uuid.uuid4()
        )
        
        service = EmployeeConversionService(mock_db)
        service.offer_repo.get_offer_by_id = AsyncMock(return_value=mock_offer)
        service.bgv_repo.get_bgv_by_candidate = AsyncMock(return_value=mock_bgv)
        service.onboarding_repo.get_onboarding_checklist = AsyncMock(return_value=mock_checklist)
        service.conversion_repo.get_conversion_by_candidate = AsyncMock(return_value=None)
        service.conversion_repo.create_conversion = AsyncMock(return_value=Mock(id=uuid.uuid4(), employee_id=uuid.uuid4()))
        service.offer_repo.update_offer_status = AsyncMock()
        service.workflow_hooks.on_employee_converted = AsyncMock(return_value={"status": "success"})
        
        result = await service.convert_to_employee(sample_org_id, conversion_data, sample_user_id)
        
        assert result["status"] == "success"
        assert "conversion_id" in result
        assert "employee_id" in result


# ==================== Workflow Hooks Tests ====================

class TestOfferWorkflowHooks:
    """Test suite for offer workflow hooks"""
    
    @pytest.mark.asyncio
    async def test_on_offer_created(self, mock_db, sample_offer_id, sample_org_id, sample_user_id):
        """Test offer created hook"""
        hooks = OfferWorkflowHooks(mock_db)
        
        result = await hooks.on_offer_created(sample_offer_id, sample_org_id, sample_user_id)
        
        assert result["status"] == "success"
        assert "offer_id" in result


# ==================== AI Hooks Tests ====================

class TestOfferAIHooks:
    """Test suite for offer AI hooks"""
    
    @pytest.mark.asyncio
    async def test_on_compensation_intelligence_requested(self, mock_db, sample_offer_id):
        """Test compensation intelligence hook"""
        hooks = OfferAIHooks(mock_db)
        
        result = await hooks.on_compensation_intelligence_requested(
            sample_offer_id,
            {"experience": "5 years"},
            {"position": "Software Engineer"},
            {"min_salary": 1000000, "max_salary": 1500000}
        )
        
        assert result["offer_id"] == str(sample_offer_id)
        assert result["hook_status"] == "ready_for_langgraph_integration"
        assert "agent_type" in result
    
    @pytest.mark.asyncio
    async def test_on_negotiation_analysis_requested(self, mock_db, sample_offer_id):
        """Test negotiation analysis hook"""
        hooks = OfferAIHooks(mock_db)
        
        result = await hooks.on_negotiation_analysis_requested(
            sample_offer_id,
            {"requested_salary": 1600000},
            {"current_salary": 1200000},
            {"min_salary": 1000000, "max_salary": 1500000}
        )
        
        assert result["offer_id"] == str(sample_offer_id)
        assert "negotiation_analysis" in result
        assert result["hook_status"] == "ready_for_langgraph_integration"


# ==================== Test Configuration ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])