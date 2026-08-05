from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.connection import get_db
from app.models.phone_number import PhoneNumber

router = APIRouter()


class PhoneNumberCreateSchema(BaseModel):
    number: str
    friendly_name: Optional[str] = "Outbound Caller ID"
    provider: str = "twilio"
    country_code: str = "US"


@router.get("")
async def list_phone_numbers(db: Session = Depends(get_db)):
    """Get list of active organization phone numbers."""
    numbers = db.query(PhoneNumber).filter(PhoneNumber.deleted_at.is_(None)).all()

    
    # If empty, insert current Twilio number into DB for default experience
    if not numbers:
        default_num = PhoneNumber(
            organization_id="00000000-0000-0000-0000-000000000000",
            number="+17372212163",
            friendly_name="Twilio Trial Number",
            provider="twilio",
            status="active",
            capabilities={"voice": True, "sms": True}
        )
        db.add(default_num)
        db.commit()
        db.refresh(default_num)
        numbers = [default_num]

    return [
        {
            "id": str(n.id),
            "number": n.number,
            "friendly_name": n.friendly_name,
            "provider": n.provider,
            "status": n.status,
            "created_at": n.created_at.isoformat() if n.created_at else None,
        }
        for n in numbers
    ]


@router.post("")
async def create_phone_number(data: PhoneNumberCreateSchema, db: Session = Depends(get_db)):
    """Register a new phone number."""
    phone = PhoneNumber(
        organization_id="00000000-0000-0000-0000-000000000000",
        number=data.number,
        friendly_name=data.friendly_name,
        provider=data.provider,
        status="active",
        capabilities={"voice": True, "sms": True}
    )
    db.add(phone)
    db.commit()
    db.refresh(phone)
    return {"status": "success", "id": str(phone.id), "number": phone.number}
