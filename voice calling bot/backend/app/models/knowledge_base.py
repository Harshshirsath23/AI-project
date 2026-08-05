from typing import Optional

from sqlalchemy import Uuid, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditMixin, BaseModel, SoftDeleteMixin


class KnowledgeBase(BaseModel, AuditMixin, SoftDeleteMixin):
    """Knowledge Base model for RAG implementation."""

    __tablename__ = "knowledge_base"

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organization.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    embedding_model: Mapped[str] = mapped_column(
        String(100),
        default="sentence-transformers",
        nullable=False,
    )
    chunk_size: Mapped[int] = mapped_column(default=500, nullable=False)
    chunk_overlap: Mapped[int] = mapped_column(default=50, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False, index=True)
    document_count: Mapped[int] = mapped_column(default=0, nullable=False)
    total_chunks: Mapped[int] = mapped_column(default=0, nullable=False)

    # Relationships
    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="knowledge_bases",
    )
    documents: Mapped[list["KnowledgeDocument"]] = relationship(
        "KnowledgeDocument",
        back_populates="knowledge_base",
        cascade="all, delete-orphan",
    )


class KnowledgeDocument(BaseModel, AuditMixin, SoftDeleteMixin):
    """Knowledge Document model for storing document metadata."""

    __tablename__ = "knowledge_document"

    knowledge_base_id: Mapped[str] = mapped_column(
        ForeignKey("knowledge_base.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    file_name: Mapped[str] = mapped_column(String(500), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    file_size: Mapped[int] = mapped_column(nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)  # pdf, txt, docx, etc.
    mime_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    chunk_count: Mapped[int] = mapped_column(default=0, nullable=False)
    embedding_status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False,
        index=True,
    )  # pending, processing, completed, failed
    last_embedded_at: Mapped[Optional[str]] = mapped_column(Uuid, nullable=True)
    meta_data: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON for additional metadata
    content_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)  # SHA-256 hash

    # Relationships
    knowledge_base: Mapped["KnowledgeBase"] = relationship(
        "KnowledgeBase",
        back_populates="documents",
    )
