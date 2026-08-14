import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.modules.auth.models import User, UserProfile, Role, Permission, Session as SessionModel, RefreshToken
from app.modules.auth.schemas import (
    LoginRequest, TokenResponse, UserCreateRequest, UserResponse, UserProfileSchema,
    RoleResponse, PermissionResponse, ChangePasswordRequest
)
from app.modules.auth.repository import (
    UserRepository, RoleRepository, PermissionRepository, SessionRepository, AuditRepository
)
from app.modules.auth.security import hash_password, verify_password, hash_token, generate_random_token
from app.modules.auth.jwt import create_access_token, create_refresh_token
from app.modules.auth.exceptions import (
    InvalidCredentialsException, AccountLockedException, UserInactiveException,
    TokenExpiredException, TokenRevokedException, InvalidTokenException
)
from app.modules.auth.constants import AccountStatus, AccountType

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.session_repo = SessionRepository(db)
        self.audit_repo = AuditRepository(db)

    async def login(self, request: LoginRequest, ip: Optional[str] = None, user_agent: Optional[str] = None) -> TokenResponse:
        normalized_email = request.email.lower().strip()
        user = await self.user_repo.get_by_email(normalized_email)
        
        if not user:
            raise InvalidCredentialsException("Invalid email or password")

        # Verify Argon2id Password Hash
        if not verify_password(request.password, user.password_hash):
            await self.audit_repo.log_login(user.id, status="Failed", ip=ip, reason="Wrong password")
            await self.audit_repo.log_security_event("Failed Login", "Medium", f"Failed password attempt for {user.email}", user_id=user.id)
            raise InvalidCredentialsException("Invalid email or password")

        # Check Account Status & Flags
        if user.account_status == AccountStatus.LOCKED.value:
            raise AccountLockedException()
        if user.account_status in [AccountStatus.SUSPENDED.value, AccountStatus.DISABLED.value] or not user.is_active:
            raise UserInactiveException("Account is disabled or suspended")

        # Check Tenant Organization Status if scoped to an Organization
        if user.organization_id:
            from app.modules.organizations.models import Organization
            from sqlalchemy import select
            org_res = await self.db.execute(select(Organization).where(Organization.id == user.organization_id))
            org = org_res.scalar_one_or_none()
            if org and (org.subscription_status == "Suspended" or not org.is_active):
                raise UserInactiveException("Organization account is suspended. Contact Platform Administrator.")

        # Update Last Login
        await self.user_repo.update_last_login(user.id)
        await self.audit_repo.log_login(user.id, status="Success", ip=ip, browser=user_agent)

        # Create Session & Refresh Token
        session_token = generate_random_token(48)
        raw_refresh_token, token_hash_str = create_refresh_token()
        
        now = datetime.now(timezone.utc)
        session_expires = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        session_obj = SessionModel(
            session_token=session_token,
            user_id=user.id,
            ip_address=ip,
            login_time=now,
            expires_at=session_expires
        )
        
        refresh_token_obj = RefreshToken(
            token_hash=token_hash_str,
            expires_at=session_expires
        )
        
        await self.session_repo.create_session(session_obj, refresh_token_obj)
        await self.db.commit()

        # Generate Access Token
        access_token = create_access_token(
            user_id=user.id,
            organization_id=user.organization_id,
            account_type=user.account_type
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=raw_refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user_id=user.id,
            organization_id=user.organization_id,
            account_type=user.account_type
        )

    async def refresh(self, raw_refresh_token: str, ip: Optional[str] = None) -> TokenResponse:
        token_hash_str = hash_token(raw_refresh_token)
        rt = await self.session_repo.get_refresh_token_by_hash(token_hash_str)
        
        if not rt or rt.revoked:
            raise TokenRevokedException("Refresh token is invalid or revoked")
            
        if rt.expires_at < datetime.now(timezone.utc):
            raise TokenExpiredException("Refresh token has expired")

        # Revoke previous refresh token (Token Rotation)
        await self.session_repo.revoke_refresh_token(rt.id)
        
        session_obj = await self.session_repo.get_session_by_id(rt.session_id)
        if not session_obj or session_obj.revoked_at is not None:
            raise TokenRevokedException("Session revoked")

        user = await self.user_repo.get_by_id(session_obj.user_id)
        if not user or not user.is_active or user.is_deleted:
            raise UserInactiveException()

        # Issue new token pair (Rotation)
        new_raw_refresh, new_token_hash = create_refresh_token()
        new_rt = RefreshToken(
            session_id=session_obj.id,
            token_hash=new_token_hash,
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        self.db.add(new_rt)
        await self.db.commit()

        access_token = create_access_token(
            user_id=user.id,
            organization_id=user.organization_id,
            account_type=user.account_type
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_raw_refresh,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user_id=user.id,
            organization_id=user.organization_id,
            account_type=user.account_type
        )

    async def logout(self, user_id: uuid.UUID) -> None:
        await self.session_repo.revoke_all_user_sessions(user_id)
        await self.audit_repo.log_activity(user_id, module="auth", action="Logout")
        await self.db.commit()

    async def change_password(self, user_id: uuid.UUID, req: ChangePasswordRequest) -> None:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise InvalidTokenException()

        if not verify_password(req.old_password, user.password_hash):
            raise InvalidCredentialsException("Current password incorrect")

        new_hash = hash_password(req.new_password)
        await self.user_repo.update_password(user_id, new_hash)
        
        # Revoke active sessions on password change
        await self.session_repo.revoke_all_user_sessions(user_id)
        await self.audit_repo.log_security_event("Password Change", "Low", f"User {user.email} changed password", user_id=user_id)
        await self.db.commit()

    async def get_user_me(self, user_id: uuid.UUID) -> UserResponse:
        user = await self.user_repo.get_with_profile(user_id)
        if not user:
            raise InvalidTokenException("User profile not found")

        permissions = await self.user_repo.get_user_permissions(user_id)
        roles = await self.user_repo.get_user_roles(user_id)
        role_codes = [r.role_code for r in roles]

        profile_schema = None
        if hasattr(user, "profile_obj") and user.profile_obj:
            p = user.profile_obj
            profile_schema = UserProfileSchema(
                first_name=p.first_name,
                middle_name=p.middle_name,
                last_name=p.last_name,
                profile_photo=p.profile_photo,
                gender=p.gender,
                date_of_birth=p.date_of_birth
            )

        is_platform_admin = user.account_type in [AccountType.PLATFORM_SUPER_ADMIN.value, AccountType.SUPER_ADMIN.value] or getattr(user, "account_scope", "ORGANIZATION") == "PLATFORM"
        is_organization_admin = user.account_type in [AccountType.ORGANIZATION_SUPER_ADMIN.value, AccountType.HR_ADMIN.value] or "ORGANIZATION_SUPER_ADMIN" in role_codes
        user_scope = "PLATFORM" if is_platform_admin else "ORGANIZATION"

        return UserResponse(
            id=user.id,
            organization_id=user.organization_id,
            username=user.username,
            email=user.email,
            phone=user.phone,
            account_type=user.account_type,
            account_status=user.account_status,
            account_scope=getattr(user, "account_scope", user_scope),
            scope=user_scope,
            is_platform_admin=is_platform_admin,
            is_organization_admin=is_organization_admin,
            email_verified=user.email_verified,
            phone_verified=user.phone_verified,
            mfa_enabled=user.mfa_enabled,
            is_active=user.is_active,
            last_login_at=user.last_login_at,
            created_at=user.created_at,
            profile=profile_schema,
            roles=role_codes,
            permissions=permissions
        )


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def create_user(self, req: UserCreateRequest) -> User:
        existing = await self.user_repo.get_by_email(req.email)
        if existing:
            raise Exception(f"User with email {req.email} already exists")

        user = User(
            organization_id=req.organization_id,
            username=req.username,
            email=req.email.lower(),
            phone=req.phone,
            password_hash=hash_password(req.password),
            account_type=req.account_type,
            account_status=AccountStatus.ACTIVE.value,
            email_verified=True
        )

        profile = UserProfile(
            first_name=req.first_name,
            last_name=req.last_name
        )

        return await self.user_repo.create(user, profile)


class RoleService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.role_repo = RoleRepository(db)
        self.perm_repo = PermissionRepository(db)

    async def get_org_roles(self, org_id: uuid.UUID) -> Sequence[Role]:
        return await self.role_repo.get_all_by_org(org_id)

    async def get_all_permissions(self) -> Sequence[Permission]:
        return await self.perm_repo.get_all()
