from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
import csv
import io

from app.database.connection import get_db
from app.models.lead import Lead

router = APIRouter()


class LeadCreateSchema(BaseModel):
    name: str
    phone_number: str
    email: Optional[str] = None
    company: Optional[str] = None
    campaign_id: Optional[str] = None
    notes: Optional[str] = None


@router.get("")
async def list_leads(
    db: Session = Depends(get_db),
    campaign_id: Optional[str] = None,
    status: Optional[str] = None
):
    """Get list of leads."""
    query = db.query(Lead).filter(Lead.deleted_at.is_(None))
    if campaign_id:
        query = query.filter(Lead.campaign_id == campaign_id)
    if status:
        query = query.filter(Lead.status == status)
        
    leads = query.order_by(Lead.created_at.desc()).all()

    return [
        {
            "id": str(lead.id),
            "name": lead.name,
            "phone_number": lead.phone_number,
            "email": lead.email,
            "company": lead.company,
            "status": lead.status,
            "call_attempts": lead.call_attempts,
            "last_call_at": str(lead.last_call_at) if lead.last_call_at else None,
            "created_at": lead.created_at.isoformat() if lead.created_at else None,
        }
        for lead in leads
    ]



@router.post("")
async def create_lead(data: LeadCreateSchema, db: Session = Depends(get_db)):
    """Create a single lead."""
    lead = Lead(
        name=data.name,
        phone_number=data.phone_number,
        email=data.email,
        company=data.company,
        campaign_id=data.campaign_id if data.campaign_id else None,
        notes=data.notes,
        source="manual",
        status="pending",
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return {"status": "success", "id": str(lead.id), "name": lead.name}


@router.post("/bulk")
async def create_leads_bulk(
    leads_data: List[LeadCreateSchema],
    db: Session = Depends(get_db)
):
    """Batch create multiple leads into PostgreSQL."""
    if not leads_data:
        raise HTTPException(status_code=400, detail="Empty leads list provided.")

    created_leads = []
    for item in leads_data:
        if not item.phone_number or not item.name:
            continue
        lead = Lead(
            name=item.name.strip(),
            phone_number=item.phone_number.strip(),
            email=item.email.strip() if item.email else None,
            company=item.company.strip() if item.company else None,
            campaign_id=item.campaign_id if item.campaign_id else None,
            notes=item.notes,
            source="csv_import",
            status="pending",
        )
        db.add(lead)
        created_leads.append(lead)

    db.commit()
    for l in created_leads:
        db.refresh(l)

    return {
        "status": "success",
        "imported_count": len(created_leads),
        "leads": [{"id": str(l.id), "name": l.name, "phone_number": l.phone_number} for l in created_leads]
    }


@router.post("/upload-csv")
async def upload_leads_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload, parse, and persist CSV leads directly to PostgreSQL."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are supported.")

    content = await file.read()
    try:
        text_content = content.decode("utf-8")
    except UnicodeDecodeError:
        text_content = content.decode("latin-1")

    reader = csv.DictReader(io.StringIO(text_content))
    created_leads = []

    for row in reader:
        # Normalize header keys to lowercase
        norm_row = {k.strip().lower(): v.strip() for k, v in row.items() if k}

        # Find name
        name = (
            norm_row.get("name")
            or norm_row.get("full_name")
            or norm_row.get("contact_name")
            or norm_row.get("lead_name")
            or "Target Lead"
        )

        # Find phone
        phone = (
            norm_row.get("phone")
            or norm_row.get("phone_number")
            or norm_row.get("mobile")
            or norm_row.get("telephone")
            or norm_row.get("contact_number")
            or ""
        )

        if not phone:
            continue

        email = norm_row.get("email") or norm_row.get("email_address") or None
        company = norm_row.get("company") or norm_row.get("organization") or norm_row.get("business") or None
        notes = norm_row.get("notes") or norm_row.get("description") or None

        lead = Lead(
            name=name,
            phone_number=phone,
            email=email,
            company=company,
            notes=notes,
            source="csv_upload",
            status="pending",
        )
        db.add(lead)
        created_leads.append(lead)

    db.commit()
    for l in created_leads:
        db.refresh(l)

    return {
        "status": "success",
        "imported_count": len(created_leads),
        "leads": [{"id": str(l.id), "name": l.name, "phone_number": l.phone_number} for l in created_leads]
    }


class LeadUpdateSchema(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


@router.put("/{lead_id}")
async def update_lead(lead_id: str, data: LeadUpdateSchema, db: Session = Depends(get_db)):
    """Update lead details."""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    if data.name is not None:
        lead.name = data.name
    if data.phone_number is not None:
        lead.phone_number = data.phone_number
    if data.email is not None:
        lead.email = data.email
    if data.company is not None:
        lead.company = data.company
    if data.status is not None:
        lead.status = data.status
    if data.notes is not None:
        lead.notes = data.notes

    db.commit()
    db.refresh(lead)
    return {"status": "success", "id": str(lead.id), "name": lead.name}


@router.delete("/{lead_id}")
async def delete_lead(lead_id: str, db: Session = Depends(get_db)):
    """Delete a lead."""
    from datetime import datetime, UTC
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead.deleted_at = datetime.now(UTC)
    db.commit()
    return {"status": "success", "message": "Lead deleted successfully"}
