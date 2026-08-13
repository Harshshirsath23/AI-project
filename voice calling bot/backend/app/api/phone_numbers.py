from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.config.settings import get_settings
from app.core.logging import get_logger
from app.database.connection import get_db
from app.models.phone_number import PhoneNumber

logger = get_logger(__name__)
router = APIRouter()


class PhoneNumberCreateSchema(BaseModel):
    number: str
    provider: str = "twilio"


@router.get("")
async def list_phone_numbers(db: Session = Depends(get_db)):
    """Get list of active organization phone numbers from PostgreSQL."""
    numbers = db.query(PhoneNumber).filter(PhoneNumber.deleted_at.is_(None)).all()

    # If empty, seed default Twilio trial number
    if not numbers:
        default_num = PhoneNumber(
            organization_id="00000000-0000-0000-0000-000000000000",
            number="+17372212163",
            provider="twilio",
            status="active",
        )
        db.add(default_num)
        db.commit()
        db.refresh(default_num)
        numbers = [default_num]

    return [
        {
            "id": str(n.id),
            "number": n.number,
            "provider": n.provider,
            "status": n.status,
            "created_at": n.created_at.isoformat() if n.created_at else None,
        }
        for n in numbers
    ]


@router.post("/sync-twilio")
async def sync_twilio_phone_numbers(db: Session = Depends(get_db)):
    """Fetch active numbers directly from Twilio API and register into PostgreSQL."""
    from app.models.organization import OrganizationSettings
    org_id = "00000000-0000-0000-0000-000000000000"
    
    org_settings = db.query(OrganizationSettings).filter_by(organization_id=org_id).first()
    
    if not org_settings:
        raise HTTPException(status_code=400, detail="Organization settings not found")
        
    account_sid = org_settings.twilio_account_sid
    auth_token = org_settings.twilio_auth_token

    synced_count = 0
    if account_sid and auth_token and account_sid.startswith("AC"):
        try:
            from twilio.rest import Client
            client = Client(account_sid, auth_token)
            incoming = client.incoming_phone_numbers.list()

            for item in incoming:
                existing = db.query(PhoneNumber).filter(PhoneNumber.number == item.phone_number).first()
                if not existing:
                    new_num = PhoneNumber(
                        organization_id="00000000-0000-0000-0000-000000000000",
                        number=item.phone_number,
                        provider="twilio",
                        status="active",
                    )
                    db.add(new_num)
                    synced_count += 1

            if synced_count > 0:
                db.commit()
            logger.info("Successfully fetched numbers from Twilio", count=synced_count)
        except Exception as e:
            logger.warning("Twilio API fetch exception", error=str(e))

    numbers = db.query(PhoneNumber).filter(PhoneNumber.deleted_at.is_(None)).all()
    return [
        {
            "id": str(n.id),
            "number": n.number,
            "provider": n.provider,
            "status": n.status,
            "created_at": n.created_at.isoformat() if n.created_at else None,
        }
        for n in numbers
    ]


@router.post("")
async def create_phone_number(data: PhoneNumberCreateSchema, db: Session = Depends(get_db)):
    """Register a phone number in PostgreSQL."""
    phone = PhoneNumber(
        organization_id="00000000-0000-0000-0000-000000000000",
        number=data.number,
        provider=data.provider,
        status="active",
    )
    db.add(phone)
    db.commit()
    db.refresh(phone)
    return {"status": "success", "id": str(phone.id), "number": phone.number}
