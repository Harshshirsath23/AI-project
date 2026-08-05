from typing import Optional

from sqlalchemy import Uuid, Float, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditMixin, BaseModel, SoftDeleteMixin


class Agent(BaseModel, AuditMixin, SoftDeleteMixin):
    """AI Agent model representing voice agents."""

    __tablename__ = "agent"

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organization.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50),
        default="draft",
        nullable=False,
        index=True,
    )  # draft, active, paused, archived
    default_language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    default_voice: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    llm_provider: Mapped[str] = mapped_column(String(50), default="gemini", nullable=False)  # gemini, nemotron, etc.
    stt_provider: Mapped[str] = mapped_column(String(50), default="whisper", nullable=False)  # whisper, sarvam, etc.
    tts_provider: Mapped[str] = mapped_column(String(50), default="gtts", nullable=False)  # gtts, piper, sarvam, etc.
    temperature: Mapped[float] = mapped_column(Float, default=0.7, nullable=False)
    max_tokens: Mapped[int] = mapped_column(default=1000, nullable=False)
    personality: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    speaking_speed: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    greeting_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    system_prompt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    conversation_script: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    outbound_phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, index=True)
    knowledge_base_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("knowledge_base.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(default=False, nullable=False, index=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)


    # Relationships
    organization: Mapped["Organization"] = relationship(
        "Organization",
        foreign_keys=[organization_id],
        back_populates="agents",
    )

    voice_profile: Mapped["AgentVoiceProfile"] = relationship(
        "AgentVoiceProfile",
        back_populates="agent",
        uselist=False,
        cascade="all, delete-orphan",
    )
    configuration: Mapped["AgentConfiguration"] = relationship(
        "AgentConfiguration",
        back_populates="agent",
        uselist=False,
        cascade="all, delete-orphan",
    )


class AgentVoiceProfile(BaseModel, AuditMixin):
    """Agent voice profile for TTS configuration."""

    __tablename__ = "agent_voice_profile"

    agent_id: Mapped[str] = mapped_column(
        ForeignKey("agent.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    voice_id: Mapped[str] = mapped_column(String(100), nullable=False)
    voice_name: Mapped[str] = mapped_column(String(255), nullable=False)
    voice_gender: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    voice_age: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    voice_accent: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    pitch: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    speed: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    volume: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    emotion: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    custom_settings: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON for provider-specific settings

    # Relationships
    agent: Mapped["Agent"] = relationship(
        "Agent",
        foreign_keys=[agent_id],
        back_populates="voice_profile",
    )


class AgentConfiguration(BaseModel, AuditMixin):
    """Agent configuration for behavior and capabilities."""

    __tablename__ = "agent_configuration"

    agent_id: Mapped[str] = mapped_column(
        ForeignKey("agent.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    interruption_allowed: Mapped[bool] = mapped_column(default=True, nullable=False)
    interruption_threshold: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)
    silence_timeout: Mapped[int] = mapped_column(default=3000, nullable=False)  # milliseconds
    max_response_length: Mapped[int] = mapped_column(default=500, nullable=False)  # characters
    enable_sentiment_analysis: Mapped[bool] = mapped_column(default=True, nullable=False)
    enable_entity_extraction: Mapped[bool] = mapped_column(default=True, nullable=False)
    enable_call_summarization: Mapped[bool] = mapped_column(default=True, nullable=False)
    fallback_behavior: Mapped[str] = mapped_column(String(50), default="transfer", nullable=False)
    transfer_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    custom_intents: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON for custom intents
    knowledge_base_ids: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array of KB IDs
    prompt_template_id: Mapped[Optional[str]] = mapped_column(Uuid, nullable=True, index=True)

    # Relationships
    agent: Mapped["Agent"] = relationship(
        "Agent",
        back_populates="configuration",
    )
