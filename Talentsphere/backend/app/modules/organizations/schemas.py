from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime, date
import uuid

# -----------------------------
# Organization Schemas
# -----------------------------
class OrganizationBase(BaseModel):
    organization_code: str = Field(..., max_length=50)
    legal_name: str = Field(..., max_length=255)
    display_name: str = Field(..., max_length=255)
    registration_number: Optional[str] = Field(None, max_length=100)
    tax_number: Optional[str] = Field(None, max_length=100)
    industry_id: uuid.UUID
    website: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=30)
    logo_path: Optional[str] = Field(None, max_length=500)
    employee_count: Optional[int] = None
    subscription_plan: str = Field(..., max_length=50)
    subscription_status: str = Field(..., max_length=30)
    timezone_id: Optional[uuid.UUID] = None
    currency_id: Optional[uuid.UUID] = None
    language_id: Optional[uuid.UUID] = None

class OrganizationCreate(OrganizationBase):
    admin_email: Optional[EmailStr] = None
    admin_first_name: Optional[str] = None
    admin_last_name: Optional[str] = None
    admin_password: Optional[str] = None

class OrganizationUpdate(BaseModel):
    display_name: Optional[str] = Field(None, max_length=255)
    website: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=30)
    logo_path: Optional[str] = Field(None, max_length=500)
    timezone_id: Optional[uuid.UUID] = None
    currency_id: Optional[uuid.UUID] = None
    language_id: Optional[uuid.UUID] = None

class OrganizationResponse(OrganizationBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# -----------------------------
# Branch Schemas
# -----------------------------
class BranchBase(BaseModel):
    branch_code: str = Field(..., max_length=30)
    branch_name: str = Field(..., max_length=150)
    location_id: Optional[uuid.UUID] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=30)
    manager_id: Optional[uuid.UUID] = None
    is_head_office: bool = False

class BranchCreate(BranchBase):
    pass

class BranchUpdate(BaseModel):
    branch_name: Optional[str] = Field(None, max_length=150)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=30)
    manager_id: Optional[uuid.UUID] = None
    is_head_office: Optional[bool] = None

class BranchResponse(BranchBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

# -----------------------------
# Department Schemas
# -----------------------------
class DepartmentBase(BaseModel):
    department_code: str = Field(..., max_length=50)
    department_name: str = Field(..., max_length=150)
    business_unit_id: Optional[uuid.UUID] = None
    parent_department_id: Optional[uuid.UUID] = None
    department_head_id: Optional[uuid.UUID] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    department_name: Optional[str] = Field(None, max_length=150)
    business_unit_id: Optional[uuid.UUID] = None
    parent_department_id: Optional[uuid.UUID] = None
    department_head_id: Optional[uuid.UUID] = None

class DepartmentResponse(DepartmentBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

# -----------------------------
# Designation Schemas
# -----------------------------
class DesignationBase(BaseModel):
    designation_code: str = Field(..., max_length=50)
    designation_name: str = Field(..., max_length=150)
    job_family_id: Optional[uuid.UUID] = None
    level: Optional[str] = Field(None, max_length=30)
    grade: Optional[str] = Field(None, max_length=30)

class DesignationCreate(DesignationBase):
    pass

class DesignationUpdate(BaseModel):
    designation_name: Optional[str] = Field(None, max_length=150)
    job_family_id: Optional[uuid.UUID] = None
    level: Optional[str] = Field(None, max_length=30)
    grade: Optional[str] = Field(None, max_length=30)

class DesignationResponse(DesignationBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

# -----------------------------
# Shift Schemas
# -----------------------------
class ShiftBase(BaseModel):
    shift_name: str = Field(..., max_length=100)
    start_time: str = Field(..., max_length=30)
    end_time: str = Field(..., max_length=30)
    is_flexible: bool = False

class ShiftCreate(ShiftBase):
    pass

class ShiftUpdate(BaseModel):
    shift_name: Optional[str] = Field(None, max_length=100)
    start_time: Optional[str] = Field(None, max_length=30)
    end_time: Optional[str] = Field(None, max_length=30)
    is_flexible: Optional[bool] = None

class ShiftResponse(ShiftBase):
    id: uuid.UUID
    organization_id: uuid.UUID
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

# -----------------------------
# Settings Schemas
# -----------------------------
class SettingResponse(BaseModel):
    setting_key: str
    setting_value: str
    model_config = ConfigDict(from_attributes=True)

class SettingUpdate(BaseModel):
    setting_value: str
