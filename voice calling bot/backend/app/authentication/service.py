from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
    is_token_expired,
)
from app.authentication.security import (
    generate_reset_token,
    hash_password,
    validate_password_strength,
    verify_password,
)
from app.config.settings import get_settings
from app.core.logging import get_logger
from app.models.organization import Organization
from app.models.user import Role, User

logger = get_logger(__name__)
settings = get_settings()


class AuthenticationService:
    """Service for authentication operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        organization_name: str,
        organization_slug: str,
    ) -> tuple[User, Organization]:
        """
        Register a new user and create an organization.
        
        Returns:
            tuple: (user, organization)
        """
        # Validate password strength
        is_valid, error_msg = validate_password_strength(password)
        if not is_valid:
            raise ValueError(error_msg)

        # Check if organization slug already exists
        result = await self.db.execute(
            select(Organization).where(Organization.slug == organization_slug)
        )
        if result.scalar_one_or_none():
            raise ValueError("Organization slug already exists")

        # Check if email already exists
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        if result.scalar_one_or_none():
            raise ValueError("Email already registered")

        # Create organization
        organization = Organization(
            name=organization_name,
            slug=organization_slug,
            is_active=True,
        )
        self.db.add(organization)
        await self.db.flush()

        # Create default role (Organization Admin)
        role = Role(
            name="Organization Admin",
            slug="org_admin",
            description="Organization administrator with full access",
            permissions='["*"]',  # Full permissions
            is_system=False,
        )
        self.db.add(role)
        await self.db.flush()

        # Create user
        hashed_password = hash_password(password)
        user = User(
            organization_id=organization.id,
            role_id=role.id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password_hash=hashed_password,  # Will be added to model
            is_active=True,
            is_verified=False,
            timezone="UTC",
            locale="en-US",
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        logger.info(
            "User registered successfully",
            user_id=user.id,
            email=email,
            organization_id=organization.id,
        )

        return user, organization

    async def login(
        self,
        email: str,
        password: str,
        organization_slug: Optional[str] = None,
    ) -> tuple[str, str, User, Organization, Role]:
        """
        Authenticate a user and return tokens.
        
        Returns:
            tuple: (access_token, refresh_token, user, organization, role)
        """
        # Find user by email
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise ValueError("Invalid credentials")

        # Check if user is active
        if not user.is_active:
            raise ValueError("User account is deactivated")

        # Verify password
        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        # Get organization
        result = await self.db.execute(
            select(Organization).where(Organization.id == user.organization_id)
        )
        organization = result.scalar_one_or_none()

        if not organization or not organization.is_active:
            raise ValueError("Organization is not active")

        # Check organization slug if provided
        if organization_slug and organization.slug != organization_slug:
            raise ValueError("Organization not found")

        # Get role
        result = await self.db.execute(
            select(Role).where(Role.id == user.role_id)
        )
        role = result.scalar_one_or_none()

        # Update last login
        user.last_login_at = datetime.utcnow()
        await self.db.commit()

        # Create tokens
        access_token, access_expire = create_access_token(
            user_id=str(user.id),
            email=user.email,
            organization_id=str(organization.id),
            role_id=str(role.id if role else ""),
        )

        refresh_token, refresh_expire = create_refresh_token(
            user_id=str(user.id),
            email=user.email,
            organization_id=str(organization.id),
            role_id=str(role.id if role else ""),
        )

        logger.info(
            "User logged in successfully",
            user_id=user.id,
            email=email,
            organization_id=organization.id,
        )

        return access_token, refresh_token, user, organization, role

    async def refresh_tokens(
        self, refresh_token: str
    ) -> tuple[str, str, datetime]:
        """
        Refresh access and refresh tokens.
        
        Returns:
            tuple: (new_access_token, new_refresh_token, expiration)
        """
        # Decode refresh token
        payload = decode_token(refresh_token)
        if not payload:
            raise ValueError("Invalid refresh token")

        if payload.token_type != "refresh":
            raise ValueError("Invalid token type")

        if is_token_expired(refresh_token):
            raise ValueError("Refresh token expired")

        # Verify user still exists and is active
        result = await self.db.execute(
            select(User).where(User.id == payload.sub)
        )
        user = result.scalar_one_or_none()

        if not user or not user.is_active:
            raise ValueError("User not found or inactive")

        # Verify organization is active
        result = await self.db.execute(
            select(Organization).where(Organization.id == payload.organization_id)
        )
        organization = result.scalar_one_or_none()

        if not organization or not organization.is_active:
            raise ValueError("Organization not found or inactive")

        # Create new tokens (token rotation)
        access_token, access_expire = create_access_token(
            user_id=payload.sub,
            email=payload.email,
            organization_id=payload.organization_id,
            role_id=payload.role_id,
        )

        new_refresh_token, refresh_expire = create_refresh_token(
            user_id=payload.sub,
            email=payload.email,
            organization_id=payload.organization_id,
            role_id=payload.role_id,
        )

        logger.info(
            "Tokens refreshed successfully",
            user_id=payload.sub,
            organization_id=payload.organization_id,
        )

        return access_token, new_refresh_token, access_expire

    async def change_password(
        self, user_id: str, current_password: str, new_password: str
    ) -> None:
        """Change user password."""
        # Validate new password strength
        is_valid, error_msg = validate_password_strength(new_password)
        if not is_valid:
            raise ValueError(error_msg)

        # Get user
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise ValueError("User not found")

        # Verify current password
        if not verify_password(current_password, user.password_hash):
            raise ValueError("Current password is incorrect")

        # Hash new password
        user.password_hash = hash_password(new_password)
        await self.db.commit()

        logger.info(
            "Password changed successfully",
            user_id=user_id,
        )

    async def initiate_password_reset(self, email: str) -> Optional[str]:
        """
        Initiate password reset process.
        
        Returns:
            Optional[str]: Reset token if user found, None otherwise
        """
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        if not user:
            # Don't reveal if email exists
            return None

        # Generate reset token
        reset_token = generate_reset_token()

        # Store reset token (would typically be stored in Redis or a separate table)
        # For now, we'll log it (in production, this would be sent via email)
        logger.info(
            "Password reset initiated",
            user_id=user.id,
            email=email,
            reset_token=reset_token,
        )

        return reset_token

    async def confirm_password_reset(
        self, token: str, new_password: str
    ) -> None:
        """Confirm password reset with token."""
        # Validate new password strength
        is_valid, error_msg = validate_password_strength(new_password)
        if not is_valid:
            raise ValueError(error_msg)

        # In production, this would validate the token from Redis or database
        # For now, this is a placeholder for the architecture
        logger.info(
            "Password reset confirmation",
            token=token[:10] + "...",  # Log partial token for security
        )

        raise NotImplementedError(
            "Password reset confirmation requires token storage implementation"
        )

    async def get_current_user(
        self, user_id: str, organization_id: str
    ) -> tuple[User, Organization, Role]:
        """
        Get current user with organization and role.
        
        Returns:
            tuple: (user, organization, role)
        """
        # Get user
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise ValueError("User not found")

        # Verify user belongs to organization
        if str(user.organization_id) != organization_id:
            raise ValueError("User does not belong to this organization")

        # Get organization
        result = await self.db.execute(
            select(Organization).where(Organization.id == organization_id)
        )
        organization = result.scalar_one_or_none()

        if not organization:
            raise ValueError("Organization not found")

        # Get role
        result = await self.db.execute(
            select(Role).where(Role.id == user.role_id)
        )
        role = result.scalar_one_or_none()

        return user, organization, role
