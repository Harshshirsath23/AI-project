"""Audit logger service and function decorators."""

import json
from functools import wraps
from typing import Any, Dict, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog
from app.core.logging import get_logger

logger = get_logger(__name__)


class AuditLogger:
    """Audit logger helper for persisting security and administrative action logs."""

    @staticmethod
    async def log_event(
        db: AsyncSession,
        resource_type: str,
        action: str,
        organization_id: Optional[Union[str, UUID]] = None,
        user_id: Optional[Union[str, UUID]] = None,
        resource_id: Optional[str] = None,
        changes: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        status: str = "success",
        error_message: Optional[str] = None,
    ) -> Optional[AuditLog]:
        """Record an audit log entry."""
        try:
            org_uuid = UUID(str(organization_id)) if organization_id else None
            user_uuid = UUID(str(user_id)) if user_id else None

            audit = AuditLog(
                organization_id=org_uuid,
                user_id=user_uuid,
                resource_type=resource_type,
                resource_id=str(resource_id) if resource_id else None,
                action=action,
                changes=json.dumps(changes) if changes else None,
                ip_address=ip_address,
                user_agent=user_agent,
                status=status,
                error_message=error_message,
            )
            db.add(audit)
            await db.commit()
            return audit
        except Exception as e:
            logger.error("Failed to persist audit log", error=str(e))
            return None

    @staticmethod
    def log_guardrail_violation(
        call_id: str,
        violation_type: str,
        detail: str,
        severity: str = "warning",
    ):
        """Record a synchronous guardrail violation log to DB / structlog."""
        logger.warning(
            "Guardrail Violation Logged",
            call_id=call_id,
            type=violation_type,
            detail=detail,
            severity=severity,
        )
        try:
            from app.database.connection import SessionLocal

            with SessionLocal() as db:
                audit = AuditLog(
                    resource_type="guardrail",
                    resource_id=call_id,
                    action=f"violation_{violation_type}",
                    changes=json.dumps({"detail": detail, "severity": severity}),
                    status="warning",
                    error_message=detail,
                )
                db.add(audit)
                db.commit()
        except Exception as e:
            logger.error("Failed to persist sync guardrail audit log", error=str(e))


def audit_action(resource_type: str, action: str):
    """Decorator to automatically record audit event on endpoint execution."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                logger.warning(
                    "Audited function failed",
                    resource_type=resource_type,
                    action=action,
                    error=str(e),
                )
                raise
        return wrapper
    return decorator
