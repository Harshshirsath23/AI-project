from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.jwt import decode_token, is_token_expired
from app.authentication.service import AuthenticationService
from app.core.logging import get_logger
from app.database.connection import get_db
from app.models.organization import Organization
from app.models.user import Role, User

logger = get_logger(__name__)
security = HTTPBearer()


class AuthenticatedUser:
    """Container for authenticated user context."""

    def __init__(
        self,
        user: User,
        organization: Organization,
        role: Optional[Role],
        token_payload,
    ):
        self.user = user
        self.organization = organization
        self.role = role
        self.token_payload = token_payload


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> AuthenticatedUser:
    """
    Dependency to get the current authenticated user.
    
    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    payload = decode_token(token)

    if not payload:
        logger.warning("Invalid token provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if is_token_expired(token):
        logger.warning("Expired token provided", user_id=payload.sub)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if payload.token_type != "access":
        logger.warning("Invalid token type", token_type=payload.token_type)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user
    result = await db.execute(
        select(User).where(User.id == payload.sub)
    )
    user = result.scalar_one_or_none()

    if not user:
        logger.warning("User not found", user_id=payload.sub)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user.is_active:
        logger.warning("User account deactivated", user_id=payload.sub)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated",
        )

    # Get organization
    result = await db.execute(
        select(Organization).where(Organization.id == payload.organization_id)
    )
    organization = result.scalar_one_or_none()

    if not organization:
        logger.warning("Organization not found", organization_id=payload.organization_id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Organization not found",
        )

    if not organization.is_active:
        logger.warning("Organization deactivated", organization_id=payload.organization_id)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organization is deactivated",
        )

    # Verify user belongs to organization
    if str(user.organization_id) != payload.organization_id:
        logger.warning(
            "User does not belong to organization",
            user_id=payload.sub,
            organization_id=payload.organization_id,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not belong to this organization",
        )

    # Get role
    role = None
    if user.role_id:
        result = await db.execute(
            select(Role).where(Role.id == user.role_id)
        )
        role = result.scalar_one_or_none()

    return AuthenticatedUser(
        user=user,
        organization=organization,
        role=role,
        token_payload=payload,
    )


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    ),
    db: AsyncSession = Depends(get_db),
) -> Optional[AuthenticatedUser]:
    """
    Optional authentication dependency.
    Returns None if no valid token provided.
    """
    if not credentials:
        return None

    try:
        return await get_current_user(credentials, db)
    except HTTPException:
        return None


class OrganizationContext:
    """Container for organization-scoped context."""

    def __init__(
        self,
        user: User,
        organization: Organization,
        role: Optional[Role],
    ):
        self.user = user
        self.organization = organization
        self.role = role


async def get_organization_context(
    auth: AuthenticatedUser = Depends(get_current_user),
) -> OrganizationContext:
    """
    Dependency to get organization context for multi-tenant operations.
    
    This ensures all operations are scoped to the authenticated user's organization.
    """
    return OrganizationContext(
        user=auth.user,
        organization=auth.organization,
        role=auth.role,
    )


def require_role(*allowed_roles: str):
    """
    Dependency factory to require specific roles.
    
    Args:
        *allowed_roles: List of allowed role slugs
    """

    async def role_checker(
        auth: AuthenticatedUser = Depends(get_current_user),
    ) -> AuthenticatedUser:
        if not auth.role:
            logger.warning("User has no role assigned", user_id=auth.user.id)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No role assigned to user",
            )

        if auth.role.slug not in allowed_roles:
            logger.warning(
                "User role not authorized",
                user_id=auth.user.id,
                role_slug=auth.role.slug,
                allowed_roles=allowed_roles,
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{auth.role.slug}' is not authorized for this operation",
            )

        return auth

    return role_checker


def require_permission(*permissions: str):
    """
    Dependency factory to require specific permissions.
    
    Args:
        *permissions: List of required permissions
    """

    async def permission_checker(
        auth: AuthenticatedUser = Depends(get_current_user),
    ) -> AuthenticatedUser:
        if not auth.role:
            logger.warning("User has no role assigned", user_id=auth.user.id)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No role assigned to user",
            )

        # Parse permissions from role
        import json

        try:
            role_permissions = json.loads(auth.role.permissions or "[]")
        except json.JSONDecodeError:
            role_permissions = []

        # Check for wildcard permission
        if "*" in role_permissions:
            return auth

        # Check if user has all required permissions
        missing_permissions = [
            perm for perm in permissions if perm not in role_permissions
        ]

        if missing_permissions:
            logger.warning(
                "User lacks required permissions",
                user_id=auth.user.id,
                role_slug=auth.role.slug,
                missing_permissions=missing_permissions,
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permissions: {', '.join(missing_permissions)}",
            )

        return auth

    return permission_checker
