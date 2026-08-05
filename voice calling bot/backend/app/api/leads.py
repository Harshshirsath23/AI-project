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
    
    # If DB is empty, populate demo seed lead
    if not leads:
        demo_lead = Lead(
            name="Harsh Shirsath",
            phone_number="+917039015196",
            email="harsh@example.com",
            company="Voxera Client",
            status="pending",
        )
        db.add(demo_lead)
        db.commit()
        db.refresh(demo_lead)
        leads = [demo_lead]

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
        status="pending",
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return {"status": "success", "id": str(lead.id), "name": lead.name}


@router.post("/import")
async def import_leads_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Import contacts from CSV file."""
    content = await file.read()
    text = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    
    imported_count = 0
    for row in reader:
        name = row.get("name") or row.get("Name") or "Unknown Contact"
        phone = row.get("phone") or row.get("Phone") or row.get("phone_number")
        if phone:
            lead = Lead(
                name=name,
                phone_number=phone,
                email=row.get("email") or row.get("Email"),
                company=row.get("company") or row.get("Company"),
                status="pending"
            )
            db.add(lead)
            imported_count += 1
            
    db.commit()
    return {"status": "success", "imported_count": imported_count}
