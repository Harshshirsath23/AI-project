from typing import Optional
from fastapi import HTTPException, status


class OfferException(Exception):
    """Base exception for offers module"""
    pass


class OfferNotFoundException(HTTPException):
    def __init__(self, offer_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Offer with ID {offer_id} not found"
        )


class InvalidOfferStatusException(HTTPException):
    def __init__(self, current_status: str, required_status: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid offer status transition. Current: {current_status}, Required: {required_status}"
        )


class CompensationValidationException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Compensation validation failed: {message}"
        )


class SalaryBandViolationException(HTTPException):
    def __init__(self, min_salary: float, max_salary: float, proposed_salary: float):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Proposed compensation {proposed_salary} exceeds salary band range {min_salary} - {max_salary}"
        )


class OfferApprovalException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Offer approval failed: {message}"
        )


class InsufficientApprovalAuthorityException(HTTPException):
    def __init__(self, required_role: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient approval authority. Required role: {required_role}"
        )


class OfferAlreadyApprovedException(HTTPException):
    def __init__(self, offer_id: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Offer {offer_id} is already approved"
        )


class OfferAlreadySentException(HTTPException):
    def __init__(self, offer_id: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Offer {offer_id} has already been sent to candidate"
        )


class NegotiationException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Negotiation failed: {message}"
        )


class BGVInitiationException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Background verification initialization failed: {message}"
        )


class OnboardingException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Onboarding operation failed: {message}"
        )


class EmployeeConversionException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Employee conversion failed: {message}"
        )


class TemplateNotFoundException(HTTPException):
    def __init__(self, template_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Offer template with ID {template_id} not found"
        )


class DocumentGenerationException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document generation failed: {message}"
        )


class StorageException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Storage operation failed: {message}"
        )