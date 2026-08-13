from typing import Optional
from datetime import datetime

from sqlalchemy import Uuid, String, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Call(BaseModel):
    """Call model representing an active or past phone conversation."""

    __tablename__ = "call"

    organization_id: Mapped[str] = mapped_column(
        Uuid,
        nullable=False,
        index=True,
    )
    agent_id: Mapped[str] = mapped_column(
        Uuid, ForeignKey("agent.id"), nullable=False, index=True
    )
    lead_id: Mapped[Optional[str]] = mapped_column(
        Uuid, ForeignKey("lead.id"), nullable=True, index=True
    )
    from_number: Mapped[str] = mapped_column(String(20), nullable=False, index=True)

    to_number: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    status: Mapped[str] = mapped_column(
        String(50),
        default="queued",
        nullable=False,
        index=True,
    )  # queued, in-progress, completed, failed, no-answer
    provider_call_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    
    transcript: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sentiment: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    started_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    ended_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    duration_seconds: Mapped[Optional[int]] = mapped_column(default=0, nullable=True)

    # Relationships
    agent: Mapped["Agent"] = relationship("Agent")
