from typing import Optional

from sqlalchemy import Uuid, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import AuditMixin, BaseModel


class SecurityAuditLog(BaseModel, AuditMixin):
    """Security audit log for tracking security-related events."""

    __tablename__ = "security_audit_log"

    user_id: Mapped[Optional[str]] = mapped_column(Uuid, nullable=True, index=True)
    organization_id: Mapped[Optional[str]] = mapped_column(Uuid, nullable=True, index=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    event_category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )  # authentication, authorization, data_access, configuration
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)  # IPv6 compatible
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    resource_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    resource_id: Mapped[Optional[str]] = mapped_column(Uuid, nullable=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False)  # create, read, update, delete, login, logout
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)  # success, failure, warning
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON for additional details
    failure_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
