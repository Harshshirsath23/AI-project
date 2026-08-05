from typing import Optional

from sqlalchemy import Uuid, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditMixin, BaseModel, SoftDeleteMixin



class Organization(BaseModel, AuditMixin, SoftDeleteMixin):
    """Organization model representing a company using the platform."""

    __tablename__ = "organization"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    company_size: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False, index=True)

    # Relationships
    settings: Mapped["OrganizationSettings"] = relationship(
        "OrganizationSettings",
        back_populates="organization",
        uselist=False,
        cascade="all, delete-orphan",
    )
    users: Mapped[list["User"]] = relationship(
        "User",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    agents: Mapped[list["Agent"]] = relationship(
        "Agent",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    campaigns: Mapped[list["Campaign"]] = relationship(
        "Campaign",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    knowledge_bases: Mapped[list["KnowledgeBase"]] = relationship(
        "KnowledgeBase",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    prompts: Mapped[list["Prompt"]] = relationship(
        "Prompt",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    provider_configs: Mapped[list["AIProviderConfig"]] = relationship(
        "AIProviderConfig",
        back_populates="organization",
        cascade="all, delete-orphan",
    )


class OrganizationSettings(BaseModel, AuditMixin):
    """Organization-specific settings and preferences."""

    __tablename__ = "organization_settings"

    organization_id: Mapped[str] = mapped_column(

        ForeignKey("organization.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    timezone: Mapped[str] = mapped_column(String(50), default="UTC", nullable=False)
    locale: Mapped[str] = mapped_column(String(10), default="en-US", nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    default_language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    max_concurrent_calls: Mapped[int] = mapped_column(default=10, nullable=False)
    call_recording_enabled: Mapped[bool] = mapped_column(default=True, nullable=False)
    auto_transcription_enabled: Mapped[bool] = mapped_column(default=True, nullable=False)
    retention_days: Mapped[int] = mapped_column(default=90, nullable=False)
    custom_branding_enabled: Mapped[bool] = mapped_column(default=False, nullable=False)
    api_rate_limit: Mapped[int] = mapped_column(default=1000, nullable=False)

    # Relationships
    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="settings",
    )
