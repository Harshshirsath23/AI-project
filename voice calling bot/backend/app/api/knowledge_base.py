from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.connection import get_db
from app.models.knowledge_base import KnowledgeBase, KnowledgeDocument

router = APIRouter()


class KnowledgeBaseCreateSchema(BaseModel):
    name: str
    description: Optional[str] = ""
    embedding_model: str = "sentence_transformers"
    chunk_size: int = 512
    chunk_overlap: int = 50


@router.get("")
async def list_knowledge_bases(db: Session = Depends(get_db)):
    """Get list of RAG knowledge bases."""
    kbs = db.query(KnowledgeBase).filter(KnowledgeBase.deleted_at.is_(None)).all()

    
    if not kbs:
        default_kb = KnowledgeBase(
            organization_id="00000000-0000-0000-0000-000000000000",
            name="Default Product Knowledge Base",
            description="Core product FAQs, features, and sales documentation for AI agents.",
            embedding_model="sentence_transformers",
            chunk_size=512,
            chunk_overlap=50,
            is_active=True,
            document_count=1,
            total_chunks=12,
        )
        db.add(default_kb)
        db.commit()
        db.refresh(default_kb)
        kbs = [default_kb]

    return [
        {
            "id": str(kb.id),
            "name": kb.name,
            "description": kb.description,
            "embedding_model": kb.embedding_model,
            "chunk_size": kb.chunk_size,
            "is_active": kb.is_active,
            "document_count": kb.document_count,
            "total_chunks": kb.total_chunks,
            "created_at": kb.created_at.isoformat() if kb.created_at else None,
        }
        for kb in kbs
    ]


@router.post("")
async def create_knowledge_base(data: KnowledgeBaseCreateSchema, db: Session = Depends(get_db)):
    """Create a new knowledge base."""
    kb = KnowledgeBase(
        organization_id="00000000-0000-0000-0000-000000000000",
        name=data.name,
        description=data.description,
        embedding_model=data.embedding_model,
        chunk_size=data.chunk_size,
        chunk_overlap=data.chunk_overlap,
        is_active=True,
    )
    db.add(kb)
    db.commit()
    db.refresh(kb)
    return {"status": "success", "id": str(kb.id), "name": kb.name}


class TextScriptUploadSchema(BaseModel):
    title: str
    script_text: str


@router.post("/{kb_id}/documents/text")
async def add_text_script_document(
    kb_id: str,
    data: TextScriptUploadSchema,
    db: Session = Depends(get_db)
):
    """
    Extracts and stores a text script document inside the Knowledge Base in PostgreSQL.
    """
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="Knowledge base not found")

    doc = KnowledgeDocument(
        knowledge_base_id=kb.id,
        title=data.title,
        file_name=f"{data.title.lower().replace(' ', '_')}.txt",
        file_path=f"/scripts/{data.title.lower().replace(' ', '_')}.txt",
        file_size=len(data.script_text.encode('utf-8')),
        file_type="txt",
        embedding_status="completed",
        chunk_count=1,
        meta_data=data.script_text,  # Stores extracted raw text content in DB
    )
    db.add(doc)
    
    kb.document_count = (kb.document_count or 0) + 1
    db.commit()
    db.refresh(doc)

    return {
        "status": "success",
        "document_id": str(doc.id),
        "title": doc.title,
        "extracted_chars": len(data.script_text)
    }


@router.get("/{kb_id}/documents")
async def list_kb_documents(kb_id: str, db: Session = Depends(get_db)):
    """List all extracted documents and scripts stored in a Knowledge Base."""
    docs = db.query(KnowledgeDocument).filter(KnowledgeDocument.knowledge_base_id == kb_id).all()
    return [
        {
            "id": str(d.id),
            "title": d.title,
            "file_name": d.file_name,
            "file_type": d.file_type,
            "file_size": d.file_size,
            "embedding_status": d.embedding_status,
            "content_preview": (d.meta_data[:200] + "...") if d.meta_data else "No text extracted",
            "content": d.meta_data or "",
            "created_at": d.created_at.isoformat() if d.created_at else None,
        }
        for d in docs
    ]


@router.get("/documents/all")
async def list_all_kb_documents(db: Session = Depends(get_db)):
    """List all Knowledge Base documents and scripts across all Knowledge Bases."""
    docs = db.query(KnowledgeDocument).filter(KnowledgeDocument.deleted_at.is_(None)).all()
    return [
        {
            "id": str(d.id),
            "kb_id": str(d.knowledge_base_id),
            "title": d.title,
            "file_name": d.file_name,
            "content": d.meta_data or "",
            "created_at": d.created_at.isoformat() if d.created_at else None,
        }
        for d in docs
    ]


class UpdateDocumentSchema(BaseModel):
    title: Optional[str] = None
    content: str


@router.put("/documents/{doc_id}")
async def update_kb_document(
    doc_id: str,
    data: UpdateDocumentSchema,
    db: Session = Depends(get_db)
):
    """Update extracted text content of a Knowledge Base script document."""
    doc = db.query(KnowledgeDocument).filter(KnowledgeDocument.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if data.title:
        doc.title = data.title
    doc.meta_data = data.content
    doc.file_size = len(data.content.encode('utf-8'))
    db.commit()
    db.refresh(doc)
    return {"status": "success", "id": str(doc.id), "title": doc.title}



