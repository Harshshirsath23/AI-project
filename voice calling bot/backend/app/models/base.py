from datetime import UTC, datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


class TimestampMixin:
    """Mixin for adding timestamp fields to models."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )


class SoftDeleteMixin:
    """Mixin for adding soft delete support to models."""

    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
    )


class AuditMixin:
    """Mixin for adding audit fields to models."""

    created_by: Mapped[Optional[UUID]] = mapped_column(nullable=True, index=True)
    updated_by: Mapped[Optional[UUID]] = mapped_column(nullable=True, index=True)


class BaseModel(Base, TimestampMixin):
    """Base model with UUID primary key and timestamps."""
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        nullable=False,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Generate table name from class name."""
        return cls.__name__.lower()

    def __repr__(self) -> str:
        """String representation of the model."""
        return f"<{self.__class__.__name__}(id={self.id})>"
