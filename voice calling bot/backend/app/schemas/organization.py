from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class OrganizationCreate(BaseModel):
    """Schema for organization creation."""

    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    website: Optional[str] = Field(None, max_length=500)
    industry: Optional[str] = Field(None, max_length=100)
    company_size: Optional[str] = Field(None, max_length=50)
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = Field(None, max_length=20)


class OrganizationUpdate(BaseModel):
    """Schema for organization update."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    website: Optional[str] = Field(None, max_length=500)
    logo_url: Optional[str] = Field(None, max_length=500)
    industry: Optional[str] = Field(None, max_length=100)
    company_size: Optional[str] = Field(None, max_length=50)
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = Field(None, max_length=20)


class OrganizationSettingsUpdate(BaseModel):
    """Schema for organization settings update."""

    timezone: Optional[str] = Field(None, max_length=50)
    locale: Optional[str] = Field(None, max_length=10)
    currency: Optional[str] = Field(None, max_length=10)
    default_language: Optional[str] = Field(None, max_length=10)
    max_concurrent_calls: Optional[int] = Field(None, ge=1, le=1000)
    call_recording_enabled: Optional[bool] = None
    auto_transcription_enabled: Optional[bool] = None
    retention_days: Optional[int] = Field(None, ge=1, le=3650)
    custom_branding_enabled: Optional[bool] = None
    api_rate_limit: Optional[int] = Field(None, ge=1, le=10000)


class OrganizationResponse(BaseModel):
    """Schema for organization response."""

    id: str
    name: str
    slug: str
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrganizationDetailResponse(BaseModel):
    """Schema for organization detail response with settings."""

    id: str
    name: str
    slug: str
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    settings: Optional[dict] = None

    class Config:
        from_attributes = True
