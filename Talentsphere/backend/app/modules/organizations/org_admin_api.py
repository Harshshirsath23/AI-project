import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_async_db
from app.modules.auth.dependencies import require_org_admin, get_current_user, get_current_organization
from app.modules.auth.models import User, Role, UserRole, Permission, RolePermission, UserProfile
from app.modules.auth.repository import UserRepository, AuditRepository
from app.modules.auth.schemas import UserResponse, UserCreateRequest
from app.modules.auth.constants import SYSTEM_PERMISSIONS, AccountType, AccountStatus
from app.modules.organizations.repository import OrganizationRepository, SettingsRepository

router = APIRouter(prefix="/organization", tags=["Organization Administration"])


class CustomRoleCreate(BaseModel):
    role_code: str
    role_name: str
    description: Optional[str] = None
    permissions: List[str] = []


@router.get("/users", summary="List Organization Users", dependencies=[Depends(require_org_admin)])
async def list_org_users(
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """List users within the authenticated user's organization."""
    if not org_id:
        raise HTTPException(status_code=400, detail="User is not associated with an organization")
    
    stmt = select(User).where(User.organization_id == org_id, User.is_deleted == False)
    res = await db.execute(stmt)
    users = res.scalars().all()
    
    user_repo = UserRepository(db)
    result = []
    for u in users:
        u_with_profile = await user_repo.get_with_profile(u.id)
        roles = await user_repo.get_user_roles(u.id)
        perms = await user_repo.get_user_permissions(u.id)
        role_codes = [r.role_code for r in roles]

        profile_schema = None
        if hasattr(u_with_profile, "profile_obj") and u_with_profile.profile_obj:
            p = u_with_profile.profile_obj
            profile_schema = {
                "first_name": p.first_name,
                "last_name": p.last_name
            }

        result.append({
            "id": str(u.id),
            "username": u.username,
            "email": u.email,
            "account_type": u.account_type,
            "account_status": u.account_status,
            "is_active": u.is_active,
            "profile": profile_schema,
            "roles": role_codes,
            "permissions": perms
        })
    return result


@router.post("/users", summary="Create Organization User", dependencies=[Depends(require_org_admin)])
async def create_org_user(
    req: UserCreateRequest,
    current_user: User = Depends(get_current_user),
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a user inside the Organization. Escalation to PLATFORM_SUPER_ADMIN is forbidden."""
    if not org_id:
        raise HTTPException(status_code=400, detail="Organization context required")

    # Protection against privilege escalation
    if req.account_type in [AccountType.PLATFORM_SUPER_ADMIN.value, AccountType.SUPER_ADMIN.value]:
        raise HTTPException(status_code=403, detail="Escalation forbidden: Cannot create Platform Super Admin")

    user_repo = UserRepository(db)
    existing = await user_repo.get_by_email(req.email)
    if existing:
        raise HTTPException(status_code=400, detail="User email already registered")

    from app.modules.auth.security import hash_password
    raw_pwd = req.password or "WelcomeTS2026!"
    pwd_hash = hash_password(raw_pwd)

    new_user = User(
        organization_id=org_id,
        username=req.username or req.email,
        email=req.email,
        phone=req.phone,
        password_hash=pwd_hash,
        account_type=req.account_type or "RECRUITER",
        account_status="Active",
        account_scope="ORGANIZATION",
        email_verified=True,
        is_active=True
    )
    profile = UserProfile(
        first_name=req.first_name,
        last_name=req.last_name
    )
    created_user = await user_repo.create(new_user, profile)

    audit_repo = AuditRepository(db)
    await audit_repo.log_activity(
        user_id=current_user.id,
        module="auth",
        action=f"Created User {created_user.email} in Org {org_id}"
    )
    await db.commit()

    return {
        "status": "success",
        "user_id": str(created_user.id),
        "email": created_user.email,
        "temporary_password": raw_pwd
    }


@router.get("/roles", summary="List Organization Roles", dependencies=[Depends(require_org_admin)])
async def list_org_roles(
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """List tenant-scoped roles for this organization."""
    stmt = select(Role).where(
        (Role.organization_id == org_id) | (Role.organization_id.is_(None) & (Role.scope == "ORGANIZATION"))
    )
    res = await db.execute(stmt)
    roles = res.scalars().all()
    return roles


@router.post("/roles", summary="Create Custom Organization Role", dependencies=[Depends(require_org_admin)])
async def create_custom_org_role(
    req: CustomRoleCreate,
    current_user: User = Depends(get_current_user),
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Create custom role inside organization. Cannot grant PLATFORM scope permissions."""
    if not org_id:
        raise HTTPException(status_code=400, detail="Organization context required")

    # Protection against assigning platform permissions
    platform_perms = [p["code"] for p in SYSTEM_PERMISSIONS if p.get("scope") == "PLATFORM"]
    forbidden_requested = [p for p in req.permissions if p in platform_perms]
    if forbidden_requested:
        raise HTTPException(
            status_code=403,
            detail=f"Escalation forbidden: Cannot assign platform permissions ({', '.join(forbidden_requested)}) to organization role"
        )

    new_role = Role(
        organization_id=org_id,
        role_code=req.role_code.upper(),
        role_name=req.role_name,
        scope="ORGANIZATION",
        description=req.description,
        is_system_role=False
    )
    db.add(new_role)
    await db.flush()

    audit_repo = AuditRepository(db)
    await audit_repo.log_activity(
        user_id=current_user.id,
        module="auth",
        action=f"Created custom org role {new_role.role_code}"
    )
    await db.commit()

    return {
        "status": "success",
        "role_id": str(new_role.id),
        "role_code": new_role.role_code,
        "role_name": new_role.role_name
    }


@router.get("/permissions", summary="List Assignable Organization Permissions", dependencies=[Depends(require_org_admin)])
async def list_assignable_org_permissions():
    """Returns permissions assignable by Organization Super Admin (strictly ORGANIZATION scope)."""
    org_permissions = [p for p in SYSTEM_PERMISSIONS if p.get("scope") == "ORGANIZATION"]
    return org_permissions


@router.get("/settings", summary="Get Organization Settings", dependencies=[Depends(require_org_admin)])
async def get_org_settings(
    org_id: uuid.UUID = Depends(get_current_organization),
    db: AsyncSession = Depends(get_async_db)
):
    """Get tenant organization settings."""
    if not org_id:
        raise HTTPException(status_code=400, detail="Organization context required")

    settings_repo = SettingsRepository(db)
    settings = await settings_repo.get_all_settings(org_id)
    return settings
