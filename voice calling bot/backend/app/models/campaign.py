from datetime import time
from typing import Optional

from sqlalchemy import Uuid, Integer, String, Text, Time, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditMixin, BaseModel, SoftDeleteMixin


class Campaign(BaseModel, AuditMixin, SoftDeleteMixin):
    """Campaign model for outbound calling campaigns."""

    __tablename__ = "campaign"

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organization.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    agent_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("agent.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    agent_ids: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)  # Store list of agent IDs
    phone_numbers: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)  # Store list of phone numbers
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    campaign_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )  # outbound, inbound, blended
    status: Mapped[str] = mapped_column(
        String(50),
        default="draft",
        nullable=False,
        index=True,
    )  # draft, scheduled, running, paused, completed, cancelled
    start_date: Mapped[Optional[str]] = mapped_column(Uuid, nullable=True, index=True)
    end_date: Mapped[Optional[str]] = mapped_column(Uuid, nullable=True, index=True)
    calling_window_start: Mapped[time] = mapped_column(
        Time,
        default=time(9, 0),
        nullable=False,
    )
    calling_window_end: Mapped[time] = mapped_column(
        Time,
        default=time(17, 0),
        nullable=False,
    )
    calling_timezone: Mapped[str] = mapped_column(String(50), default="UTC", nullable=False)
    max_concurrent_calls: Mapped[int] = mapped_column(default=5, nullable=False)
    retry_count: Mapped[int] = mapped_column(default=3, nullable=False)
    retry_delay_minutes: Mapped[int] = mapped_column(default=30, nullable=False)
    call_duration_limit_seconds: Mapped[int] = mapped_column(default=300, nullable=False)
    total_leads: Mapped[int] = mapped_column(default=0, nullable=False)
    completed_calls: Mapped[int] = mapped_column(default=0, nullable=False)
    successful_calls: Mapped[int] = mapped_column(default=0, nullable=False)
    failed_calls: Mapped[int] = mapped_column(default=0, nullable=False)
    success_rate: Mapped[float] = mapped_column(default=0.0, nullable=False)
    priority: Mapped[int] = mapped_column(default=5, nullable=False, index=True)  # 1-10, higher is more important
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="campaigns",
    )
    leads: Mapped[list["Lead"]] = relationship(
        "Lead",
        back_populates="campaign",
        cascade="all, delete-orphan",
    )
