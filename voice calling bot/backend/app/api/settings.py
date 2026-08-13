from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.connection import get_db
from app.config.settings import get_settings

router = APIRouter()


class SettingsUpdateSchema(BaseModel):
    app_name: Optional[str] = None
    gemini_api_key: Optional[str] = None
    huggingface_api_key: Optional[str] = None
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_phone_number: Optional[str] = None


@router.get("")
async def get_app_settings(db: Session = Depends(get_db)):
    """Get current organization & provider settings from DB."""
    from app.models.organization import OrganizationSettings
    # We use the default org UUID for single-tenant mode
    org_id = "00000000-0000-0000-0000-000000000000"
    
    org_settings = db.query(OrganizationSettings).filter_by(organization_id=org_id).first()
    s = get_settings()
    
    return {
        "app_name": s.app_name,
        "app_env": s.app_env,
        "app_version": s.app_version,
        "gemini_api_key_configured": bool(s.gemini_api_key),
        "huggingface_api_key_configured": bool(s.huggingface_api_key),
        "twilio_configured": bool(org_settings and org_settings.twilio_account_sid and org_settings.twilio_auth_token),
        "twilio_account_sid": org_settings.twilio_account_sid if org_settings else "",
        "twilio_phone_number": s.twilio_phone_number,
    }


@router.put("")
async def update_app_settings(data: SettingsUpdateSchema, db: Session = Depends(get_db)):
    """Update settings in DB."""
    from app.models.organization import OrganizationSettings
    from app.services.telephony_service import telephony_provider
    org_id = "00000000-0000-0000-0000-000000000000"
    
    org_settings = db.query(OrganizationSettings).filter_by(organization_id=org_id).first()
    if not org_settings:
        org_settings = OrganizationSettings(organization_id=org_id)
        db.add(org_settings)
    
    if data.twilio_account_sid is not None:
        org_settings.twilio_account_sid = data.twilio_account_sid
    if data.twilio_auth_token is not None:
        org_settings.twilio_auth_token = data.twilio_auth_token
        
    db.commit()
    
    # Reload telephony provider credentials
    telephony_provider.reload_credentials()

    return {"status": "success", "message": "Settings updated"}
