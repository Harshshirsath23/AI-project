from typing import Optional

from sqlalchemy import Uuid, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditMixin, BaseModel, SoftDeleteMixin


class Prompt(BaseModel, AuditMixin, SoftDeleteMixin):
    """Prompt model for AI prompt templates."""

    __tablename__ = "prompt"

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organization.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    prompt_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )  # system, user, assistant, function
    base_template: Mapped[str] = mapped_column(Text, nullable=False)
    variables: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array of variable names
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False, index=True)
    current_version: Mapped[int] = mapped_column(default=1, nullable=False)
    tags: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array of tags

    # Relationships
    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="prompts",
    )
    versions: Mapped[list["PromptVersion"]] = relationship(
        "PromptVersion",
        back_populates="prompt",
        cascade="all, delete-orphan",
        order_by="PromptVersion.version_number.desc()",
    )


class PromptVersion(BaseModel, AuditMixin):
    """Prompt Version model for version control of prompts."""

    __tablename__ = "prompt_version"

    prompt_id: Mapped[str] = mapped_column(
        ForeignKey("prompt.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    version_number: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    change_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_published: Mapped[bool] = mapped_column(default=False, nullable=False, index=True)
    performance_metrics: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON for metrics
    usage_count: Mapped[int] = mapped_column(default=0, nullable=False)

    # Relationships
    prompt: Mapped["Prompt"] = relationship(
        "Prompt",
        back_populates="versions",
    )
