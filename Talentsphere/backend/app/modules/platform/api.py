import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_async_db
from app.modules.auth.dependencies import require_platform_admin, get_current_user
from app.modules.auth.models import User, Role, Permission, AuditLog, SecurityEvent
from app.modules.auth.repository import UserRepository, AuditRepository
from app.modules.auth.schemas import UserResponse, UserCreateRequest, ProvisionOrgAdminRequest
from app.modules.auth.constants import SYSTEM_PERMISSIONS, DEFAULT_ROLES, AccountStatus
from app.modules.organizations.models import Organization
from app.modules.organizations.schemas import OrganizationResponse, OrganizationCreate, OrganizationUpdate
from app.modules.organizations.repository import OrganizationRepository
from app.modules.organizations.service import OrganizationInitializationService

router = APIRouter(tags=["Platform Administration"])


@router.get("/metrics", summary="Get Platform Metrics", dependencies=[Depends(require_platform_admin)])
async def get_platform_metrics(db: AsyncSession = Depends(get_async_db)):
    """Fetch high-level platform stats for the Platform Super Admin."""
    total_orgs_res = await db.execute(select(func.count()).select_from(Organization))
    total_orgs = total_orgs_res.scalar() or 0

    active_orgs_res = await db.execute(
        select(func.count()).select_from(Organization).where(Organization.subscription_status == "Active")
    )
    active_orgs = active_orgs_res.scalar() or 0

    suspended_orgs_res = await db.execute(
        select(func.count()).select_from(Organization).where(Organization.subscription_status == "Suspended")
    )
    suspended_orgs = suspended_orgs_res.scalar() or 0

    total_users_res = await db.execute(select(func.count()).select_from(User).where(User.is_deleted == False))
    total_users = total_users_res.scalar() or 0

    recent_security_res = await db.execute(
        select(SecurityEvent).order_by(SecurityEvent.event_time.desc()).limit(10)
    )
    recent_security = recent_security_res.scalars().all()

    return {
        "total_organizations": total_orgs,
        "active_organizations": active_orgs,
        "suspended_organizations": suspended_orgs,
        "total_users": total_users,
        "recent_security_events": [
            {
                "id": str(e.id),
                "event_type": e.event_type,
                "severity": e.severity,
                "description": e.description,
                "event_time": e.event_time
            } for e in recent_security
        ]
    }


@router.get("/organizations", summary="List All Organizations", dependencies=[Depends(require_platform_admin)])
async def list_all_organizations(db: AsyncSession = Depends(get_async_db)):
    """List all tenant organizations across the platform."""
    repo = OrganizationRepository(db)
    orgs = await repo.get_all()
    return orgs


@router.post("/organizations", summary="Create Organization & Provision Org Super Admin", dependencies=[Depends(require_platform_admin)])
async def create_organization_platform(
    org_data: OrganizationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Platform Super Admin creates a new Organization and provisions its initial Organization Super Admin."""
    service = OrganizationInitializationService(db)
    result = await service.initialize_tenant(org_data, current_user.id)
    return result


@router.get("/organizations/{org_id}", summary="Get Organization Profile", dependencies=[Depends(require_platform_admin)])
async def get_organization_detail(org_id: uuid.UUID, db: AsyncSession = Depends(get_async_db)):
    """Get metadata for a specific organization."""
    repo = OrganizationRepository(db)
    org = await repo.get_by_id(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@router.post("/organizations/{org_id}/activate", summary="Activate Organization", dependencies=[Depends(require_platform_admin)])
async def activate_organization(org_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    """Activate a suspended organization tenant."""
    repo = OrganizationRepository(db)
    org = await repo.get_by_id(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    org.subscription_status = "Active"
    org.is_active = True
    await db.commit()

    audit_repo = AuditRepository(db)
    await audit_repo.log_security_event(
        event_type="ORGANIZATION_ACTIVATED",
        severity="INFO",
        description=f"Organization {org.display_name} ({org.organization_code}) activated by Platform Admin",
        user_id=current_user.id
    )
    await db.commit()

    return {"status": "success", "message": f"Organization '{org.display_name}' activated."}


@router.post("/organizations/{org_id}/suspend", summary="Suspend Organization", dependencies=[Depends(require_platform_admin)])
async def suspend_organization(org_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    """Suspend an organization tenant."""
    repo = OrganizationRepository(db)
    org = await repo.get_by_id(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    org.subscription_status = "Suspended"
    org.is_active = False
    await db.commit()

    audit_repo = AuditRepository(db)
    await audit_repo.log_security_event(
        event_type="ORGANIZATION_SUSPENDED",
        severity="WARNING",
        description=f"Organization {org.display_name} ({org.organization_code}) suspended by Platform Admin",
        user_id=current_user.id
    )
    await db.commit()

    return {"status": "success", "message": f"Organization '{org.display_name}' suspended."}


@router.post("/organizations/{org_id}/admin", summary="Provision / Reset Org Super Admin", dependencies=[Depends(require_platform_admin)])
async def provision_org_admin(
    org_id: uuid.UUID,
    req: ProvisionOrgAdminRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Create or reset an Organization Super Admin for a tenant."""
    org_repo = OrganizationRepository(db)
    org = await org_repo.get_by_id(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    user_repo = UserRepository(db)
    normalized_email = req.email.lower().strip()
    existing = await user_repo.get_by_email(normalized_email)

    from app.modules.auth.security import hash_password
    from app.modules.auth.models import UserProfile, UserRole

    raw_password = req.password or "OrgAdmin123!"
    pwd_hash = hash_password(raw_password)

    if existing:
        # Reset / Update existing admin password and credentials
        existing.password_hash = pwd_hash
        existing.account_type = "ORGANIZATION_SUPER_ADMIN"
        existing.account_scope = "ORGANIZATION"
        existing.account_status = "Active"
        existing.is_active = True
        existing.organization_id = org_id

        # Update profile names if provided
        prof_res = await db.execute(select(UserProfile).where(UserProfile.user_id == existing.id))
        prof = prof_res.scalar_one_or_none()
        if prof:
            if req.first_name: prof.first_name = req.first_name
            if req.last_name: prof.last_name = req.last_name
        
        await db.commit()
        target_user = existing
    else:
        new_user = User(
            organization_id=org_id,
            username=normalized_email,
            email=normalized_email,
            phone=req.phone,
            password_hash=pwd_hash,
            account_type="ORGANIZATION_SUPER_ADMIN",
            account_status="Active",
            account_scope="ORGANIZATION",
            email_verified=True,
            is_active=True
        )
        profile = UserProfile(
            first_name=req.first_name or "Org",
            last_name=req.last_name or "Admin"
        )
        target_user = await user_repo.create(new_user, profile)

        # Assign ORGANIZATION_SUPER_ADMIN role if exists
        role_res = await db.execute(
            select(Role).where(Role.organization_id == org_id, Role.role_code == "ORGANIZATION_SUPER_ADMIN")
        )
        admin_role = role_res.scalar_one_or_none()
        if admin_role:
            self_ur = UserRole(user_id=target_user.id, role_id=admin_role.id)
            db.add(self_ur)

        await db.commit()

    audit_repo = AuditRepository(db)
    await audit_repo.log_security_event(
        event_type="ORG_ADMIN_PROVISIONED",
        severity="INFO",
        description=f"Org Super Admin {target_user.email} provisioned/reset for org {org.display_name}",
        user_id=current_user.id
    )
    await db.commit()

    return {
        "status": "success",
        "user_id": str(target_user.id),
        "email": target_user.email,
        "temporary_password": raw_password
    }


@router.get("/roles", summary="List Global Roles", dependencies=[Depends(require_platform_admin)])
async def list_global_roles(db: AsyncSession = Depends(get_async_db)):
    """List system/global roles across the platform."""
    stmt = select(Role).where(Role.scope == "PLATFORM")
    res = await db.execute(stmt)
    roles = res.scalars().all()
    if not roles:
        return DEFAULT_ROLES
    return roles


@router.get("/permissions", summary="List All Permissions Catalog", dependencies=[Depends(require_platform_admin)])
async def list_system_permissions():
    """List all system permissions categorized by PLATFORM vs ORGANIZATION scopes."""
    return {
        "platform_permissions": [p for p in SYSTEM_PERMISSIONS if p.get("scope") == "PLATFORM"],
        "organization_permissions": [p for p in SYSTEM_PERMISSIONS if p.get("scope") == "ORGANIZATION"],
        "catalog": SYSTEM_PERMISSIONS
    }


@router.get("/audit", summary="Get Platform Security Audit Logs", dependencies=[Depends(require_platform_admin)])
async def get_platform_audit_logs(db: AsyncSession = Depends(get_async_db)):
    """Fetch recent platform security events and audit logs."""
    audit_res = await db.execute(select(SecurityEvent).order_by(SecurityEvent.event_time.desc()).limit(50))
    events = audit_res.scalars().all()
    return events
