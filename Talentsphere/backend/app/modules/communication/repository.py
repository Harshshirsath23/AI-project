from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, update, delete
from sqlalchemy.orm import selectinload
import uuid
from datetime import datetime

from app.modules.communication.models import (
    CommunicationTemplate, MessageQueue, Conversation, Message,
    Notification, WebhookConfiguration, WebhookLog,
    NotificationPreference, AutomationPolicy, CommunicationAudit
)
from app.modules.communication.enums import MessageStatus, WebhookStatus


class TemplateRepository:
    """Repository for communication template operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_template(
        self, 
        org_id: uuid.UUID, 
        template_data: dict
    ) -> CommunicationTemplate:
        """Create communication template"""
        template = CommunicationTemplate(
            organization_id=org_id,
            template_name=template_data["template_name"],
            template_type=template_data["template_type"],
            notification_type=template_data["notification_type"],
            subject=template_data.get("subject"),
            body=template_data["body"],
            variables=template_data.get("variables"),
            is_default=template_data.get("is_default", False)
        )
        self.db.add(template)
        await self.db.commit()
        return template
    
    async def get_template_by_id(
        self, 
        org_id: uuid.UUID, 
        template_id: uuid.UUID
    ) -> Optional[CommunicationTemplate]:
        """Get template by ID"""
        query = select(CommunicationTemplate).where(
            and_(
                CommunicationTemplate.id == template_id,
                CommunicationTemplate.organization_id == org_id
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_templates_by_type(
        self, 
        org_id: uuid.UUID, 
        template_type: str,
        notification_type: str
    ) -> Optional[CommunicationTemplate]:
        """Get default template by type"""
        query = select(CommunicationTemplate).where(
            and_(
                CommunicationTemplate.organization_id == org_id,
                CommunicationTemplate.template_type == template_type,
                CommunicationTemplate.notification_type == notification_type,
                CommunicationTemplate.is_default == True,
                CommunicationTemplate.is_active == True
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


class MessageQueueRepository:
    """Repository for message queue operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_message(
        self, 
        message_data: dict
    ) -> MessageQueue:
        """Create message in queue"""
        message = MessageQueue(
            organization_id=message_data["organization_id"],
            recipient_id=message_data["recipient_id"],
            recipient_type=message_data["recipient_type"],
            recipient_email=message_data.get("recipient_email"),
            recipient_phone=message_data.get("recipient_phone"),
            channel=message_data["channel"],
            notification_type=message_data["notification_type"],
            template_id=message_data.get("template_id"),
            subject=message_data.get("subject"),
            body=message_data["body"],
            priority=message_data.get("priority", "Normal"),
            scheduled_at=message_data.get("scheduled_at"),
            metadata=message_data.get("metadata"),
            conversation_id=message_data.get("conversation_id"),
            requires_approval=message_data.get("requires_approval", False)
        )
        self.db.add(message)
        await self.db.commit()
        return message
    
    async def get_message_by_id(
        self, 
        org_id: uuid.UUID, 
        message_id: uuid.UUID
    ) -> Optional[MessageQueue]:
        """Get message by ID"""
        query = select(MessageQueue).where(
            and_(
                MessageQueue.id == message_id,
                MessageQueue.organization_id == org_id
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_message_status(
        self, 
        message_id: uuid.UUID, 
        new_status: str,
        failure_reason: Optional[str] = None
    ) -> None:
        """Update message status"""
        update_data = {"status": new_status}
        
        if new_status == MessageStatus.SENT:
            update_data["sent_at"] = datetime.now()
        elif new_status == MessageStatus.DELIVERED:
            update_data["delivered_at"] = datetime.now()
        elif new_status == MessageStatus.READ:
            update_data["read_at"] = datetime.now()
        elif new_status == MessageStatus.FAILED:
            update_data["failure_reason"] = failure_reason
        
        query = update(MessageQueue).where(
            MessageQueue.id == message_id
        ).values(**update_data)
        await self.db.execute(query)
        await self.db.commit()
    
    async def increment_retry_count(
        self, 
        message_id: uuid.UUID
    ) -> None:
        """Increment message retry count"""
        query = update(MessageQueue).where(
            MessageQueue.id == message_id
        ).values(retry_count=MessageQueue.retry_count + 1)
        await self.db.execute(query)
        await self.db.commit()


class ConversationRepository:
    """Repository for conversation operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_conversation(
        self, 
        org_id: uuid.UUID, 
        conversation_data: dict
    ) -> Conversation:
        """Create conversation"""
        conversation = Conversation(
            organization_id=org_id,
            conversation_type=conversation_data["conversation_type"],
            entity_id=conversation_data["entity_id"],
            entity_type=conversation_data["entity_type"],
            subject=conversation_data["subject"],
            participants=conversation_data.get("participants")
        )
        self.db.add(conversation)
        await self.db.commit()
        return conversation
    
    async def get_conversation_by_id(
        self, 
        org_id: uuid.UUID, 
        conversation_id: uuid.UUID
    ) -> Optional[Conversation]:
        """Get conversation by ID"""
        query = select(Conversation).where(
            and_(
                Conversation.id == conversation_id,
                Conversation.organization_id == org_id
            )
        ).options(selectinload(Conversation.messages))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_conversations_by_entity(
        self, 
        org_id: uuid.UUID, 
        entity_id: uuid.UUID,
        entity_type: str
    ) -> List[Conversation]:
        """Get conversations by entity"""
        query = select(Conversation).where(
            and_(
                Conversation.organization_id == org_id,
                Conversation.entity_id == entity_id,
                Conversation.entity_type == entity_type
            )
        ).order_by(Conversation.updated_at.desc())
        result = await self.db.execute(query)
        return result.scalars().all()


class MessageRepository:
    """Repository for message operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_message(
        self, 
        message_data: dict
    ) -> Message:
        """Create message"""
        message = Message(
            conversation_id=message_data["conversation_id"],
            sender_id=message_data["sender_id"],
            sender_type=message_data["sender_type"],
            direction=message_data["direction"],
            content=message_data["content"],
            channel=message_data.get("channel", "In-App"),
            attachments=message_data.get("attachments"),
            metadata=message_data.get("metadata"),
            parent_message_id=message_data.get("parent_message_id")
        )
        self.db.add(message)
        await self.db.commit()
        return message
    
    async def get_messages_by_conversation(
        self, 
        conversation_id: uuid.UUID
    ) -> List[Message]:
        """Get messages by conversation"""
        query = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc())
        result = await self.db.execute(query)
        return result.scalars().all()


class NotificationRepository:
    """Repository for notification operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_notification(
        self, 
        notification_data: dict
    ) -> Notification:
        """Create notification"""
        notification = Notification(
            organization_id=notification_data["organization_id"],
            recipient_id=notification_data["recipient_id"],
            recipient_type=notification_data["recipient_type"],
            notification_type=notification_data["notification_type"],
            title=notification_data["title"],
            body=notification_data["body"],
            channel=notification_data["channel"],
            priority=notification_data.get("priority", "Normal"),
            action_url=notification_data.get("action_url"),
            action_label=notification_data.get("action_label"),
            expires_at=notification_data.get("expires_at"),
            metadata=notification_data.get("metadata"),
            related_entity_id=notification_data.get("related_entity_id"),
            related_entity_type=notification_data.get("related_entity_type")
        )
        self.db.add(notification)
        await self.db.commit()
        return notification
    
    async def get_notifications_by_recipient(
        self, 
        org_id: uuid.UUID, 
        recipient_id: uuid.UUID,
        status: Optional[str] = None
    ) -> List[Notification]:
        """Get notifications by recipient"""
        conditions = [
            Notification.organization_id == org_id,
            Notification.recipient_id == recipient_id
        ]
        
        if status:
            conditions.append(Notification.status == status)
        
        query = select(Notification).where(
            and_(*conditions)
        ).order_by(Notification.created_at.desc())
        result = await self.db.execute(query)
        return result.scalars().all()


class NotificationPreferenceRepository:
    """Repository for notification preference operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def upsert_preference(
        self, 
        preference_data: dict
    ) -> NotificationPreference:
        """Upsert notification preference"""
        # Check if exists
        query = select(NotificationPreference).where(
            and_(
                NotificationPreference.organization_id == preference_data["organization_id"],
                NotificationPreference.user_id == preference_data["user_id"],
                NotificationPreference.notification_type == preference_data["notification_type"]
            )
        )
        result = await self.db.execute(query)
        existing = result.scalar_one_or_none()
        
        if existing:
            # Update
            for key, value in preference_data.items():
                if key not in ["organization_id", "user_id", "notification_type"]:
                    setattr(existing, key, value)
            await self.db.commit()
            return existing
        else:
            # Create
            preference = NotificationPreference(**preference_data)
            self.db.add(preference)
            await self.db.commit()
            return preference


class WebhookRepository:
    """Repository for webhook operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_webhook_config(
        self, 
        webhook_data: dict
    ) -> WebhookConfiguration:
        """Create webhook configuration"""
        webhook = WebhookConfiguration(
            organization_id=webhook_data["organization_id"],
            provider=webhook_data["provider"],
            webhook_url=webhook_data["webhook_url"],
            secret_key=webhook_data["secret_key"],
            events={"events": webhook_data["events"]}
        )
        self.db.add(webhook)
        await self.db.commit()
        return webhook
    
    async def log_webhook(
        self, 
        webhook_log_data: dict
    ) -> WebhookLog:
        """Log webhook event"""
        log = WebhookLog(
            webhook_config_id=webhook_log_data["webhook_config_id"],
            event_type=webhook_log_data["event_type"],
            payload=webhook_log_data["payload"],
            status=WebhookStatus.RECEIVED
        )
        self.db.add(log)
        await self.db.commit()
        return log
    
    async def update_webhook_log_status(
        self, 
        log_id: uuid.UUID, 
        status: str,
        response_code: Optional[int] = None,
        response_body: Optional[str] = None,
        failure_reason: Optional[str] = None
    ) -> None:
        """Update webhook log status"""
        update_data = {"status": status}
        
        if status == WebhookStatus.PROCESSED:
            update_data["processed_at"] = datetime.now()
        
        if response_code:
            update_data["response_code"] = response_code
        if response_body:
            update_data["response_body"] = response_body
        if failure_reason:
            update_data["failure_reason"] = failure_reason
        
        query = update(WebhookLog).where(
            WebhookLog.id == log_id
        ).values(**update_data)
        await self.db.execute(query)
        await self.db.commit()


class AutomationPolicyRepository:
    """Repository for automation policy operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_policy(
        self, 
        policy_data: dict
    ) -> AutomationPolicy:
        """Create automation policy"""
        policy = AutomationPolicy(
            organization_id=policy_data["organization_id"],
            policy_name=policy_data["policy_name"],
            notification_type=policy_data["notification_type"],
            automation_type=policy_data["automation_type"],
            conditions=policy_data.get("conditions"),
            required_approval_level=policy_data.get("required_approval_level")
        )
        self.db.add(policy)
        await self.db.commit()
        return policy
    
    async def get_policy_by_notification_type(
        self, 
        org_id: uuid.UUID, 
        notification_type: str
    ) -> Optional[AutomationPolicy]:
        """Get automation policy by notification type"""
        query = select(AutomationPolicy).where(
            and_(
                AutomationPolicy.organization_id == org_id,
                AutomationPolicy.notification_type == notification_type,
                AutomationPolicy.is_active == True
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()