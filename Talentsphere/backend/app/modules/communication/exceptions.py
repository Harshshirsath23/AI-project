from typing import Optional
from fastapi import HTTPException, status


class CommunicationException(Exception):
    """Base exception for communication module"""
    pass


class TemplateNotFoundException(HTTPException):
    def __init__(self, template_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Communication template with ID {template_id} not found"
        )


class MessageNotFoundException(HTTPException):
    def __init__(self, message_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Message with ID {message_id} not found"
        )


class ConversationNotFoundException(HTTPException):
    def __init__(self, conversation_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation with ID {conversation_id} not found"
        )


class InvalidMessageStatusException(HTTPException):
    def __init__(self, current_status: str, required_status: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid message status transition. Current: {current_status}, Required: {required_status}"
        )


class TemplateValidationException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Template validation failed: {message}"
        )


class ProviderException(HTTPException):
    def __init__(self, provider: str, message: str):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Provider {provider} error: {message}"
        )


class MessageSendException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send message: {message}"
        )


class WebhookException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Webhook processing failed: {message}"
        )


class InvalidWebhookSignatureException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook signature"
        )


class NotificationPreferenceException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Notification preference error: {message}"
        )


class RateLimitExceededException(HTTPException):
    def __init__(self, limit: int, window: str):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded: {limit} messages per {window}"
        )


class InvalidRecipientException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid recipient: {message}"
        )


class TemplateVariableException(HTTPException):
    def __init__(self, variable: str, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Template variable error for {variable}: {message}"
        )


class AutomationPolicyException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Automation policy violation: {message}"
        )