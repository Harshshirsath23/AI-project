from typing import List, Optional
from datetime import datetime, date, timedelta
from fastapi import HTTPException, status

from app.modules.offers.enums import (
    OfferStatus, ApprovalStatus, EmploymentType, WorkMode,
    PayFrequency, NegotiationStatus, BGVStatus, CheckItemStatus,
    TaskStatus, ApproverRole, OnboardingStatus
)
from app.modules.offers.exceptions import (
    InvalidOfferStatusException, CompensationValidationException,
    SalaryBandViolationException, OfferApprovalException,
    InsufficientApprovalAuthorityException, OfferAlreadyApprovedException,
    OfferAlreadySentException, NegotiationException, BGVInitiationException,
    OnboardingException, EmployeeConversionException
)


class OfferValidator:
    """Validator for offer operations"""
    
    @staticmethod
    def validate_offer_dates(issue_date: date, expiry_date: date, start_date: date) -> None:
        """Validate offer date sequence"""
        if issue_date > expiry_date:
            raise CompensationValidationException("Issue date cannot be after expiry date")
        
        if expiry_date < date.today():
            raise CompensationValidationException("Expiry date cannot be in the past")
        
        if start_date < date.today():
            raise CompensationValidationException("Start date cannot be in the past")
        
        if start_date < expiry_date:
            raise CompensationValidationException("Start date should be after or on expiry date")
        
        if (expiry_date - issue_date).days < 7:
            raise CompensationValidationException("Offer validity period should be at least 7 days")
    
    @staticmethod
    def validate_status_transition(current_status: str, new_status: str) -> None:
        """Validate offer status transitions"""
        valid_transitions = {
            OfferStatus.DRAFT: [OfferStatus.PENDING_APPROVAL, OfferStatus.WITHDRAWN],
            OfferStatus.PENDING_APPROVAL: [OfferStatus.APPROVED, OfferStatus.REJECTED, OfferStatus.WITHDRAWN],
            OfferStatus.APPROVED: [OfferStatus.GENERATED, OfferStatus.WITHDRAWN],
            OfferStatus.GENERATED: [OfferStatus.SENT, OfferStatus.WITHDRAWN],
            OfferStatus.SENT: [OfferStatus.VIEWED, OfferStatus.NEGOTIATING, OfferStatus.ACCEPTED, OfferStatus.REJECTED, OfferStatus.EXPIRED],
            OfferStatus.VIEWED: [OfferStatus.NEGOTIATING, OfferStatus.ACCEPTED, OfferStatus.REJECTED, OfferStatus.EXPIRED],
            OfferStatus.NEGOTIATING: [OfferStatus.SENT, OfferStatus.ACCEPTED, OfferStatus.REJECTED, OfferStatus.EXPIRED],
            OfferStatus.ACCEPTED: [OfferStatus.JOINING_CONFIRMED],
            OfferStatus.REJECTED: [],  # Terminal state
            OfferStatus.EXPIRED: [],  # Terminal state
            OfferStatus.WITHDRAWN: [],  # Terminal state
            OfferStatus.JOINING_CONFIRMED: []  # Terminal state
        }
        
        if current_status not in valid_transitions:
            raise InvalidOfferStatusException(current_status, "Unknown current status")
        
        if new_status not in valid_transitions[current_status]:
            raise InvalidOfferStatusException(current_status, new_status)
    
    @staticmethod
    def validate_compensation_structure(compensation: dict) -> None:
        """Validate compensation structure"""
        base_salary = compensation.get("base_salary", 0)
        variable_comp = compensation.get("variable_compensation", 0)
        joining_bonus = compensation.get("joining_bonus", 0)
        
        if base_salary <= 0:
            raise CompensationValidationException("Base salary must be positive")
        
        if variable_comp < 0:
            raise CompensationValidationException("Variable compensation cannot be negative")
        
        if joining_bonus < 0:
            raise CompensationValidationException("Joining bonus cannot be negative")
        
        total = base_salary + variable_comp + joining_bonus
        if total <= 0:
            raise CompensationValidationException("Total compensation must be positive")
    
    @staticmethod
    def validate_salary_band_compliance(
        proposed_salary: float,
        min_salary: float,
        max_salary: float,
        requires_approval: bool = True
    ) -> None:
        """Validate if compensation is within salary band"""
        if min_salary <= proposed_salary <= max_salary:
            return  # Within band
        
        if requires_approval:
            raise SalaryBandViolationException(min_salary, max_salary, proposed_salary)
        else:
            # Just warn but allow
            pass


class ApprovalValidator:
    """Validator for offer approval operations"""
    
    @staticmethod
    def validate_approval_authority(user_role: str, required_roles: List[str]) -> None:
        """Validate user has approval authority"""
        if user_role not in required_roles:
            raise InsufficientApprovalAuthorityException(required_roles[0])
    
    @staticmethod
    def validate_approval_eligibility(offer_status: str, approval_status: str) -> None:
        """Validate offer is eligible for approval"""
        if offer_status != OfferStatus.PENDING_APPROVAL:
            raise OfferApprovalException(f"Offer must be in Pending Approval status for approval. Current: {offer_status}")
        
        if approval_status == ApprovalStatus.APPROVED:
            raise OfferAlreadyApprovedException("Offer is already approved")


class NegotiationValidator:
    """Validator for negotiation operations"""
    
    @staticmethod
    def validate_negotiation_eligibility(offer_status: str) -> None:
        """Validate offer is eligible for negotiation"""
        negotiable_statuses = [OfferStatus.SENT, OfferStatus.VIEWED, OfferStatus.NEGOTIATING]
        
        if offer_status not in negotiable_statuses:
            raise NegotiationException(f"Offer must be sent or viewed for negotiation. Current: {offer_status}")
    
    @staticmethod
    def validate_compensation_request(
        requested_salary: float,
        current_salary: float,
        max_increase_percentage: float = 20
    ) -> None:
        """Validate if compensation request is reasonable"""
        if requested_salary <= current_salary:
            raise NegotiationException("Requested salary must be higher than current offer")
        
        increase_percentage = ((requested_salary - current_salary) / current_salary) * 100
        
        if increase_percentage > max_increase_percentage:
            raise NegotiationException(
                f"Requested increase ({increase_percentage:.1f}%) exceeds maximum allowed ({max_increase_percentage}%)"
            )


class BGVValidator:
    """Validator for background verification operations"""
    
    @staticmethod
    def validate_bgv_eligibility(offer_status: str) -> None:
        """Validate offer is eligible for BGV"""
        if offer_status != OfferStatus.ACCEPTED:
            raise BGVInitiationException(f"Offer must be accepted before BGV. Current: {offer_status}")
    
    @staticmethod
    def validate_check_items(items: List[dict]) -> None:
        """Validate background check items configuration"""
        if not items:
            raise BGVInitiationException("At least one background check item is required")
        
        valid_types = [
            "Employment", "Education", "Criminal", "Identity",
            "Address", "Reference", "Drug Test", "Credit Check"
        ]
        
        for item in items:
            # Handle both dict and Pydantic models
            item_type = item.get("item_type") if isinstance(item, dict) else getattr(item, "item_type", None)
            if item_type not in valid_types:
                raise BGVInitiationException(f"Invalid check item type: {item_type}")


class OnboardingValidator:
    """Validator for onboarding operations"""
    
    @staticmethod
    def validate_onboarding_eligibility(offer_status: str, bgv_status: str) -> None:
        """Validate candidate is eligible for onboarding"""
        if offer_status != OfferStatus.ACCEPTED:
            raise OnboardingException(f"Offer must be accepted for onboarding. Current: {offer_status}")
        
        if bgv_status not in [BGVStatus.COMPLETED, None]:
            raise OnboardingException(f"BGV must be completed for onboarding. Current: {bgv_status}")
    
    @staticmethod
    def validate_task_dependencies(
        task_dependencies: Optional[dict],
        completed_tasks: List[str]
    ) -> None:
        """Validate if task dependencies are satisfied"""
        if not task_dependencies:
            return
        
        required_tasks = task_dependencies.get("required_tasks", [])
        
        for required_task in required_tasks:
            if required_task not in completed_tasks:
                raise OnboardingException(f"Required task not completed: {required_task}")
    
    @staticmethod
    def validate_onboarding_plan(tasks: List[dict]) -> None:
        """Validate onboarding plan structure"""
        if not tasks:
            raise OnboardingException("Onboarding plan must have at least one task")
        
        sequence_numbers = []
        for task in tasks:
            # Handle both dict and Pydantic models
            seq_order = task.get("sequence_order", 0) if isinstance(task, dict) else getattr(task, "sequence_order", 0)
            sequence_numbers.append(seq_order)
        
        if len(set(sequence_numbers)) != len(sequence_numbers):
            raise OnboardingException("Task sequence numbers must be unique")


class EmployeeConversionValidator:
    """Validator for employee conversion operations"""
    
    @staticmethod
    def validate_conversion_eligibility(
        offer_status: str,
        bgv_status: str,
        onboarding_status: str
    ) -> None:
        """Validate candidate is eligible for employee conversion"""
        if offer_status != OfferStatus.ACCEPTED:
            raise EmployeeConversionException(f"Offer must be accepted. Current: {offer_status}")
        
        if bgv_status != BGVStatus.COMPLETED:
            raise EmployeeConversionException(f"BGV must be completed. Current: {bgv_status}")
        
        if onboarding_status != OnboardingStatus.COMPLETED:
            raise EmployeeConversionException(f"Onboarding must be completed. Current: {onboarding_status}")
    
    @staticmethod
    def validate_employee_not_exists(candidate_id: str, existing_employee_id: Optional[str]) -> None:
        """Validate employee doesn't already exist for candidate"""
        if existing_employee_id:
            raise EmployeeConversionException(f"Employee already exists for candidate: {candidate_id}")