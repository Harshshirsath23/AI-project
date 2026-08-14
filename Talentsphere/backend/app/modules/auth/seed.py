import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session as SyncSession

from app.modules.organizations.models import Organization, Industry
from app.modules.auth.models import User, UserProfile, Role, Permission, RolePermission, UserRole
from app.modules.auth.constants import SYSTEM_PERMISSIONS, DEFAULT_ROLES, AccountType, AccountStatus
from app.modules.auth.security import hash_password

def seed_iam_data(db: SyncSession) -> dict:
    """Synchronous seeder populating initial permissions, system roles, master tenant, and super admin user."""
    print("[+] Seeding IAM System Permissions...")
    permission_map = {}
    
    # 1. Seed Permissions Catalog
    for p_data in SYSTEM_PERMISSIONS:
        stmt = select(Permission).where(Permission.permission_code == p_data["code"])
        perm = db.execute(stmt).scalar_one_or_none()
        if not perm:
            perm = Permission(
                permission_code=p_data["code"],
                permission_name=p_data["name"],
                module=p_data["module"],
                description=p_data.get("description")
            )
            db.add(perm)
            db.flush()
        permission_map[p_data["code"]] = perm.id
    print(f"[+] Seeded {len(permission_map)} system permissions.")

    # 1b. Seed Default Industry for Master Tenant
    stmt_ind = select(Industry).where(Industry.industry_code == "TECH")
    default_ind = db.execute(stmt_ind).scalar_one_or_none()
    if not default_ind:
        default_ind = Industry(industry_code="TECH", industry_name="Technology & Software")
        db.add(default_ind)
        db.flush()

    # 2. Seed Master Organization Tenant
    stmt_org = select(Organization).where(Organization.organization_code == "TS-MASTER")
    master_org = db.execute(stmt_org).scalar_one_or_none()
    if not master_org:
        master_org = Organization(
            organization_code="TS-MASTER",
            legal_name="TalentSphere Master Tenant Inc.",
            display_name="TalentSphere Master Tenant",
            industry_id=default_ind.id,
            subscription_plan="Enterprise",
            subscription_status="Active",
            is_active=True
        )
        db.add(master_org)
        db.flush()
    print(f"[+] Master Tenant Organization ready: ID = {master_org.id}")

    # 3. Seed System Roles
    role_map = {}
    for r_data in DEFAULT_ROLES:
        stmt_r = select(Role).where(
            Role.organization_id == master_org.id,
            Role.role_code == r_data["code"]
        )
        role = db.execute(stmt_r).scalar_one_or_none()
        if not role:
            role = Role(
                organization_id=master_org.id,
                role_code=r_data["code"],
                role_name=r_data["name"],
                description=r_data.get("description"),
                is_system_role=r_data.get("is_system_role", False)
            )
            db.add(role)
            db.flush()

            # Map Role -> Permissions
            allowed_codes = r_data["permissions"]
            if "*" in allowed_codes:
                target_p_ids = list(permission_map.values())
            else:
                target_p_ids = [permission_map[code] for code in allowed_codes if code in permission_map]

            for p_id in target_p_ids:
                stmt_rp = select(RolePermission).where(
                    RolePermission.role_id == role.id,
                    RolePermission.permission_id == p_id
                )
                if not db.execute(stmt_rp).scalar_one_or_none():
                    db.add(RolePermission(role_id=role.id, permission_id=p_id))

        role_map[r_data["code"]] = role.id
    print(f"[+] Seeded {len(DEFAULT_ROLES)} system roles and permission mappings.")

    # 4. Seed Super Admin User
    stmt_user = select(User).where(User.email == "admin@talentsphere.ai")
    admin_user = db.execute(stmt_user).scalar_one_or_none()
    if not admin_user:
        admin_user = User(
            organization_id=master_org.id,
            username="superadmin",
            email="admin@talentsphere.ai",
            phone="+1234567890",
            password_hash=hash_password("Admin@123456"),
            account_type=AccountType.SUPER_ADMIN.value,
            account_status=AccountStatus.ACTIVE.value,
            email_verified=True,
            is_active=True
        )
        db.add(admin_user)
        db.flush()

        profile = UserProfile(
            user_id=admin_user.id,
            first_name="Super",
            last_name="Admin"
        )
        db.add(profile)

        # Assign Super Admin Role
        if "SUPER_ADMIN" in role_map:
            db.add(UserRole(user_id=admin_user.id, role_id=role_map["SUPER_ADMIN"]))
            
        print("[+] Created default Super Admin account: 'admin@talentsphere.ai' (Password: 'Admin@123456')")
    else:
        print("[i] Super Admin account already exists.")

    db.commit()
    return {
        "organization_id": str(master_org.id),
        "admin_user_id": str(admin_user.id),
        "admin_email": admin_user.email
    }
