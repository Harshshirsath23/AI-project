from sqlalchemy import Column, String, Integer, ForeignKey, Date, Float, TEXT, Boolean, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.models import Base, AuditMixin

from app.modules.communication.enums import (
    CommunicationChannel, MessageStatus, NotificationType,
    NotificationPriority, ConversationType, MessageDirection,
    WebhookEvent, WebhookStatus, AutomationPolicy
)


# ==================== Communication Templates ====================

class CommunicationTemplate(AuditMixin, Base):
    __tablename__ = "communication_templates"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    template_name: Mapped[str] = mapped_column(String(150))
    template_type: Mapped[str] = mapped_column(String(100))  # email, sms, whatsapp
    notification_type: Mapped[str] = mapped_column(String(100))  # interview_scheduled, offer_sent, etc.
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True)  # For email
    body: Mapped[str] = mapped_column(TEXT)  # Template body with {{variables}}
    variables: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # Available variables schema
    is_default: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)


# ==================== Message Queue ====================

class MessageQueue(AuditMixin, Base):
    __tablename__ = "message_queue"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    recipient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))  # User or candidate ID
    recipient_type: Mapped[str] = mapped_column(String(50))  # user, candidate
    recipient_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    recipient_phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    channel: Mapped[str] = mapped_column(SQLEnum(CommunicationChannel))
    notification_type: Mapped[str] = mapped_column(String(100))
    template_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("communication_templates.id"), nullable=True)
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True)
    body: Mapped[str] = mapped_column(TEXT)
    priority: Mapped[str] = mapped_column(SQLEnum(NotificationPriority), default=NotificationPriority.NORMAL)
    status: Mapped[str] = mapped_column(SQLEnum(MessageStatus), default=MessageStatus.QUEUED)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    failure_reason: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    max_retries: Mapped[int] = mapped_column(Integer, default=3)
    provider_message_id: Mapped[str | None] = mapped_column(String(255), nullable=True)  # External provider's message ID
    meta_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    conversation_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("conversations.id"), nullable=True)
    requires_approval: Mapped[bool] = mapped_column(default=False)
    approved_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


# ==================== Conversation Threads ====================

class Conversation(AuditMixin, Base):
    __tablename__ = "conversations"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    conversation_type: Mapped[str] = mapped_column(SQLEnum(ConversationType))
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))  # candidate_id, application_id, interview_id, offer_id
    entity_type: Mapped[str] = mapped_column(String(50))  # candidate, application, interview, offer
    subject: Mapped[str] = mapped_column(String(255))
    participants: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # List of participant IDs and roles
    status: Mapped[str] = mapped_column(String(50), default="Active")  # Active, Closed, Archived
    last_message_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    message_count: Mapped[int] = mapped_column(Integer, default=0)
    unread_count: Mapped[int] = mapped_column(Integer, default=0)


class Message(AuditMixin, Base):
    __tablename__ = "messages"
    conversation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("conversations.id"))
    sender_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    sender_type: Mapped[str] = mapped_column(String(50))  # user, candidate, system
    direction: Mapped[str] = mapped_column(SQLEnum(MessageDirection))
    content: Mapped[str] = mapped_column(TEXT)
    channel: Mapped[str] = mapped_column(SQLEnum(CommunicationChannel))
    is_read: Mapped[bool] = mapped_column(default=False)
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    attachments: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    meta_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    parent_message_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("messages.id"), nullable=True)


# ==================== Notifications ====================

class Notification(AuditMixin, Base):
    __tablename__ = "notifications"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    recipient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    recipient_type: Mapped[str] = mapped_column(String(50))  # user, candidate
    notification_type: Mapped[str] = mapped_column(String(100))
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(TEXT)
    channel: Mapped[str] = mapped_column(SQLEnum(CommunicationChannel))
    priority: Mapped[str] = mapped_column(SQLEnum(NotificationPriority), default=NotificationPriority.NORMAL)
    status: Mapped[str] = mapped_column(String(50), default="Unread")  # Unread, Read, Dismissed
    action_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    action_label: Mapped[str | None] = mapped_column(String(100), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    meta_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    related_entity_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    related_entity_type: Mapped[str | None] = mapped_column(String(50), nullable=True)


# ==================== Webhooks ====================

class WebhookConfiguration(AuditMixin, Base):
    __tablename__ = "webhook_configurations"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    provider: Mapped[str] = mapped_column(String(100))  # email_provider, sms_provider
    webhook_url: Mapped[str] = mapped_column(String(500))
    secret_key: Mapped[str] = mapped_column(String(255))  # For signature verification
    events: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # List of subscribed events
    is_active: Mapped[bool] = mapped_column(default=True)
    last_triggered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class WebhookLog(AuditMixin, Base):
    __tablename__ = "communication_webhook_logs"
    webhook_config_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("webhook_configurations.id"))
    event_type: Mapped[str] = mapped_column(String(100))
    payload: Mapped[dict] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(SQLEnum(WebhookStatus), default=WebhookStatus.RECEIVED)
    response_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    response_body: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    failure_reason: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)


# ==================== Notification Preferences ====================

class NotificationPreference(AuditMixin, Base):
    __tablename__ = "notification_preferences"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    notification_type: Mapped[str] = mapped_column(String(100))
    email_enabled: Mapped[bool] = mapped_column(default=True)
    in_app_enabled: Mapped[bool] = mapped_column(default=True)
    sms_enabled: Mapped[bool] = mapped_column(default=False)
    whatsapp_enabled: Mapped[bool] = mapped_column(default=False)
    push_enabled: Mapped[bool] = mapped_column(default=False)


# ==================== Automation Policies ====================

class AutomationPolicy(AuditMixin, Base):
    __tablename__ = "automation_policies"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    policy_name: Mapped[str] = mapped_column(String(150))
    notification_type: Mapped[str] = mapped_column(String(100))
    automation_type: Mapped[str] = mapped_column(SQLEnum(AutomationPolicy))
    conditions: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # When to apply this policy
    required_approval_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)


# ==================== Communication Audit ====================

class CommunicationAudit(AuditMixin, Base):
    __tablename__ = "communication_audits"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    action_type: Mapped[str] = mapped_column(String(100))
    entity_type: Mapped[str] = mapped_column(String(50))  # template, message, conversation, webhook
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    performed_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    details: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)