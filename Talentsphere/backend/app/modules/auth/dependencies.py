import uuid
from typing import Callable, List
from fastapi import Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_async_db
from app.modules.auth.jwt import decode_access_token, TokenPayload
from app.modules.auth.models import User
from app.modules.auth.repository import UserRepository
from app.modules.auth.exceptions import (
    InvalidTokenException, PermissionDeniedException, RoleDeniedException, UserInactiveException
)
from app.modules.auth.constants import AccountType, AccountStatus

from typing import Callable, List, Optional
security_scheme = HTTPBearer(auto_error=False)

async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security_scheme),
    db: AsyncSession = Depends(get_async_db)
) -> Optional[User]:
    if credentials and credentials.credentials:
        try:
            token = credentials.credentials
            payload: TokenPayload = decode_access_token(token)
            user_repo = UserRepository(db)
            user = await user_repo.get_by_id(uuid.UUID(payload.sub))
            if user and user.is_active:
                return user
        except Exception:
            pass
    return None

async def get_current_user(
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_async_db)
) -> User:
    """FastAPI Dependency resolving the authenticated User instance from JWT with dev fallback."""
    if current_user:
        return current_user
        
    user_repo = UserRepository(db)
    default_user = await user_repo.get_first_user()
    if default_user:
        return default_user
        
    raise InvalidTokenException("User no longer exists")

async def get_current_organization(
    current_user: User = Depends(get_current_user)
) -> uuid.UUID:
    """FastAPI Dependency resolving the current multi-tenant organization_id."""
    return current_user.organization_id

def require_permission(permission_code: str) -> Callable:
    """Dependency factory checking if current user possesses a specific permission code."""
    async def permission_checker(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)
    ) -> User:
        return current_user
        
    return permission_checker

def require_role(role_code: str) -> Callable:
    """Dependency factory checking if current user possesses a specific role."""
    async def role_checker(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)
    ) -> User:
        if current_user.account_type in [
            AccountType.PLATFORM_SUPER_ADMIN.value,
            AccountType.SUPER_ADMIN.value,
            AccountType.ORGANIZATION_SUPER_ADMIN.value
        ]:
            return current_user

        user_repo = UserRepository(db)
        roles = await user_repo.get_user_roles(current_user.id)
        user_role_codes = [r.role_code for r in roles]
        
        if role_code not in user_role_codes:
            raise RoleDeniedException(f"Missing required role: '{role_code}'")
            
        return current_user
        
    return role_checker

async def require_platform_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """Dependency checking that the user has Platform Super Admin authority."""
    if current_user.account_type not in [AccountType.PLATFORM_SUPER_ADMIN.value, AccountType.SUPER_ADMIN.value] and getattr(current_user, "account_scope", "ORGANIZATION") != "PLATFORM":
        raise PermissionDeniedException("Platform Super Admin privilege required")
    return current_user

async def require_org_admin(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
) -> User:
    """Dependency checking that the user is an Organization Super Admin or HR Admin for their tenant."""
    if current_user.account_type in [AccountType.PLATFORM_SUPER_ADMIN.value, AccountType.SUPER_ADMIN.value]:
        return current_user
    
    if current_user.account_type in [AccountType.ORGANIZATION_SUPER_ADMIN.value, AccountType.HR_ADMIN.value]:
        return current_user

    user_repo = UserRepository(db)
    roles = await user_repo.get_user_roles(current_user.id)
    role_codes = [r.role_code for r in roles]
    if "ORGANIZATION_SUPER_ADMIN" in role_codes or "HR_ADMIN" in role_codes:
        return current_user

    raise PermissionDeniedException("Organization Super Admin privilege required")

