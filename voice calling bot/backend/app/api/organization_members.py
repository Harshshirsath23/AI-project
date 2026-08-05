from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.authentication.dependencies import (
    AuthenticatedUser,
    get_organization_context,
    require_permission,
)
from app.authentication.security import hash_password, validate_password_strength
from app.core.logging import get_logger
from app.database.connection import get_db
from app.models.user import Role, User
from app.schemas.organization_member import (
    OrganizationMemberCreate,
    OrganizationMemberResponse,
    OrganizationMemberUpdate,
)

logger = get_logger(__name__)
router = APIRouter(prefix="/organizations/members", tags=["Organization Members"])


@router.get("", response_model=list[OrganizationMemberResponse])
async def list_members(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    role_id: Optional[str] = Query(None),
    org_context: AuthenticatedUser = Depends(get_organization_context),
    db: AsyncSession = Depends(get_db),
):
    """
    List all members of the current organization.
    """
    # Build base query with organization scoping
    query = (
        select(User)
        .where(User.organization_id == org_context.organization.id)
        .options(selectinload(User.role))
    )

    # Apply filters
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            User.email.ilike(search_pattern)
            | User.first_name.ilike(search_pattern)
            | User.last_name.ilike(search_pattern)
        )

    if is_active is not None:
        query = query.where(User.is_active == is_active)

    if role_id:
        query = query.where(User.role_id == role_id)

    # Apply soft delete filter
    query = query.where(User.deleted_at.is_(None))

    # Apply pagination
    query = query.order_by(User.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    users = result.scalars().all()

    logger.info(
        "Organization members listed",
        organization_id=org_context.organization.id,
        page=page,
        page_size=page_size,
    )

    return [
        OrganizationMemberResponse(
            user_id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            avatar_url=user.avatar_url,
            job_title=user.job_title,
            department=user.department,
            role_id=str(user.role_id) if user.role_id else "",
            role_name=user.role.name if user.role else "",
            role_slug=user.role.slug if user.role else "",
            is_active=user.is_active,
            is_verified=user.is_verified,
            joined_at=user.created_at,
        )
        for user in users
    ]


@router.post("", response_model=OrganizationMemberResponse, status_code=status.HTTP_201_CREATED)
async def add_member(
    member_data: OrganizationMemberCreate,
    org_context: AuthenticatedUser = Depends(require_permission("manage_users")),
    db: AsyncSession = Depends(get_db),
):
    """
    Add a new member to the organization.
    
    Note: This creates a user with a temporary password.
    In production, you would send an email with a password reset link.
    """
    # Check if email already exists in organization
    result = await db.execute(
        select(User)
        .where(User.email == member_data.email)
        .where(User.organization_id == org_context.organization.id)
        .where(User.deleted_at.is_(None))
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists in organization",
        )

    # Verify role exists
    result = await db.execute(
        select(Role).where(Role.id == member_data.role_id)
    )
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role not found",
        )

    # Generate temporary password
    import secrets
    temp_password = secrets.token_urlsafe(16)

    # Create user
    hashed_password = hash_password(temp_password)
    user = User(
        organization_id=org_context.organization.id,
        role_id=member_data.role_id,
        email=member_data.email,
        password_hash=hashed_password,
        first_name="",  # Will be filled when user accepts invite
        last_name="",
        job_title=member_data.job_title,
        department=member_data.department,
        timezone="UTC",
        locale="en-US",
        is_active=True,
        is_verified=False,
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Load role for response
    await db.refresh(user, ["role"])

    logger.info(
        "Organization member added",
        user_id=user.id,
        email=member_data.email,
        organization_id=org_context.organization.id,
    )

    # In production, send email with password reset link
    # For now, return the temporary password for testing
    return OrganizationMemberResponse(
        user_id=str(user.id),
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        avatar_url=user.avatar_url,
        job_title=user.job_title,
        department=user.department,
        role_id=str(user.role_id) if user.role_id else "",
        role_name=user.role.name if user.role else "",
        role_slug=user.role.slug if user.role else "",
        is_active=user.is_active,
        is_verified=user.is_verified,
        joined_at=user.created_at,
    )


@router.put("/{user_id}", response_model=OrganizationMemberResponse)
async def update_member(
    user_id: str,
    member_data: OrganizationMemberUpdate,
    org_context: AuthenticatedUser = Depends(require_permission("manage_users")),
    db: AsyncSession = Depends(get_db),
):
    """
    Update a member's role and information.
    """
    result = await db.execute(
        select(User)
        .where(User.id == user_id)
        .where(User.organization_id == org_context.organization.id)
        .where(User.deleted_at.is_(None))
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Prevent updating self
    if str(user.id) == str(org_context.user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update your own role through this endpoint",
        )

    # Verify role exists if provided
    if member_data.role_id:
        result = await db.execute(
            select(Role).where(Role.id == member_data.role_id)
        )
        role = result.scalar_one_or_none()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role not found",
            )

    # Update fields
    update_data = member_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)

    # Load role for response
    await db.refresh(user, ["role"])

    logger.info(
        "Organization member updated",
        user_id=user_id,
        organization_id=org_context.organization.id,
    )

    return OrganizationMemberResponse(
        user_id=str(user.id),
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        avatar_url=user.avatar_url,
        job_title=user.job_title,
        department=user.department,
        role_id=str(user.role_id) if user.role_id else "",
        role_name=user.role.name if user.role else "",
        role_slug=user.role.slug if user.role else "",
        is_active=user.is_active,
        is_verified=user.is_verified,
        joined_at=user.created_at,
    )


@router.delete("/{user_id}")
async def remove_member(
    user_id: str,
    org_context: AuthenticatedUser = Depends(require_permission("manage_users")),
    db: AsyncSession = Depends(get_db),
):
    """
    Remove a member from the organization (soft delete).
    """
    result = await db.execute(
        select(User)
        .where(User.id == user_id)
        .where(User.organization_id == org_context.organization.id)
        .where(User.deleted_at.is_(None))
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Prevent removing self
    if str(user.id) == str(org_context.user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove yourself from the organization",
        )

    # Soft delete
    from datetime import datetime
    user.deleted_at = datetime.utcnow()
    await db.commit()

    logger.info(
        "Organization member removed",
        user_id=user_id,
        organization_id=org_context.organization.id,
    )

    return {"message": "Member removed successfully"}
