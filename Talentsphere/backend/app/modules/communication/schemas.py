from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

from app.modules.communication.enums import (
    CommunicationChannel, MessageStatus, NotificationType,
    NotificationPriority, ConversationType, MessageDirection,
    AutomationPolicy
)


# ==================== Template Schemas ====================

class CommunicationTemplateCreate(BaseModel):
    template_name: str = Field(..., description="Template name")
    template_type: str = Field(..., description="Template type (email, sms, whatsapp)")
    notification_type: str = Field(..., description="Notification type")
    subject: Optional[str] = Field(None, description="Email subject")
    body: str = Field(..., description="Template body with {{variables}}")
    variables: Optional[Dict[str, Any]] = Field(None, description="Available variables schema")
    is_default: bool = Field(default=False, description="Whether this is default template")

class CommunicationTemplateResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    template_name: str
    template_type: str
    notification_type: str
    subject: Optional[str]
    body: str
    variables: Optional[Dict[str, Any]]
    is_default: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Message Schemas ====================

class MessageCreate(BaseModel):
    recipient_id: uuid.UUID = Field(..., description="Recipient ID")
    recipient_type: str = Field(..., description="Recipient type (user, candidate)")
    recipient_email: Optional[str] = Field(None, description="Recipient email")
    recipient_phone: Optional[str] = Field(None, description="Recipient phone")
    channel: str = Field(..., description="Communication channel")
    notification_type: str = Field(..., description="Notification type")
    template_id: Optional[uuid.UUID] = Field(None, description="Template ID")
    subject: Optional[str] = Field(None, description="Message subject")
    body: str = Field(..., description="Message body")
    priority: str = Field(default="Normal", description="Message priority")
    scheduled_at: Optional[datetime] = Field(None, description="Scheduled send time")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    conversation_id: Optional[uuid.UUID] = Field(None, description="Associated conversation ID")
    requires_approval: bool = Field(default=False, description="Whether approval is required")

class MessageResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    recipient_id: uuid.UUID
    recipient_type: str
    recipient_email: Optional[str]
    recipient_phone: Optional[str]
    channel: str
    notification_type: str
    template_id: Optional[uuid.UUID]
    subject: Optional[str]
    body: str
    priority: str
    status: str
    scheduled_at: Optional[datetime]
    sent_at: Optional[datetime]
    delivered_at: Optional[datetime]
    read_at: Optional[datetime]
    failure_reason: Optional[str]
    retry_count: int
    provider_message_id: Optional[str]
    conversation_id: Optional[uuid.UUID]
    requires_approval: bool
    approved_by: Optional[uuid.UUID]
    approved_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Conversation Schemas ====================

class ConversationCreate(BaseModel):
    conversation_type: str = Field(..., description="Conversation type")
    entity_id: uuid.UUID = Field(..., description="Associated entity ID")
    entity_type: str = Field(..., description="Entity type (candidate, application, interview, offer)")
    subject: str = Field(..., description="Conversation subject")
    participants: Optional[Dict[str, Any]] = Field(None, description="Participants list")

class ConversationResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    conversation_type: str
    entity_id: uuid.UUID
    entity_type: str
    subject: str
    participants: Optional[Dict[str, Any]]
    status: str
    last_message_at: Optional[datetime]
    message_count: int
    unread_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MessageCreateForConversation(BaseModel):
    conversation_id: uuid.UUID = Field(..., description="Conversation ID")
    sender_id: uuid.UUID = Field(..., description="Sender ID")
    sender_type: str = Field(..., description="Sender type")
    direction: str = Field(..., description="Message direction")
    content: str = Field(..., description="Message content")
    channel: str = Field(default="In-App", description="Communication channel")
    attachments: Optional[Dict[str, Any]] = Field(None, description="Attachments")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    parent_message_id: Optional[uuid.UUID] = Field(None, description="Parent message ID for replies")


# ==================== Notification Schemas ====================

class NotificationCreate(BaseModel):
    recipient_id: uuid.UUID = Field(..., description="Recipient ID")
    recipient_type: str = Field(..., description="Recipient type")
    notification_type: str = Field(..., description="Notification type")
    title: str = Field(..., description="Notification title")
    body: str = Field(..., description="Notification body")
    channel: str = Field(..., description="Notification channel")
    priority: str = Field(default="Normal", description="Notification priority")
    action_url: Optional[str] = Field(None, description="Action URL")
    action_label: Optional[str] = Field(None, description="Action button label")
    expires_at: Optional[datetime] = Field(None, description="Expiration time")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    related_entity_id: Optional[uuid.UUID] = Field(None, description="Related entity ID")
    related_entity_type: Optional[str] = Field(None, description="Related entity type")

class NotificationResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    recipient_id: uuid.UUID
    recipient_type: str
    notification_type: str
    title: str
    body: str
    channel: str
    priority: str
    status: str
    action_url: Optional[str]
    action_label: Optional[str]
    expires_at: Optional[datetime]
    metadata: Optional[Dict[str, Any]]
    related_entity_id: Optional[uuid.UUID]
    related_entity_type: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Webhook Schemas ====================

class WebhookConfigurationCreate(BaseModel):
    provider: str = Field(..., description="Provider name")
    webhook_url: str = Field(..., description="Webhook URL")
    secret_key: str = Field(..., description="Secret key for signature verification")
    events: List[str] = Field(..., description="List of subscribed events")

class WebhookConfigurationResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    provider: str
    webhook_url: str
    secret_key: str
    events: Optional[Dict[str, Any]]
    is_active: bool
    last_triggered_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Notification Preference Schemas ====================

class NotificationPreferenceCreate(BaseModel):
    user_id: uuid.UUID = Field(..., description="User ID")
    notification_type: str = Field(..., description="Notification type")
    email_enabled: bool = Field(default=True, description="Email notifications enabled")
    in_app_enabled: bool = Field(default=True, description="In-app notifications enabled")
    sms_enabled: bool = Field(default=False, description="SMS notifications enabled")
    whatsapp_enabled: bool = Field(default=False, description="WhatsApp notifications enabled")
    push_enabled: bool = Field(default=False, description="Push notifications enabled")

class NotificationPreferenceResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    user_id: uuid.UUID
    notification_type: str
    email_enabled: bool
    in_app_enabled: bool
    sms_enabled: bool
    whatsapp_enabled: bool
    push_enabled: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Automation Policy Schemas ====================

class AutomationPolicyCreate(BaseModel):
    policy_name: str = Field(..., description="Policy name")
    notification_type: str = Field(..., description="Notification type")
    automation_type: str = Field(..., description="Automation type")
    conditions: Optional[Dict[str, Any]] = Field(None, description="Policy conditions")
    required_approval_level: Optional[int] = Field(None, description="Required approval level")

class AutomationPolicyResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    policy_name: str
    notification_type: str
    automation_type: str
    conditions: Optional[Dict[str, Any]]
    required_approval_level: Optional[int]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Utility Schemas ====================

class SuccessResponse(BaseModel):
    status: str = Field(default="success", description="Operation status")
    message: str = Field(..., description="Success message")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional data")


class MessageBatchCreate(BaseModel):
    messages: List[MessageCreate] = Field(..., description="List of messages to send")


class TemplateVariableSubstitution(BaseModel):
    template_id: uuid.UUID = Field(..., description="Template ID")
    variables: Dict[str, Any] = Field(..., description="Variable values for substitution")