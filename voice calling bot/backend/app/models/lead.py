from typing import Optional

from sqlalchemy import Uuid, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditMixin, BaseModel, SoftDeleteMixin


class Lead(BaseModel, AuditMixin, SoftDeleteMixin):
    """Lead model for campaign targets."""

    __tablename__ = "lead"

    organization_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("organization.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    campaign_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("campaign.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    agent_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("agent.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )


    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    company: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    timezone: Mapped[str] = mapped_column(String(50), default="UTC", nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # csv, manual, api, etc.
    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False,
        index=True,
    )  # pending, queued, calling, answered, voicemail, busy, no_answer, completed, failed, rejected, callback_requested, interested, not_interested, qualified, converted
    job_title: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    custom_fields: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON for custom fields
    call_attempts: Mapped[int] = mapped_column(default=0, nullable=False)
    retry_count: Mapped[int] = mapped_column(default=0, nullable=False)
    last_call_at: Mapped[Optional[str]] = mapped_column(Uuid, nullable=True)
    next_call_at: Mapped[Optional[str]] = mapped_column(Uuid, nullable=True, index=True)
    priority: Mapped[int] = mapped_column(default=5, nullable=False, index=True)  # 1-10, higher is more important
    final_disposition: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)

    # Relationships
    campaign: Mapped["Campaign"] = relationship(
        "Campaign",
        back_populates="leads",
    )
