from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# -------------------------
# Auth / Token Schemas
# -------------------------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="User password")

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int # seconds
    user_id: UUID
    organization_id: Optional[UUID] = None
    account_type: str

class RefreshRequest(BaseModel):
    refresh_token: str

class LogoutResponse(BaseModel):
    message: str = "Successfully logged out"

# -------------------------
# User Profile Schemas
# -------------------------
class UserProfileSchema(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    profile_photo: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    id: UUID
    organization_id: Optional[UUID] = None
    username: str
    email: EmailStr
    phone: Optional[str] = None
    account_type: str
    account_status: str
    account_scope: str = "ORGANIZATION"
    scope: str = "ORGANIZATION"
    is_platform_admin: bool = False
    is_organization_admin: bool = False
    email_verified: bool
    phone_verified: bool
    mfa_enabled: bool
    is_active: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime
    profile: Optional[UserProfileSchema] = None
    roles: List[str] = []
    permissions: List[str] = []

    model_config = ConfigDict(from_attributes=True)

class UserCreateRequest(BaseModel):
    organization_id: Optional[UUID] = None
    username: Optional[str] = Field(None, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    first_name: str
    last_name: str
    phone: Optional[str] = None
    account_type: str = "RECRUITER"

class ProvisionOrgAdminRequest(BaseModel):
    email: EmailStr
    first_name: Optional[str] = "Org"
    last_name: Optional[str] = "Admin"
    password: Optional[str] = Field("Password123!", min_length=6)
    phone: Optional[str] = None

class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    account_status: Optional[str] = None

# -------------------------
# Password Management
# -------------------------
class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)

# -------------------------
# Role & Permission Schemas
# -------------------------
class PermissionResponse(BaseModel):
    id: UUID
    permission_code: str
    permission_name: str
    module: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class RoleResponse(BaseModel):
    id: UUID
    organization_id: UUID
    role_code: str
    role_name: str
    description: Optional[str] = None
    is_system_role: bool
    permissions: List[PermissionResponse] = []

    model_config = ConfigDict(from_attributes=True)

class RoleCreateRequest(BaseModel):
    role_code: str = Field(..., min_length=2, max_length=50)
    role_name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    permission_ids: List[UUID] = []

class UserRoleAssignRequest(BaseModel):
    user_id: UUID
    role_ids: List[UUID]

# -------------------------
# Session Schemas
# -------------------------
class SessionResponse(BaseModel):
    id: UUID
    user_id: UUID
    device_name: Optional[str] = None
    device_type: Optional[str] = None
    operating_system: Optional[str] = None
    browser: Optional[str] = None
    ip_address: Optional[str] = None
    login_time: datetime
    expires_at: datetime
    is_revoked: bool

    model_config = ConfigDict(from_attributes=True)
