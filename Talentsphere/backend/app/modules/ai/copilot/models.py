from sqlalchemy import Column, String, ForeignKey, TEXT, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.models import Base, AuditMixin


class CopilotConversation(AuditMixin, Base):
    __tablename__ = "copilot_conversations"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)


class CopilotMessage(AuditMixin, Base):
    __tablename__ = "copilot_messages"
    conversation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("copilot_conversations.id"))
    role: Mapped[str] = mapped_column(String(50)) # user, assistant, system, tool
    content: Mapped[str] = mapped_column(TEXT)
    meta_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class CopilotExecutionContext(AuditMixin, Base):
    __tablename__ = "copilot_execution_context"
    conversation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("copilot_conversations.id"))
    execution_id: Mapped[str] = mapped_column(String(100), unique=True)
    intent: Mapped[str | None] = mapped_column(String(100), nullable=True)
    intent_confidence: Mapped[float | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(String(50)) # running, hitl_blocked, completed, failed
    final_response: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class CopilotToolCall(AuditMixin, Base):
    __tablename__ = "copilot_tool_calls"
    execution_context_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("copilot_execution_context.id"))
    tool_name: Mapped[str] = mapped_column(String(150))
    arguments: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String(50)) # success, error


class CopilotPreference(AuditMixin, Base):
    __tablename__ = "copilot_preferences"
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    preferences: Mapped[dict] = mapped_column(JSON)
