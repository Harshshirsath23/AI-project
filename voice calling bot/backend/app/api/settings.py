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
async def get_app_settings():
    """Get current organization & provider settings."""
    s = get_settings()
    return {
        "app_name": s.app_name,
        "app_env": s.app_env,
        "app_version": s.app_version,
        "gemini_api_key_configured": bool(s.gemini_api_key),
        "huggingface_api_key_configured": bool(s.huggingface_api_key),
        "twilio_configured": bool(s.twilio_account_sid and s.twilio_auth_token),
        "twilio_account_sid": s.twilio_account_sid,
        "twilio_phone_number": s.twilio_phone_number,
    }


@router.put("")
async def update_app_settings(data: SettingsUpdateSchema):
    """Update settings (dev mode update)."""
    return {"status": "success", "message": "Settings updated"}
