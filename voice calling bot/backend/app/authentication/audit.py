from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import AuditMixin, BaseModel


class SecurityAuditLog(BaseModel, AuditMixin):
    """Security audit log for tracking security-related events."""

    __tablename__ = "security_audit_log"

    user_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True, index=True)
    organization_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True, index=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    event_category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )  # authentication, authorization, data_access, configuration
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)  # IPv6 compatible
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    resource_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    resource_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False)  # create, read, update, delete, login, logout
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)  # success, failure, warning
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON for additional details
    failure_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class AuditLogger:
    """Audit logger for security events."""

    def __init__(self):
        self._enabled = True

    async def log_event(
        self,
        db,
        event_type: str,
        event_category: str,
        action: str,
        status: str,
        user_id: Optional[str] = None,
        organization_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Optional[dict] = None,
        failure_reason: Optional[str] = None,
    ):
        """
        Log a security event to the audit log.
        
        Args:
            db: Database session
            event_type: Type of event (e.g., "user_login", "permission_denied")
            event_category: Category of event (authentication, authorization, data_access, configuration)
            action: Action performed (create, read, update, delete, login, logout)
            status: Status of event (success, failure, warning)
            user_id: ID of the user (if applicable)
            organization_id: ID of the organization (if applicable)
            ip_address: IP address of the request
            user_agent: User agent string
            resource_type: Type of resource affected
            resource_id: ID of resource affected
            details: Additional details as dict
            failure_reason: Reason for failure (if applicable)
        """
        if not self._enabled:
            return

        import json

        audit_log = SecurityAuditLog(
            user_id=user_id,
            organization_id=organization_id,
            event_type=event_type,
            event_category=event_category,
            ip_address=ip_address,
            user_agent=user_agent,
            resource_type=resource_type,
            resource_id=resource_id,
            action=action,
            status=status,
            details=json.dumps(details) if details else None,
            failure_reason=failure_reason,
        )

        db.add(audit_log)
        # Note: Commit should be handled by the caller or in a transaction


# Global audit logger instance
audit_logger = AuditLogger()


def log_authentication_event(
    event_type: str,
    status: str,
    user_id: Optional[str] = None,
    organization_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    failure_reason: Optional[str] = None,
):
    """
    Helper function to log authentication events.
    
    Args:
        event_type: Type of auth event (user_login, user_logout, token_refresh, etc.)
        status: Status (success, failure)
        user_id: User ID
        organization_id: Organization ID
        ip_address: IP address
        user_agent: User agent
        failure_reason: Reason for failure
    """
    from app.core.logging import get_logger

    logger = get_logger(__name__)

    # Log to application logger
    log_data = {
        "event_type": event_type,
        "status": status,
        "user_id": user_id,
        "organization_id": organization_id,
        "ip_address": ip_address,
    }

    if status == "success":
        logger.info("Authentication event", **log_data)
    else:
        logger.warning("Authentication event failed", failure_reason=failure_reason, **log_data)

    # Note: Database audit logging would be done in the service layer
    # where we have access to the database session


def log_authorization_event(
    event_type: str,
    status: str,
    user_id: str,
    organization_id: str,
    resource_type: str,
    resource_id: Optional[str] = None,
    action: str = "access",
    failure_reason: Optional[str] = None,
):
    """
    Helper function to log authorization events.
    
    Args:
        event_type: Type of authz event (permission_check, role_check, etc.)
        status: Status (success, failure)
        user_id: User ID
        organization_id: Organization ID
        resource_type: Type of resource
        resource_id: Resource ID
        action: Action being performed
        failure_reason: Reason for failure
    """
    from app.core.logging import get_logger

    logger = get_logger(__name__)

    log_data = {
        "event_type": event_type,
        "status": status,
        "user_id": user_id,
        "organization_id": organization_id,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "action": action,
    }

    if status == "success":
        logger.info("Authorization event", **log_data)
    else:
        logger.warning("Authorization event failed", failure_reason=failure_reason, **log_data)


def log_data_access_event(
    event_type: str,
    user_id: str,
    organization_id: str,
    resource_type: str,
    resource_id: Optional[str] = None,
    action: str = "read",
    details: Optional[dict] = None,
):
    """
    Helper function to log data access events.
    
    Args:
        event_type: Type of data access event
        user_id: User ID
        organization_id: Organization ID
        resource_type: Type of resource
        resource_id: Resource ID
        action: Action performed
        details: Additional details
    """
    from app.core.logging import get_logger

    logger = get_logger(__name__)

    logger.info(
        "Data access event",
        event_type=event_type,
        user_id=user_id,
        organization_id=organization_id,
        resource_type=resource_type,
        resource_id=resource_id,
        action=action,
        details=details,
    )
