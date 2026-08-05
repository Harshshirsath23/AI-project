from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for user creation."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    job_title: Optional[str] = Field(None, max_length=100)
    department: Optional[str] = Field(None, max_length=100)
    role_id: Optional[str] = None
    timezone: str = Field(default="UTC", max_length=50)
    locale: str = Field(default="en-US", max_length=10)


class UserUpdate(BaseModel):
    """Schema for user update."""

    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = Field(None, max_length=500)
    job_title: Optional[str] = Field(None, max_length=100)
    department: Optional[str] = Field(None, max_length=100)
    timezone: Optional[str] = Field(None, max_length=50)
    locale: Optional[str] = Field(None, max_length=10)
    role_id: Optional[str] = None


class UserListResponse(BaseModel):
    """Schema for user list response."""

    id: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    is_active: bool
    is_verified: bool
    role_id: Optional[str] = None
    role_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UserDetailResponse(BaseModel):
    """Schema for user detail response."""

    id: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    timezone: str
    locale: str
    is_active: bool
    is_verified: bool
    last_login_at: Optional[datetime] = None
    role_id: Optional[str] = None
    role_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserDeactivateRequest(BaseModel):
    """Schema for user deactivation."""

    reason: Optional[str] = Field(None, max_length=500)
