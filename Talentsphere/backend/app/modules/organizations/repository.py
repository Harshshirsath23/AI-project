import uuid
from typing import Optional, List
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.organizations.models import (
    Organization, Branch, Department, Designation, Shift
)
from app.modules.platform.models import OrganizationSetting
from app.modules.organizations.schemas import (
    OrganizationCreate, OrganizationUpdate,
    BranchCreate, BranchUpdate,
    DepartmentCreate, DepartmentUpdate,
    DesignationCreate, DesignationUpdate,
    ShiftCreate, ShiftUpdate
)

class OrganizationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, org_id: uuid.UUID) -> Optional[Organization]:
        stmt = select(Organization).where(Organization.id == org_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
        
    async def get_all(self) -> List[Organization]:
        stmt = select(Organization).order_by(Organization.created_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
        
    async def get_by_code(self, code: str) -> Optional[Organization]:
        stmt = select(Organization).where(Organization.organization_code == code)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, data: OrganizationCreate) -> Organization:
        raw_data = data.model_dump()
        admin_keys = {'admin_email', 'admin_first_name', 'admin_last_name', 'admin_password'}
        org_payload = {k: v for k, v in raw_data.items() if k not in admin_keys}
        org = Organization(**org_payload)
        self.db.add(org)
        await self.db.flush()
        return org

    async def update(self, org_id: uuid.UUID, data: OrganizationUpdate) -> Optional[Organization]:
        update_data = {k: v for k, v in data.model_dump(exclude_unset=True).items() if v is not None}
        if not update_data:
            return await self.get_by_id(org_id)
            
        stmt = update(Organization).where(Organization.id == org_id).values(**update_data)
        await self.db.execute(stmt)
        return await self.get_by_id(org_id)

class BranchRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, org_id: uuid.UUID, branch_id: uuid.UUID) -> Optional[Branch]:
        stmt = select(Branch).where(Branch.id == branch_id, Branch.organization_id == org_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, org_id: uuid.UUID) -> List[Branch]:
        stmt = select(Branch).where(Branch.organization_id == org_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, org_id: uuid.UUID, data: BranchCreate) -> Branch:
        branch = Branch(**data.model_dump(), organization_id=org_id)
        self.db.add(branch)
        await self.db.flush()
        return branch

class DepartmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, org_id: uuid.UUID) -> List[Department]:
        stmt = select(Department).where(Department.organization_id == org_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, org_id: uuid.UUID, data: DepartmentCreate) -> Department:
        dept = Department(**data.model_dump(), organization_id=org_id)
        self.db.add(dept)
        await self.db.flush()
        return dept

class DesignationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, org_id: uuid.UUID) -> List[Designation]:
        stmt = select(Designation).where(Designation.organization_id == org_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, org_id: uuid.UUID, data: DesignationCreate) -> Designation:
        desig = Designation(**data.model_dump(), organization_id=org_id)
        self.db.add(desig)
        await self.db.flush()
        return desig

class ShiftRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, org_id: uuid.UUID) -> List[Shift]:
        stmt = select(Shift).where(Shift.organization_id == org_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, org_id: uuid.UUID, data: ShiftCreate) -> Shift:
        shift = Shift(**data.model_dump(), organization_id=org_id)
        self.db.add(shift)
        await self.db.flush()
        return shift

class SettingsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_settings(self, org_id: uuid.UUID) -> List[OrganizationSetting]:
        stmt = select(OrganizationSetting).where(OrganizationSetting.organization_id == org_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def update_setting(self, org_id: uuid.UUID, key: str, value: str) -> None:
        # Upsert logic
        stmt = select(OrganizationSetting).where(
            OrganizationSetting.organization_id == org_id,
            OrganizationSetting.setting_key == key
        )
        res = await self.db.execute(stmt)
        setting = res.scalar_one_or_none()
        
        if setting:
            setting.setting_value = value
        else:
            new_setting = OrganizationSetting(
                organization_id=org_id,
                setting_key=key,
                setting_value=value
            )
            self.db.add(new_setting)
        await self.db.flush()
