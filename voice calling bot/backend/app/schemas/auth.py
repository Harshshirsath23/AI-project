from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class LoginRequest(BaseModel):
    """Schema for user login request."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    organization_slug: Optional[str] = None

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class RegisterRequest(BaseModel):
    """Schema for user registration request."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    organization_name: str = Field(..., min_length=1, max_length=255)
    organization_slug: str = Field(..., min_length=1, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class TokenResponse(BaseModel):
    """Schema for token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request."""

    refresh_token: str


class PasswordChangeRequest(BaseModel):
    """Schema for password change request."""

    current_password: str = Field(..., min_length=1, max_length=128)
    new_password: str = Field(..., min_length=8, max_length=128)

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""

    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation."""

    token: str
    new_password: str = Field(..., min_length=8, max_length=128)

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserResponse(BaseModel):
    """Schema for user response."""

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
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CurrentUserResponse(BaseModel):
    """Schema for current user response with organization and role."""

    user: UserResponse
    organization_id: str
    organization_name: str
    organization_slug: str
    role_id: str
    role_name: str
    role_slug: str
    permissions: list[str]


class LogoutResponse(BaseModel):
    """Schema for logout response."""

    message: str
