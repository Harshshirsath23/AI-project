from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
import uuid

from app.database.session import get_async_db
from app.modules.auth.dependencies import get_current_user, get_current_organization, require_permission
from app.modules.auth.schemas import UserResponse
from app.modules.organizations.models import Organization
from app.modules.organizations.schemas import (
    OrganizationCreate, OrganizationUpdate, OrganizationResponse,
    BranchResponse, DepartmentResponse, DesignationResponse, ShiftResponse,
    SettingResponse, SettingUpdate
)
from app.modules.organizations.repository import (
    OrganizationRepository, BranchRepository, DepartmentRepository,
    DesignationRepository, ShiftRepository, SettingsRepository
)
from app.modules.organizations.service import OrganizationInitializationService

router = APIRouter(tags=["Organizations"])

# -----------------------------
# 1. Organization Management
# -----------------------------
@router.post("/", summary="Initialize New Organization Tenant", dependencies=[Depends(require_permission("sys:manage"))])
async def create_organization(
    org_data: OrganizationCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Creates a new Organization Tenant. Scaffolds storage folders, seeds master data, and creates defaults.
    """
    service = OrganizationInitializationService(db)
    result = await service.initialize_tenant(org_data, current_user.id)
    return result

@router.get("/", response_model=List[OrganizationResponse], summary="List All Organizations", dependencies=[Depends(require_permission("sys:manage"))])
async def list_organizations(
    db: AsyncSession = Depends(get_async_db)
):
    """
    Lists all organizations. Restricted to sys:manage (Super Admins).
    """
    repo = OrganizationRepository(db)
    orgs = await repo.get_all()
    return orgs

@router.get("/me", response_model=OrganizationResponse, summary="Get Current Organization", dependencies=[Depends(require_permission("org:read"))])
async def get_my_organization(
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    repo = OrganizationRepository(db)
    org = await repo.get_by_id(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.patch("/me", response_model=OrganizationResponse, summary="Update Organization", dependencies=[Depends(require_permission("org:write"))])
async def update_my_organization(
    data: OrganizationUpdate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    repo = OrganizationRepository(db)
    org = await repo.update(org_id, data)
    await db.commit()
    return org

# -----------------------------
# 2. Master Data APIs
# -----------------------------
@router.get("/branches", response_model=List[BranchResponse], summary="Get Organization Branches", dependencies=[Depends(require_permission("org:read"))])
async def get_branches(
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    repo = BranchRepository(db)
    return await repo.get_all(org_id)

@router.get("/departments", response_model=List[DepartmentResponse], summary="Get Organization Departments", dependencies=[Depends(require_permission("org:read"))])
async def get_departments(
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    repo = DepartmentRepository(db)
    return await repo.get_all(org_id)

@router.get("/designations", response_model=List[DesignationResponse], summary="Get Organization Designations", dependencies=[Depends(require_permission("org:read"))])
async def get_designations(
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    repo = DesignationRepository(db)
    return await repo.get_all(org_id)

@router.get("/shifts", response_model=List[ShiftResponse], summary="Get Organization Shifts", dependencies=[Depends(require_permission("org:read"))])
async def get_shifts(
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    repo = ShiftRepository(db)
    return await repo.get_all(org_id)

# -----------------------------
# 3. Company Settings
# -----------------------------
@router.get("/settings", response_model=List[SettingResponse], summary="Get Company Settings", dependencies=[Depends(require_permission("org:read"))])
async def get_settings(
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    repo = SettingsRepository(db)
    return await repo.get_all_settings(org_id)

@router.patch("/settings", summary="Update Company Setting", dependencies=[Depends(require_permission("org:write"))])
async def update_setting(
    key: str,
    data: SettingUpdate,
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    repo = SettingsRepository(db)
    await repo.update_setting(org_id, key, data.setting_value)
    await db.commit()
    return {"status": "success", "message": f"Setting {key} updated successfully"}
