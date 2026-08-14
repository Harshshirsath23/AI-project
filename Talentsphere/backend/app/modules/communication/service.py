from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from datetime import datetime, timedelta

from app.modules.communication.models import (
    CommunicationTemplate, MessageQueue, Conversation, Message,
    Notification, WebhookConfiguration, WebhookLog,
    NotificationPreference, AutomationPolicy
)
from app.modules.communication.schemas import (
    CommunicationTemplateCreate, MessageCreate, ConversationCreate,
    NotificationCreate, WebhookConfigurationCreate,
    NotificationPreferenceCreate, AutomationPolicyCreate,
    MessageCreateForConversation, TemplateVariableSubstitution
)
from app.modules.communication.enums import (
    CommunicationChannel, MessageStatus, NotificationType,
    NotificationPriority, ConversationType, MessageDirection,
    AutomationPolicy
)
from app.modules.communication.validators import (
    TemplateValidator, MessageValidator, ConversationValidator,
    NotificationValidator
)
from app.modules.communication.exceptions import (
    TemplateNotFoundException, MessageNotFoundException, ConversationNotFoundException,
    ProviderException, AutomationPolicyException
)
from app.modules.communication.repository import (
    TemplateRepository, MessageQueueRepository, ConversationRepository,
    MessageRepository, NotificationRepository, NotificationPreferenceRepository,
    WebhookRepository, AutomationPolicyRepository
)


class TemplateService:
    """Service for communication template management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.template_repo = TemplateRepository(db)
    
    async def create_template(
        self, 
        org_id: uuid.UUID, 
        template_data: CommunicationTemplateCreate
    ) -> Dict[str, Any]:
        """Create communication template"""
        TemplateValidator.validate_template_structure(template_data.model_dump())
        TemplateValidator.validate_template_variables(
            template_data.body, 
            template_data.variables
        )
        
        template_dict = template_data.model_dump()
        template = await self.template_repo.create_template(org_id, template_dict)
        
        return {
            "status": "success",
            "template_id": str(template.id),
            "message": "Template created successfully"
        }
    
    async def get_template(
        self, 
        org_id: uuid.UUID, 
        template_id: uuid.UUID
    ) -> Optional[CommunicationTemplate]:
        """Get template by ID"""
        template = await self.template_repo.get_template_by_id(org_id, template_id)
        if not template:
            raise TemplateNotFoundException(str(template_id))
        return template
    
    async def substitute_template_variables(
        self, 
        org_id: uuid.UUID, 
        substitution_data: TemplateVariableSubstitution
    ) -> Dict[str, Any]:
        """Substitute variables in template"""
        template = await self.template_repo.get_template_by_id(
            org_id, 
            substitution_data.template_id
        )
        if not template:
            raise TemplateNotFoundException(str(substitution_data.template_id))
        
        substituted_body = TemplateValidator.substitute_variables(
            template.body,
            substitution_data.variables
        )
        
        return {
            "status": "success",
            "substituted_body": substituted_body,
            "subject": template.subject
        }


class MessageService:
    """Service for message queue management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.message_repo = MessageQueueRepository(db)
        self.provider_service = ProviderService(db)
    
    async def create_message(
        self, 
        org_id: uuid.UUID, 
        message_data: MessageCreate,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Create and queue message"""
        MessageValidator.validate_recipient(message_data.model_dump())
        
        message_dict = message_data.model_dump()
        message_dict["organization_id"] = org_id
        
        # Check automation policy
        automation_policy = await self.check_automation_policy(
            org_id, 
            message_data.notification_type
        )
        
        if automation_policy and automation_policy.automation_type == AutomationPolicy.HUMAN_APPROVAL:
            message_dict["requires_approval"] = True
        
        message = await self.message_repo.create_message(message_dict)
        
        return {
            "status": "success",
            "message_id": str(message.id),
            "requires_approval": message.requires_approval,
            "automation_policy": automation_policy.automation_type if automation_policy else None
        }
    
    async def send_message(
        self, 
        org_id: uuid.UUID, 
        message_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Send message via provider"""
        message = await self.message_repo.get_message_by_id(org_id, message_id)
        if not message:
            raise MessageNotFoundException(str(message_id))
        
        if message.requires_approval and not message.approved_by:
            raise AutomationPolicyException("Message requires approval before sending")
        
        # Update status to processing
        await self.message_repo.update_message_status(message_id, MessageStatus.PROCESSING)
        
        # Send via provider
        try:
            provider_result = await self.provider_service.send_via_provider(
                message.channel,
                {
                    "to": message.recipient_email if message.channel == CommunicationChannel.EMAIL else message.recipient_phone,
                    "subject": message.subject,
                    "body": message.body
                }
            )
            
            # Update status to sent
            await self.message_repo.update_message_status(message_id, MessageStatus.SENT)
            
            # Store provider message ID
            if provider_result.get("message_id"):
                # Would update provider_message_id
                pass
            
            return {
                "status": "success",
                "message": "Message sent successfully",
                "provider_message_id": provider_result.get("message_id")
            }
            
        except Exception as e:
            await self.message_repo.update_message_status(
                message_id, 
                MessageStatus.FAILED, 
                str(e)
            )
            raise ProviderException(message.channel, str(e))
    
    async def get_message_status(
        self, 
        org_id: uuid.UUID, 
        message_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Get message status"""
        message = await self.message_repo.get_message_by_id(org_id, message_id)
        if not message:
            raise MessageNotFoundException(str(message_id))
        
        return {
            "status": "success",
            "message_id": str(message.id),
            "current_status": message.status,
            "sent_at": message.sent_at.isoformat() if message.sent_at else None,
            "delivered_at": message.delivered_at.isoformat() if message.delivered_at else None,
            "read_at": message.read_at.isoformat() if message.read_at else None,
            "failure_reason": message.failure_reason,
            "retry_count": message.retry_count
        }
    
    async def check_automation_policy(
        self, 
        org_id: uuid.UUID, 
        notification_type: str
    ) -> Optional[AutomationPolicy]:
        """Check automation policy for notification type"""
        # Would use AutomationPolicyRepository
        return None


class ConversationService:
    """Service for conversation management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.conversation_repo = ConversationRepository(db)
        self.message_repo = MessageRepository(db)
    
    async def create_conversation(
        self, 
        org_id: uuid.UUID, 
        conversation_data: ConversationCreate
    ) -> Dict[str, Any]:
        """Create conversation"""
        ConversationValidator.validate_conversation_creation(conversation_data.model_dump())
        
        conversation_dict = conversation_data.model_dump()
        conversation = await self.conversation_repo.create_conversation(org_id, conversation_dict)
        
        return {
            "status": "success",
            "conversation_id": str(conversation.id),
            "message": "Conversation created successfully"
        }
    
    async def get_conversation(
        self, 
        org_id: uuid.UUID, 
        conversation_id: uuid.UUID
    ) -> Optional[Conversation]:
        """Get conversation by ID"""
        conversation = await self.conversation_repo.get_conversation_by_id(org_id, conversation_id)
        if not conversation:
            raise ConversationNotFoundException(str(conversation_id))
        return conversation
    
    async def send_message_to_conversation(
        self, 
        org_id: uuid.UUID, 
        message_data: MessageCreateForConversation
    ) -> Dict[str, Any]:
        """Send message to conversation"""
        conversation = await self.conversation_repo.get_conversation_by_id(
            org_id, 
            message_data.conversation_id
        )
        if not conversation:
            raise ConversationNotFoundException(str(message_data.conversation_id))
        
        message_dict = message_data.model_dump()
        message = await self.message_repo.create_message(message_dict)
        
        # Update conversation metadata
        conversation.message_count += 1
        conversation.last_message_at = datetime.now()
        await self.db.commit()
        
        return {
            "status": "success",
            "message_id": str(message.id),
            "message": "Message sent to conversation"
        }


class NotificationService:
    """Service for notification management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.notification_repo = NotificationRepository(db)
        self.preference_repo = NotificationPreferenceRepository(db)
    
    async def create_notification(
        self, 
        org_id: uuid.UUID, 
        notification_data: NotificationCreate
    ) -> Dict[str, Any]:
        """Create notification"""
        NotificationValidator.validate_notification_priority(notification_data.priority)
        NotificationValidator.validate_notification_channel(notification_data.channel)
        
        # Check user preferences
        user_preferences = await self.get_user_preferences(
            org_id,
            notification_data.recipient_id,
            notification_data.notification_type
        )
        
        # Check if channel is enabled for this notification type
        if not self.is_channel_enabled(user_preferences, notification_data.channel):
            raise Exception(f"Channel {notification_data.channel} is disabled for this notification type")
        
        notification_dict = notification_data.model_dump()
        notification_dict["organization_id"] = org_id
        notification = await self.notification_repo.create_notification(notification_dict)
        
        return {
            "status": "success",
            "notification_id": str(notification.id),
            "message": "Notification created successfully"
        }
    
    async def get_user_notifications(
        self, 
        org_id: uuid.UUID, 
        recipient_id: uuid.UUID,
        status: Optional[str] = None
    ) -> List[Notification]:
        """Get notifications for user"""
        return await self.notification_repo.get_notifications_by_recipient(
            org_id, 
            recipient_id, 
            status
        )
    
    def is_channel_enabled(
        self, 
        preferences: Optional[Dict[str, Any]], 
        channel: str
    ) -> bool:
        """Check if channel is enabled"""
        if not preferences:
            return True  # Default to enabled
        
        channel_map = {
            CommunicationChannel.EMAIL: "email_enabled",
            CommunicationChannel.SMS: "sms_enabled",
            CommunicationChannel.WHATSAPP: "whatsapp_enabled",
            CommunicationChannel.IN_APP: "in_app_enabled",
            CommunicationChannel.PUSH: "push_enabled"
        }
        
        return preferences.get(channel_map.get(channel, ""), True)


class NotificationPreferenceService:
    """Service for notification preference management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.preference_repo = NotificationPreferenceRepository(db)
    
    async def set_preference(
        self, 
        org_id: uuid.UUID, 
        preference_data: NotificationPreferenceCreate
    ) -> Dict[str, Any]:
        """Set notification preference"""
        preference_dict = preference_data.model_dump()
        preference_dict["organization_id"] = org_id
        preference = await self.preference_repo.upsert_preference(preference_dict)
        
        return {
            "status": "success",
            "preference_id": str(preference.id),
            "message": "Notification preference set successfully"
        }


class WebhookService:
    """Service for webhook management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.webhook_repo = WebhookRepository(db)
    
    async def create_webhook_config(
        self, 
        org_id: uuid.UUID, 
        webhook_data: WebhookConfigurationCreate
    ) -> Dict[str, Any]:
        """Create webhook configuration"""
        webhook_dict = webhook_data.model_dump()
        webhook_dict["organization_id"] = org_id
        webhook = await self.webhook_repo.create_webhook_config(webhook_dict)
        
        return {
            "status": "success",
            "webhook_id": str(webhook.id),
            "message": "Webhook configuration created successfully"
        }
    
    async def process_webhook(
        self, 
        webhook_id: uuid.UUID, 
        event_type: str, 
        payload: dict
    ) -> Dict[str, Any]:
        """Process incoming webhook"""
        # Log webhook
        log_data = {
            "webhook_config_id": webhook_id,
            "event_type": event_type,
            "payload": payload
        }
        log = await self.webhook_repo.log_webhook(log_data)
        
        # Process based on event type
        # This would trigger appropriate actions
        await self.webhook_repo.update_webhook_log_status(
            log.id, 
            "Processed"
        )
        
        return {
            "status": "success",
            "webhook_log_id": str(log.id),
            "message": "Webhook processed successfully"
        }


class ProviderService:
    """Service for provider abstraction"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def send_via_provider(
        self, 
        channel: str, 
        message_data: dict
    ) -> Dict[str, Any]:
        """Send message via appropriate provider"""
        if channel == CommunicationChannel.EMAIL:
            return await self._send_email(message_data)
        elif channel == CommunicationChannel.SMS:
            return await self._send_sms(message_data)
        elif channel == CommunicationChannel.WHATSAPP:
            return await self._send_whatsapp(message_data)
        else:
            raise Exception(f"Unsupported channel: {channel}")
    
    async def _send_email(self, message_data: dict) -> Dict[str, Any]:
        """Send email (placeholder for actual implementation)"""
        # Placeholder for actual email provider integration
        # Would use SendGrid, AWS SES, or similar
        return {
            "status": "success",
            "message_id": f"email_{uuid.uuid4()}",
            "provider": "email_provider_placeholder"
        }
    
    async def _send_sms(self, message_data: dict) -> Dict[str, Any]:
        """Send SMS (placeholder for actual implementation)"""
        # Placeholder for actual SMS provider integration
        # Would use Twilio, AWS SNS, or similar
        return {
            "status": "success",
            "message_id": f"sms_{uuid.uuid4()}",
            "provider": "sms_provider_placeholder"
        }
    
    async def _send_whatsapp(self, message_data: dict) -> Dict[str, Any]:
        """Send WhatsApp message (placeholder for actual implementation)"""
        # Placeholder for actual WhatsApp provider integration
        # Would use Twilio WhatsApp, WhatsApp Business API, or similar
        return {
            "status": "success",
            "message_id": f"whatsapp_{uuid.uuid4()}",
            "provider": "whatsapp_provider_placeholder"
        }