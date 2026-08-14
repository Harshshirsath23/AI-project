import uuid
from typing import List
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_async_db
from app.modules.auth.models import User
from app.modules.auth.schemas import (
    LoginRequest, TokenResponse, RefreshRequest, LogoutResponse,
    UserResponse, UserCreateRequest, ChangePasswordRequest,
    RoleResponse, PermissionResponse, RoleCreateRequest
)
from app.modules.auth.service import AuthService, UserService, RoleService
from app.modules.auth.dependencies import (
    get_current_user, get_current_organization, require_permission, require_role
)

router = APIRouter(prefix="/auth", tags=["Identity & Access Management (IAM)"])

# -------------------------
# Public Authentication APIs
# -------------------------
@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    req: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_async_db)
):
    """Authenticate user with email and password, returning JWT access & refresh tokens."""
    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    
    auth_service = AuthService(db)
    return await auth_service.login(req, ip=client_ip, user_agent=user_agent)


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh_token(
    req: RefreshRequest,
    request: Request,
    db: AsyncSession = Depends(get_async_db)
):
    """Rotate refresh token and issue a new JWT access token."""
    client_ip = request.client.host if request.client else None
    auth_service = AuthService(db)
    return await auth_service.refresh(req.refresh_token, ip=client_ip)


# -------------------------
# Protected User APIs
# -------------------------
@router.post("/logout", response_model=LogoutResponse, status_code=status.HTTP_200_OK)
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Revoke all active sessions for the current user."""
    auth_service = AuthService(db)
    await auth_service.logout(current_user.id)
    return LogoutResponse()


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_me(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Fetch profile, assigned roles, and permission codes for the logged-in user."""
    auth_service = AuthService(db)
    return await auth_service.get_user_me(current_user.id)


@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    req: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Change account password and revoke existing sessions."""
    auth_service = AuthService(db)
    await auth_service.change_password(current_user.id, req)
    return {"message": "Password updated successfully. Please log in again with your new password."}


# -------------------------
# Admin User & Role Management APIs
# -------------------------
@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    req: UserCreateRequest,
    current_user: User = Depends(require_permission("users:write")),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new user account (Requires 'users:write' permission)."""
    user_service = UserService(db)
    new_user = await user_service.create_user(req)
    auth_service = AuthService(db)
    return await auth_service.get_user_me(new_user.id)


@router.get("/roles", response_model=List[RoleResponse], status_code=status.HTTP_200_OK)
async def get_roles(
    org_id: uuid.UUID = Depends(get_current_organization),
    current_user: User = Depends(require_permission("roles:manage")),
    db: AsyncSession = Depends(get_async_db)
):
    """List all available system and organization roles (Requires 'roles:manage' permission)."""
    role_service = RoleService(db)
    roles = await role_service.get_org_roles(org_id)
    return roles


@router.get("/permissions", response_model=List[PermissionResponse], status_code=status.HTTP_200_OK)
async def get_permissions(
    current_user: User = Depends(require_permission("roles:manage")),
    db: AsyncSession = Depends(get_async_db)
):
    """List all available system permissions (Requires 'roles:manage' permission)."""
    role_service = RoleService(db)
    perms = await role_service.get_all_permissions()
    return perms
