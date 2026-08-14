import uuid
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.core.storage import storage_service
from app.modules.auth.models import Role
from app.modules.organizations.models import Organization
from app.modules.organizations.repository import (
    OrganizationRepository, BranchRepository, DepartmentRepository,
    DesignationRepository, ShiftRepository, SettingsRepository
)
from app.modules.organizations.schemas import (
    OrganizationCreate, BranchCreate, DepartmentCreate, 
    DesignationCreate, ShiftCreate
)
from app.modules.auth.repository import AuditRepository, UserRepository

class OrganizationInitializationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.org_repo = OrganizationRepository(db)
        self.branch_repo = BranchRepository(db)
        self.dept_repo = DepartmentRepository(db)
        self.desig_repo = DesignationRepository(db)
        self.shift_repo = ShiftRepository(db)
        self.settings_repo = SettingsRepository(db)
        self.audit_repo = AuditRepository(db)

    async def initialize_tenant(self, org_data: OrganizationCreate, creator_id: uuid.UUID) -> dict:
        """
        The master orchestrator for creating a new Organization.
        Scaffolds the entire tenant workspace, folders, and defaults.
        """
        # 1. Check if org code exists
        existing = await self.org_repo.get_by_code(org_data.organization_code)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Organization code already exists")

        # Fallback industry_id if default 0000... is passed
        if str(org_data.industry_id) == '00000000-0000-0000-0000-000000000000':
            ind_res = await self.db.execute(select(Organization.industry_id).where(Organization.industry_id != None).limit(1))
            fallback_ind = ind_res.scalar()
            if not fallback_ind:
                from sqlalchemy import text
                raw_ind = await self.db.execute(text("SELECT id FROM industries LIMIT 1;"))
                fallback_ind = raw_ind.scalar()
            if fallback_ind:
                org_data.industry_id = fallback_ind

        # 2. Create the Organization Record
        org = await self.org_repo.create(org_data)
        org_id = org.id

        # 3. Create Tenant Folder Structure via Storage Abstraction
        base_tenant_dir = f"organizations/{org_id}"
        storage_service.create_directory(f"{base_tenant_dir}/logo")
        storage_service.create_directory(f"{base_tenant_dir}/resumes")
        storage_service.create_directory(f"{base_tenant_dir}/job_descriptions")
        storage_service.create_directory(f"{base_tenant_dir}/offer_letters")
        storage_service.create_directory(f"{base_tenant_dir}/reports")
        storage_service.create_directory(f"{base_tenant_dir}/ai")

        # 4. Seed Default Branch (Head Office)
        head_office = await self.branch_repo.create(org_id, BranchCreate(
            branch_code="HQ-01",
            branch_name="Headquarters",
            is_head_office=True
        ))

        # 5. Seed Default Departments
        depts = ["Engineering", "Human Resources", "Sales", "Marketing", "Finance"]
        for idx, dept in enumerate(depts, 1):
            await self.dept_repo.create(org_id, DepartmentCreate(
                department_code=f"DPT-{idx:02d}",
                department_name=dept
            ))

        # 6. Seed Default Designations
        designations = [
            ("Intern", "L1", "Trainee"),
            ("Associate", "L2", "Junior"),
            ("Specialist", "L3", "Mid"),
            ("Manager", "L4", "Senior"),
            ("Director", "L5", "Lead")
        ]
        for idx, (name, grade, level) in enumerate(designations, 1):
            await self.desig_repo.create(org_id, DesignationCreate(
                designation_code=f"DSG-{idx:02d}",
                designation_name=name,
                grade=grade,
                level=level
            ))

        # 7. Seed Default Shifts
        await self.shift_repo.create(org_id, ShiftCreate(
            shift_name="General Shift",
            start_time="09:00:00",
            end_time="18:00:00",
            is_flexible=False
        ))

        # 8. Seed Default Company Settings
        defaults = {
            "timezone": "UTC",
            "date_format": "YYYY-MM-DD",
            "currency": "USD",
            "working_days": "Mon,Tue,Wed,Thu,Fri",
            "resume_max_size_mb": "5",
            "allowed_file_types": "pdf,docx",
            "default_offer_validity_days": "7"
        }
        for k, v in defaults.items():
            await self.settings_repo.update_setting(org_id, k, v)

        # 9. Seed Tenant Organization Super Admin Role & User
        org_admin_role = Role(
            organization_id=org_id,
            role_code="ORGANIZATION_SUPER_ADMIN",
            role_name="Organization Super Administrator",
            scope="ORGANIZATION",
            description="Full tenant-scoped administrator",
            is_system_role=True
        )
        self.db.add(org_admin_role)
        await self.db.flush()

        admin_email = (org_data.admin_email or f"admin@{org_data.organization_code.lower()}.com").lower().strip()
        admin_first = org_data.admin_first_name or "Org"
        admin_last = org_data.admin_last_name or "Admin"
        raw_pwd = org_data.admin_password or "Password123!"
        
        # Check if user email exists
        user_repo = UserRepository(self.db)
        existing_user = await user_repo.get_by_email(admin_email)
        admin_user_info = None

        from app.modules.auth.security import hash_password
        from app.modules.auth.models import User, UserProfile, UserRole

        pwd_hash = hash_password(raw_pwd)

        if existing_user:
            existing_user.password_hash = pwd_hash
            existing_user.account_type = "ORGANIZATION_SUPER_ADMIN"
            existing_user.account_scope = "ORGANIZATION"
            existing_user.account_status = "Active"
            existing_user.is_active = True
            existing_user.organization_id = org_id

            # Ensure role assignment
            role_res = await self.db.execute(
                select(UserRole).where(UserRole.user_id == existing_user.id, UserRole.role_id == org_admin_role.id)
            )
            if not role_res.scalar_one_or_none():
                db_ur = UserRole(user_id=existing_user.id, role_id=org_admin_role.id)
                self.db.add(db_ur)

            await self.db.flush()
            admin_user_info = {
                "user_id": str(existing_user.id),
                "email": existing_user.email,
                "role": "ORGANIZATION_SUPER_ADMIN",
                "temporary_password": raw_pwd
            }
        else:
            admin_user = User(
                organization_id=org_id,
                username=admin_email,
                email=admin_email,
                password_hash=pwd_hash,
                account_type="ORGANIZATION_SUPER_ADMIN",
                account_status="Active",
                account_scope="ORGANIZATION",
                email_verified=True,
                is_active=True
            )
            profile = UserProfile(
                first_name=admin_first,
                last_name=admin_last
            )
            created_admin = await user_repo.create(admin_user, profile)
            
            # Assign ORGANIZATION_SUPER_ADMIN role
            user_role = UserRole(
                user_id=created_admin.id,
                role_id=org_admin_role.id
            )
            self.db.add(user_role)
            await self.db.flush()

            admin_user_info = {
                "user_id": str(created_admin.id),
                "email": created_admin.email,
                "role": "ORGANIZATION_SUPER_ADMIN",
                "temporary_password": raw_pwd
            }

        # 10. Audit Log
        await self.audit_repo.log_security_event(
            event_type="ORGANIZATION_INITIALIZED",
            severity="INFO",
            description=f"Tenant scaffolding completed for Org {org.organization_code} with Org Super Admin {admin_email}",
            user_id=creator_id
        )

        await self.db.commit()

        return {
            "status": "success",
            "organization_id": org_id,
            "organization_name": org.display_name,
            "admin_user": admin_user_info,
            "message": "Organization scaffolded successfully with Organization Super Admin provisioned."
        }
