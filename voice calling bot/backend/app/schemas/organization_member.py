from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class OrganizationMemberCreate(BaseModel):
    """Schema for adding a member to organization."""

    email: EmailStr
    role_id: str
    job_title: Optional[str] = Field(None, max_length=100)
    department: Optional[str] = Field(None, max_length=100)


class OrganizationMemberUpdate(BaseModel):
    """Schema for updating organization member."""

    role_id: Optional[str] = None
    job_title: Optional[str] = Field(None, max_length=100)
    department: Optional[str] = Field(None, max_length=100)


class OrganizationMemberResponse(BaseModel):
    """Schema for organization member response."""

    user_id: str
    email: str
    first_name: str
    last_name: str
    avatar_url: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    role_id: str
    role_name: str
    role_slug: str
    is_active: bool
    is_verified: bool
    joined_at: datetime

    class Config:
        from_attributes = True


class OrganizationInviteCreate(BaseModel):
    """Schema for creating organization invitation."""

    email: EmailStr
    role_id: str
    message: Optional[str] = Field(None, max_length=500)


class OrganizationInviteResponse(BaseModel):
    """Schema for organization invitation response."""

    id: str
    email: str
    role_id: str
    role_name: str
    status: str
    expires_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
