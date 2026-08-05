from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import Uuid, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditMixin, BaseModel, SoftDeleteMixin


class OrganizationInvitation(BaseModel, AuditMixin, SoftDeleteMixin):
    """Organization invitation model for inviting users to join organizations."""

    __tablename__ = "organization_invitation"

    organization_id: Mapped[str] = mapped_column(
        Uuid,
        nullable=False,
        index=True,
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    role_id: Mapped[str] = mapped_column(Uuid, nullable=False, index=True)
    token: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False,
        index=True,
    )  # pending, accepted, declined, expired
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    invited_by: Mapped[str] = mapped_column(Uuid, nullable=False)  # User ID
    expires_at: Mapped[datetime] = mapped_column(nullable=False, index=True)
    accepted_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    declined_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    # Relationships
    # Note: These will be added when we update the models to include back_populates
