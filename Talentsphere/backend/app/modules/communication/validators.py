from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status

from app.modules.communication.enums import (
    CommunicationChannel, MessageStatus, NotificationType,
    NotificationPriority, ConversationType, MessageDirection
)
from app.modules.communication.exceptions import (
    TemplateValidationException, InvalidMessageStatusException,
    InvalidRecipientException, TemplateVariableException
)


class TemplateValidator:
    """Validator for communication templates"""
    
    @staticmethod
    def validate_template_structure(template_data: dict) -> None:
        """Validate template structure"""
        if not template_data.get("body"):
            raise TemplateValidationException("Template body is required")
        
        if template_data.get("template_type") == "email" and not template_data.get("subject"):
            raise TemplateValidationException("Email templates require a subject")
    
    @staticmethod
    def validate_template_variables(body: str, variables: Optional[dict]) -> None:
        """Validate template variables"""
        import re
        # Find all {{variable}} patterns
        pattern = r'\{\{([^}]+)\}\}'
        found_variables = set(re.findall(pattern, body))
        
        if variables:
            variable_names = set(variables.keys())
            # Check if all found variables are defined
            undefined = found_variables - variable_names
            if undefined:
                raise TemplateVariableException(
                    list(undefined)[0],
                    f"Variable not defined in template schema"
                )
    
    @staticmethod
    def substitute_variables(body: str, variables: Dict[str, Any]) -> str:
        """Substitute variables in template body"""
        for key, value in variables.items():
            body = body.replace(f"{{{{{key}}}}}", str(value))
        return body


class MessageValidator:
    """Validator for message operations"""
    
    @staticmethod
    def validate_recipient(recipient_data: dict) -> None:
        """Validate recipient information"""
        recipient_type = recipient_data.get("recipient_type")
        
        if recipient_type not in ["user", "candidate"]:
            raise InvalidRecipientException(f"Invalid recipient type: {recipient_type}")
        
        if recipient_data.get("channel") == CommunicationChannel.EMAIL and not recipient_data.get("recipient_email"):
            raise InvalidRecipientException("Email channel requires recipient_email")
        
        if recipient_data.get("channel") in [CommunicationChannel.SMS, CommunicationChannel.WHATSAPP] and not recipient_data.get("recipient_phone"):
            raise InvalidRecipientException(f"{recipient_data.get('channel')} channel requires recipient_phone")
    
    @staticmethod
    def validate_status_transition(current_status: str, new_status: str) -> None:
        """Validate message status transitions"""
        valid_transitions = {
            MessageStatus.QUEUED: [MessageStatus.PROCESSING, MessageStatus.CANCELLED],
            MessageStatus.PROCESSING: [MessageStatus.SENT, MessageStatus.FAILED],
            MessageStatus.SENT: [MessageStatus.DELIVERED, MessageStatus.FAILED, MessageStatus.BOUNCED],
            MessageStatus.DELIVERED: [MessageStatus.READ],
            MessageStatus.FAILED: [MessageStatus.RETRY, MessageStatus.CANCELLED],
            MessageStatus.RETRY: [MessageStatus.PROCESSING, MessageStatus.CANCELLED],
            MessageStatus.BOUNCED: [MessageStatus.CANCELLED],
            MessageStatus.READ: [],  # Terminal state
            MessageStatus.CANCELLED: []  # Terminal state
        }
        
        if current_status not in valid_transitions:
            raise InvalidMessageStatusException(current_status, "Unknown current status")
        
        if new_status not in valid_transitions[current_status]:
            raise InvalidMessageStatusException(current_status, new_status)


class ConversationValidator:
    """Validator for conversation operations"""
    
    @staticmethod
    def validate_conversation_creation(conversation_data: dict) -> None:
        """Validate conversation creation"""
        if not conversation_data.get("entity_id"):
            raise Exception("Entity ID is required for conversation")
        
        if conversation_data.get("conversation_type") not in [
            ConversationType.CANDIDATE,
            ConversationType.APPLICATION,
            ConversationType.JOB,
            ConversationType.INTERVIEW,
            ConversationType.OFFER,
            ConversationType.GENERAL
        ]:
            raise Exception(f"Invalid conversation type: {conversation_data.get('conversation_type')}")


class NotificationValidator:
    """Validator for notification operations"""
    
    @staticmethod
    def validate_notification_priority(priority: str) -> None:
        """Validate notification priority"""
        if priority not in ["Low", "Normal", "High", "Urgent"]:
            raise Exception(f"Invalid priority: {priority}")
    
    @staticmethod
    def validate_notification_channel(channel: str) -> None:
        """Validate notification channel"""
        if channel not in ["Email", "SMS", "WhatsApp", "In-App", "Push"]:
            raise Exception(f"Invalid channel: {channel}")