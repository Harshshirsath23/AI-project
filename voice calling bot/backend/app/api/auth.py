from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.dependencies import (
    AuthenticatedUser,
    get_current_user,
    get_organization_context,
)
from app.authentication.jwt import get_token_expiration
from app.authentication.service import AuthenticationService
from app.config.settings import get_settings
from app.core.logging import get_logger
from app.database.connection import get_db
from app.schemas.auth import (
    CurrentUserResponse,
    LoginRequest,
    LogoutResponse,
    PasswordChangeRequest,
    PasswordResetConfirm,
    PasswordResetRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

logger = get_logger(__name__)
settings = get_settings()
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new user and create an organization.
    
    This endpoint creates both a new organization and the first user (admin).
    """
    auth_service = AuthenticationService(db)

    try:
        user, organization = await auth_service.register_user(
            email=request.email,
            password=request.password,
            first_name=request.first_name,
            last_name=request.last_name,
            organization_name=request.organization_name,
            organization_slug=request.organization_slug,
        )

        # Auto-login after registration
        access_token, refresh_token, _, _, _ = await auth_service.login(
            email=request.email,
            password=request.password,
        )

        expires_in = settings.access_token_expire_minutes * 60

        logger.info(
            "User registered successfully",
            user_id=user.id,
            email=request.email,
            organization_id=organization.id,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=expires_in,
        )

    except ValueError as e:
        logger.warning("Registration failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Authenticate a user and return access and refresh tokens.
    """
    auth_service = AuthenticationService(db)

    try:
        access_token, refresh_token, user, organization, role = await auth_service.login(
            email=request.email,
            password=request.password,
            organization_slug=request.organization_slug,
        )

        expires_in = settings.access_token_expire_minutes * 60

        logger.info(
            "User logged in successfully",
            user_id=user.id,
            email=request.email,
            organization_id=organization.id,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=expires_in,
        )

    except ValueError as e:
        logger.warning("Login failed", email=request.email, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Refresh access and refresh tokens using a valid refresh token.
    
    Implements token rotation for enhanced security.
    """
    auth_service = AuthenticationService(db)

    try:
        access_token, new_refresh_token, expire = await auth_service.refresh_tokens(
            request.refresh_token
        )

        expires_in = int((expire - expire.replace(tzinfo=None)).total_seconds())

        logger.info("Token refreshed successfully")

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=expires_in,
        )

    except ValueError as e:
        logger.warning("Token refresh failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post("/logout", response_model=LogoutResponse)
async def logout(
    auth: AuthenticatedUser = Depends(get_current_user),
):
    """
    Logout the current user.
    
    Note: In a production environment, you would add the refresh token
    to a blacklist in Redis to prevent reuse.
    """
    # In production, add refresh token to blacklist
    # For now, client-side token deletion is sufficient
    logger.info(
        "User logged out",
        user_id=auth.user.id,
        email=auth.user.email,
    )

    return LogoutResponse(message="Successfully logged out")


@router.get("/me", response_model=CurrentUserResponse)
async def get_current_user_info(
    auth: AuthenticatedUser = Depends(get_current_user),
):
    """
    Get information about the currently authenticated user.
    """
    import json

    permissions = []
    if auth.role:
        try:
            permissions = json.loads(auth.role.permissions or "[]")
        except json.JSONDecodeError:
            permissions = []

    return CurrentUserResponse(
        user=UserResponse.model_validate(auth.user),
        organization_id=str(auth.organization.id),
        organization_name=auth.organization.name,
        organization_slug=auth.organization.slug,
        role_id=str(auth.role.id) if auth.role else "",
        role_name=auth.role.name if auth.role else "",
        role_slug=auth.role.slug if auth.role else "",
        permissions=permissions,
    )


@router.post("/change-password")
async def change_password(
    request: PasswordChangeRequest,
    auth: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Change the current user's password.
    """
    auth_service = AuthenticationService(db)

    try:
        await auth_service.change_password(
            user_id=str(auth.user.id),
            current_password=request.current_password,
            new_password=request.new_password,
        )

        logger.info(
            "Password changed successfully",
            user_id=auth.user.id,
        )

        return {"message": "Password changed successfully"}

    except ValueError as e:
        logger.warning("Password change failed", user_id=auth.user.id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/reset-password")
async def request_password_reset(
    request: PasswordResetRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Request a password reset.
    
    In production, this would send an email with a reset link.
    For now, it returns the token for testing purposes.
    """
    auth_service = AuthenticationService(db)

    reset_token = await auth_service.initiate_password_reset(request.email)

    if reset_token:
        logger.info(
            "Password reset initiated",
            email=request.email,
        )
        # In production, send email with reset link
        return {
            "message": "Password reset initiated. Check your email for reset instructions.",
            "token": reset_token,  # Only for testing - remove in production
        }
    else:
        # Don't reveal if email exists
        return {
            "message": "If the email exists, password reset instructions have been sent.",
        }


@router.post("/reset-password/confirm")
async def confirm_password_reset(
    request: PasswordResetConfirm,
    db: AsyncSession = Depends(get_db),
):
    """
    Confirm password reset with token.
    """
    auth_service = AuthenticationService(db)

    try:
        await auth_service.confirm_password_reset(
            token=request.token,
            new_password=request.new_password,
        )

        logger.info("Password reset confirmed")

        return {"message": "Password reset successfully"}

    except ValueError as e:
        logger.warning("Password reset confirmation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
