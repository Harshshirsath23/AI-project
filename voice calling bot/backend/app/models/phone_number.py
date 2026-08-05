from typing import Optional

from sqlalchemy import Uuid, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditMixin, BaseModel, SoftDeleteMixin


class PhoneNumber(BaseModel, AuditMixin, SoftDeleteMixin):
    """Phone number model for outbound and inbound calling."""

    __tablename__ = "phone_number"

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organization.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, index=True)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)  # twilio, telnyx, etc.
    status: Mapped[str] = mapped_column(
        String(50),
        default="active",
        nullable=False,
        index=True,
    )  # active, pending, released
    assigned_agent_id: Mapped[Optional[str]] = mapped_column(
        Uuid, ForeignKey("agent.id"), nullable=True, index=True
    )

    # Relationships
    assigned_agent: Mapped[Optional["Agent"]] = relationship("Agent")
