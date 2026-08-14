"""
TalentSphere Extended Schema Models
Models covering enterprise knowledge RAG, AI memory, cost tracking, prompt evaluations,
communication delivery logs, calendar/meeting integrations, and webhook subscriptions.
Fully conforms to PostgreSQL 17 + pgvector enterprise standard schema (291 tables).
"""

import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    String, Boolean, Integer, Float, DateTime, ForeignKey, Text, JSON, Enum, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base
from app.core.models import AuditMixin, VectorType


# ==========================================
# 1. AI Knowledge, RAG & Vector Intelligence
# ==========================================

class RagSession(AuditMixin, Base):
    __tablename__ = "rag_sessions"
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    query_text: Mapped[str] = mapped_column(Text)
    session_context: Mapped[Optional[dict]] = mapped_column(JSONB, default=dict)


class RagRetrievalResult(AuditMixin, Base):
    __tablename__ = "rag_retrieval_results"
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("rag_sessions.id", ondelete="CASCADE"), index=True)
    document_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    chunk_index: Mapped[int] = mapped_column(Integer, default=0)
    chunk_text: Mapped[str] = mapped_column(Text)
    similarity_score: Mapped[float] = mapped_column(Float, default=0.0)


class RagCitation(AuditMixin, Base):
    __tablename__ = "rag_citations"
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("rag_sessions.id", ondelete="CASCADE"), index=True)
    citation_title: Mapped[str] = mapped_column(String(255))
    citation_source_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    cited_content: Mapped[str] = mapped_column(Text)


class DocumentEmbedding(AuditMixin, Base):
    __tablename__ = "document_embeddings"
    document_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    chunk_index: Mapped[int] = mapped_column(Integer, default=0)
    chunk_content: Mapped[str] = mapped_column(Text)
    embedding = mapped_column(VectorType(1536), nullable=False)


class AiMemory(AuditMixin, Base):
    __tablename__ = "ai_memory"
    entity_type: Mapped[str] = mapped_column(String(50), index=True)  # 'CANDIDATE', 'JOB', 'CONVERSATION'
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    memory_key: Mapped[str] = mapped_column(String(100))
    memory_value: Mapped[str] = mapped_column(Text)
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class AiCostTracking(AuditMixin, Base):
    __tablename__ = "ai_cost_tracking"
    model_name: Mapped[str] = mapped_column(String(100), index=True)
    prompt_tokens: Mapped[int] = mapped_column(Integer, default=0)
    completion_tokens: Mapped[int] = mapped_column(Integer, default=0)
    total_tokens: Mapped[int] = mapped_column(Integer, default=0)
    estimated_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    execution_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)


class PromptEvaluation(AuditMixin, Base):
    __tablename__ = "prompt_evaluations"
    prompt_template_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    evaluation_dataset_name: Mapped[str] = mapped_column(String(150))
    accuracy_score: Mapped[float] = mapped_column(Float, default=0.0)
    hallucination_rate: Mapped[float] = mapped_column(Float, default=0.0)
    average_latency_ms: Mapped[int] = mapped_column(Integer, default=0)
    evaluation_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class PromptVariable(AuditMixin, Base):
    __tablename__ = "prompt_variables"
    prompt_template_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    variable_name: Mapped[str] = mapped_column(String(100))
    variable_type: Mapped[str] = mapped_column(String(50), default="string")
    default_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True)


# ==========================================
# 2. Calendar, Meetings & Collaboration
# ==========================================

class CalendarIntegration(AuditMixin, Base):
    __tablename__ = "calendar_integrations"
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    provider: Mapped[str] = mapped_column(String(50))  # 'GOOGLE_WORKSPACE', 'MICROSOFT_365', 'OUTLOOK'
    access_token_encrypted: Mapped[str] = mapped_column(Text)
    refresh_token_encrypted: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    calendar_id: Mapped[str] = mapped_column(String(255), default="primary")
    sync_status: Mapped[str] = mapped_column(String(50), default="ACTIVE")
    last_synced_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class CalendarEvent(AuditMixin, Base):
    __tablename__ = "calendar_events"
    integration_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("calendar_integrations.id", ondelete="CASCADE"))
    external_event_id: Mapped[str] = mapped_column(String(255), index=True)
    title: Mapped[str] = mapped_column(String(255))
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    meeting_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    interview_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)


class MeetingInvitation(AuditMixin, Base):
    __tablename__ = "meeting_invitations"
    calendar_event_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("calendar_events.id", ondelete="CASCADE"))
    attendee_email: Mapped[str] = mapped_column(String(255), index=True)
    attendee_role: Mapped[str] = mapped_column(String(50))  # 'CANDIDATE', 'INTERVIEWER', 'RECRUITER'
    response_status: Mapped[str] = mapped_column(String(50), default="NEEDS_ACTION")  # 'ACCEPTED', 'DECLINED', 'TENTATIVE'


# ==========================================
# 3. Communication Delivery & Granular Queues
# ==========================================

class CommunicationPreference(AuditMixin, Base):
    __tablename__ = "communication_preferences"
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True, index=True)
    email_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    sms_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    whatsapp_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    in_app_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    digest_frequency: Mapped[str] = mapped_column(String(30), default="INSTANT")


class EmailDeliveryLog(AuditMixin, Base):
    __tablename__ = "email_delivery_logs"
    message_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    recipient_email: Mapped[str] = mapped_column(String(255), index=True)
    provider: Mapped[str] = mapped_column(String(50), default="SENDGRID")
    provider_message_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    delivery_status: Mapped[str] = mapped_column(String(50), default="DELIVERED")
    opened_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    clicked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class SmsQueue(AuditMixin, Base):
    __tablename__ = "sms_queue"
    recipient_phone: Mapped[str] = mapped_column(String(30))
    message_body: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), default="QUEUED")  # QUEUED, SENT, FAILED
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class WhatsappQueue(AuditMixin, Base):
    __tablename__ = "whatsapp_queue"
    recipient_phone: Mapped[str] = mapped_column(String(30))
    template_name: Mapped[str] = mapped_column(String(100))
    template_parameters: Mapped[Optional[dict]] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(30), default="QUEUED")
    retry_count: Mapped[int] = mapped_column(Integer, default=0)


class PushNotification(AuditMixin, Base):
    __tablename__ = "push_notifications"
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    device_token: Mapped[str] = mapped_column(String(500))
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)
    data: Mapped[Optional[dict]] = mapped_column(JSONB, default=dict)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)


# ==========================================
# 4. Webhook Subscriptions & Deliveries
# ==========================================

class WebhookSubscription(AuditMixin, Base):
    __tablename__ = "webhook_subscriptions"
    endpoint_url: Mapped[str] = mapped_column(String(500))
    secret_token: Mapped[str] = mapped_column(String(255))
    subscribed_events: Mapped[List[str]] = mapped_column(JSONB, default=list)  # e.g. ["candidate.created", "offer.signed"]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class WebhookDelivery(AuditMixin, Base):
    __tablename__ = "webhook_deliveries"
    subscription_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("webhook_subscriptions.id", ondelete="CASCADE"), index=True)
    event_type: Mapped[str] = mapped_column(String(100))
    payload: Mapped[dict] = mapped_column(JSONB)
    response_status_code: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    response_body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    execution_time_ms: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(30), default="SUCCESS")  # SUCCESS, FAILED, RETRYING


# ==========================================
# 5. Evaluation Datasets & Human Review
# ==========================================

class EvaluationDataset(AuditMixin, Base):
    __tablename__ = "evaluation_datasets"
    dataset_name: Mapped[str] = mapped_column(String(150), unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sample_count: Mapped[int] = mapped_column(Integer, default=0)
    dataset_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class HumanReview(AuditMixin, Base):
    __tablename__ = "human_reviews"
    review_type: Mapped[str] = mapped_column(String(50))  # 'AI_DISQUALIFICATION', 'OFFER_LETTER', 'JOB_DESCRIPTION'
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    reviewer_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    decision: Mapped[str] = mapped_column(String(30))  # 'APPROVED', 'REJECTED', 'MODIFIED'
    review_comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reviewed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
