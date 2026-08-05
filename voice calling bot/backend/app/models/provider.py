from typing import Optional

from sqlalchemy import Uuid, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditMixin, BaseModel, SoftDeleteMixin


class AIProviderConfig(BaseModel, AuditMixin, SoftDeleteMixin):
    """AI Provider Configuration model for storing provider-specific settings."""

    __tablename__ = "ai_provider_config"

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organization.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    provider_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )  # llm, stt, tts
    provider_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )  # gemini, whisper, sarvam, nemotron, piper
    config_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    is_default: Mapped[bool] = mapped_column(default=False, nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False, index=True)
    api_key: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    api_endpoint: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    model_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    region: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    priority: Mapped[int] = mapped_column(default=10, nullable=False, index=True)  # Lower is higher priority
    rate_limit_per_minute: Mapped[int] = mapped_column(default=60, nullable=False)
    timeout_seconds: Mapped[int] = mapped_column(default=30, nullable=False)
    retry_count: Mapped[int] = mapped_column(default=3, nullable=False)
    config: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON for provider-specific settings
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="provider_configs",
    )
