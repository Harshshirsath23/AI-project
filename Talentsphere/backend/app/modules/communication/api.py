from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid

from app.database.session import get_async_db
from app.modules.auth.dependencies import (
    get_current_organization, get_current_user, require_permission
)
from app.modules.communication.schemas import (
    CommunicationTemplateCreate, CommunicationTemplateResponse,
    MessageCreate, MessageResponse, ConversationCreate, ConversationResponse,
    NotificationCreate, NotificationResponse,
    WebhookConfigurationCreate, WebhookConfigurationResponse,
    NotificationPreferenceCreate, NotificationPreferenceResponse,
    AutomationPolicyCreate, AutomationPolicyResponse,
    MessageCreateForConversation, TemplateVariableSubstitution, SuccessResponse
)
from app.modules.communication.service import (
    TemplateService, MessageService, ConversationService,
    NotificationService, NotificationPreferenceService,
    WebhookService
)

router = APIRouter(prefix="/communication", tags=["Communication & Collaboration"])


# ==================== Template Endpoints ====================

@router.post("/templates", summary="Create Communication Template", dependencies=[Depends(require_permission("communication:template_write"))])
async def create_template(
    template_data: CommunicationTemplateCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new communication template"""
    service = TemplateService(db)
    return await service.create_template(org_id, template_data)

@router.get("/templates/{template_id}", response_model=CommunicationTemplateResponse, summary="Get Template by ID", dependencies=[Depends(require_permission("communication:template_read"))])
async def get_template(
    template_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get a specific template by ID"""
    service = TemplateService(db)
    return await service.get_template(org_id, template_id)

@router.post("/templates/substitute", summary="Substitute Template Variables", dependencies=[Depends(require_permission("communication:template_read"))])
async def substitute_template_variables(
    substitution_data: TemplateVariableSubstitution,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Substitute variables in template"""
    service = TemplateService(db)
    return await service.substitute_template_variables(org_id, substitution_data)


# ==================== Message Endpoints ====================

@router.post("/messages", summary="Create and Queue Message", dependencies=[Depends(require_permission("communication:create"))])
async def create_message(
    message_data: MessageCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Create and queue a message"""
    service = MessageService(db)
    return await service.create_message(org_id, message_data, current_user["id"])

@router.post("/messages/{message_id}/send", summary="Send Message", dependencies=[Depends(require_permission("communication:send"))])
async def send_message(
    message_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Send queued message via provider"""
    service = MessageService(db)
    return await service.send_message(org_id, message_id)

@router.get("/messages/{message_id}/status", summary="Get Message Status", dependencies=[Depends(require_permission("communication:read"))])
async def get_message_status(
    message_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get message delivery status"""
    service = MessageService(db)
    return await service.get_message_status(org_id, message_id)


# ==================== Conversation Endpoints ====================

@router.post("/conversations", summary="Create Conversation", dependencies=[Depends(require_permission("conversation:write"))])
async def create_conversation(
    conversation_data: ConversationCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new conversation"""
    service = ConversationService(db)
    return await service.create_conversation(org_id, conversation_data)

@router.get("/conversations/{conversation_id}", response_model=ConversationResponse, summary="Get Conversation by ID", dependencies=[Depends(require_permission("conversation:read"))])
async def get_conversation(
    conversation_id: uuid.UUID,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get a specific conversation by ID"""
    service = ConversationService(db)
    return await service.get_conversation(org_id, conversation_id)

@router.post("/conversations/messages", summary="Send Message to Conversation", dependencies=[Depends(require_permission("conversation:write"))])
async def send_message_to_conversation(
    message_data: MessageCreateForConversation,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Send message to a conversation"""
    service = ConversationService(db)
    return await service.send_message_to_conversation(org_id, message_data)


# ==================== Notification Endpoints ====================

@router.post("/notifications", summary="Create Notification", dependencies=[Depends(require_permission("notification:manage"))])
async def create_notification(
    notification_data: NotificationCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a notification"""
    service = NotificationService(db)
    return await service.create_notification(org_id, notification_data)

@router.get("/notifications/{recipient_id}", response_model=List[NotificationResponse], summary="Get User Notifications", dependencies=[Depends(require_permission("notification:read"))])
async def get_user_notifications(
    recipient_id: uuid.UUID,
    status: Optional[str] = None,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get notifications for a user"""
    service = NotificationService(db)
    return await service.get_user_notifications(org_id, recipient_id, status)


# ==================== Notification Preferences ====================

@router.post("/preferences", summary="Set Notification Preference", dependencies=[Depends(require_permission("notification:manage"))])
async def set_preference(
    preference_data: NotificationPreferenceCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Set notification preference for user"""
    service = NotificationPreferenceService(db)
    return await service.set_preference(org_id, preference_data)


# ==================== Webhook Endpoints ====================

@router.post("/webhooks", summary="Create Webhook Configuration", dependencies=[Depends(require_permission("communication:manage"))])
async def create_webhook_config(
    webhook_data: WebhookConfigurationCreate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Create webhook configuration"""
    service = WebhookService(db)
    return await service.create_webhook_config(org_id, webhook_data)

@router.post("/webhooks/{webhook_id}/process", summary="Process Webhook", dependencies=[Depends(require_permission("communication:manage"))])
async def process_webhook(
    webhook_id: uuid.UUID,
    event_type: str,
    payload: dict,
    db: AsyncSession = Depends(get_async_db)
):
    """Process incoming webhook from provider"""
    service = WebhookService(db)
    return await service.process_webhook(webhook_id, event_type, payload)