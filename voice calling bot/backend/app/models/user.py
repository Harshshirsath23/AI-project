from typing import Optional

from sqlalchemy import Uuid, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditMixin, BaseModel, SoftDeleteMixin


class Role(BaseModel, AuditMixin):
    """Role model for user permissions and access control."""

    __tablename__ = "role"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    permissions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of permissions
    is_system: Mapped[bool] = mapped_column(default=False, nullable=False)  # System roles cannot be deleted

    # Relationships
    users: Mapped[list["User"]] = relationship(
        "User",
        back_populates="role",
        cascade="all, delete-orphan",
    )


class User(BaseModel, AuditMixin, SoftDeleteMixin):
    """User model representing platform users."""

    __tablename__ = "user"

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organization.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("role.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    job_title: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    timezone: Mapped[str] = mapped_column(String(50), default="UTC", nullable=False)
    locale: Mapped[str] = mapped_column(String(10), default="en-US", nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False, index=True)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    last_login_at: Mapped[Optional[str]] = mapped_column(Uuid, nullable=True)

    # Relationships
    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="users",
    )
    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="users",
    )
