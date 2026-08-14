import uuid
from typing import Optional, List, Sequence
from datetime import datetime, timezone
from sqlalchemy import select, update, delete, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.auth.models import (
    User, UserProfile, Role, Permission, RolePermission, UserRole,
    Session, RefreshToken, PasswordHistory, PasswordResetToken,
    LoginHistory, SecurityEvent, ActivityLog
)

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = (
            select(User)
            .where(User.email == email.lower(), User.is_deleted == False)
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username, User.is_deleted == False)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        stmt = select(User).where(User.id == user_id, User.is_deleted == False)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_first_user(self) -> Optional[User]:
        stmt = select(User).where(User.is_deleted == False).limit(1)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_with_profile(self, user_id: uuid.UUID) -> Optional[User]:
        stmt = select(User).where(User.id == user_id, User.is_deleted == False)
        res = await self.db.execute(stmt)
        user = res.scalar_one_or_none()
        if user:
            # fetch profile
            stmt_prof = select(UserProfile).where(UserProfile.user_id == user_id)
            res_prof = await self.db.execute(stmt_prof)
            user.profile_obj = res_prof.scalar_one_or_none()
        return user

    async def create(self, user: User, profile: Optional[UserProfile] = None) -> User:
        self.db.add(user)
        await self.db.flush()
        if profile:
            profile.user_id = user.id
            self.db.add(profile)
            await self.db.flush()
        return user

    async def update_last_login(self, user_id: uuid.UUID) -> None:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(last_login_at=datetime.now(timezone.utc))
        )
        await self.db.execute(stmt)

    async def update_password(self, user_id: uuid.UUID, new_hash: str) -> None:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(password_hash=new_hash, version=User.version + 1)
        )
        await self.db.execute(stmt)
        # Log password history
        pw_hist = PasswordHistory(user_id=user_id, password_hash=new_hash)
        self.db.add(pw_hist)

    async def get_user_permissions(self, user_id: uuid.UUID) -> List[str]:
        # Select all permissions assigned to user's roles
        stmt = (
            select(Permission.permission_code)
            .join(RolePermission, Permission.id == RolePermission.permission_id)
            .join(UserRole, RolePermission.role_id == UserRole.role_id)
            .where(UserRole.user_id == user_id, UserRole.is_deleted == False)
        )
        res = await self.db.execute(stmt)
        return list(set(res.scalars().all()))

    async def get_user_roles(self, user_id: uuid.UUID) -> List[Role]:
        stmt = (
            select(Role)
            .join(UserRole, Role.id == UserRole.role_id)
            .where(UserRole.user_id == user_id, Role.is_deleted == False)
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())


class RoleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_code(self, org_id: uuid.UUID, role_code: str) -> Optional[Role]:
        stmt = select(Role).where(
            Role.organization_id == org_id,
            Role.role_code == role_code,
            Role.is_deleted == False
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_all_by_org(self, org_id: uuid.UUID) -> Sequence[Role]:
        stmt = select(Role).where(
            or_(Role.organization_id == org_id, Role.is_system_role == True),
            Role.is_deleted == False
        )
        res = await self.db.execute(stmt)
        return res.scalars().all()

    async def create_role(self, role: Role, permission_ids: List[uuid.UUID] = []) -> Role:
        self.db.add(role)
        await self.db.flush()
        for p_id in permission_ids:
            rp = RolePermission(role_id=role.id, permission_id=p_id)
            self.db.add(rp)
        return role

    async def assign_role_to_user(self, user_id: uuid.UUID, role_id: uuid.UUID, assigned_by: Optional[uuid.UUID] = None) -> UserRole:
        ur = UserRole(user_id=user_id, role_id=role_id, assigned_by=assigned_by)
        self.db.add(ur)
        return ur


class PermissionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[Permission]:
        stmt = select(Permission).where(Permission.is_deleted == False)
        res = await self.db.execute(stmt)
        return res.scalars().all()

    async def get_by_code(self, code: str) -> Optional[Permission]:
        stmt = select(Permission).where(Permission.permission_code == code, Permission.is_deleted == False)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def create_permission(self, permission: Permission) -> Permission:
        self.db.add(permission)
        return permission


class SessionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_session(self, session_obj: Session, refresh_token_obj: RefreshToken) -> Session:
        self.db.add(session_obj)
        await self.db.flush()
        refresh_token_obj.session_id = session_obj.id
        self.db.add(refresh_token_obj)
        return session_obj

    async def get_session_by_id(self, session_id: uuid.UUID) -> Optional[Session]:
        stmt = select(Session).where(Session.id == session_id, Session.is_deleted == False)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_refresh_token_by_hash(self, token_hash: str) -> Optional[RefreshToken]:
        stmt = select(RefreshToken).where(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked == False,
            RefreshToken.is_deleted == False
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def revoke_refresh_token(self, token_id: uuid.UUID) -> None:
        stmt = update(RefreshToken).where(RefreshToken.id == token_id).values(revoked=True)
        await self.db.execute(stmt)

    async def revoke_session(self, session_id: uuid.UUID) -> None:
        now = datetime.now(timezone.utc)
        stmt = update(Session).where(Session.id == session_id).values(revoked_at=now)
        await self.db.execute(stmt)

    async def revoke_all_user_sessions(self, user_id: uuid.UUID) -> None:
        now = datetime.now(timezone.utc)
        stmt = update(Session).where(Session.user_id == user_id, Session.revoked_at == None).values(revoked_at=now)
        await self.db.execute(stmt)


class AuditRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_login(self, user_id: uuid.UUID, status: str, ip: Optional[str] = None, browser: Optional[str] = None, os_info: Optional[str] = None, reason: Optional[str] = None):
        history = LoginHistory(
            user_id=user_id,
            login_status=status,
            ip_address=ip,
            browser=browser[:500] if browser else None,
            operating_system=os_info[:500] if os_info else None,
            failure_reason=reason[:255] if reason else None
        )
        self.db.add(history)

    async def log_security_event(self, event_type: str, severity: str, description: str, user_id: Optional[uuid.UUID] = None):
        event = SecurityEvent(
            user_id=user_id,
            event_type=event_type,
            severity=severity,
            description=description
        )
        self.db.add(event)

    async def log_activity(self, user_id: uuid.UUID, module: str, action: str, entity_type: Optional[str] = None, entity_id: Optional[uuid.UUID] = None, ip: Optional[str] = None):
        activity = ActivityLog(
            user_id=user_id,
            module=module,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            ip_address=ip
        )
        self.db.add(activity)
