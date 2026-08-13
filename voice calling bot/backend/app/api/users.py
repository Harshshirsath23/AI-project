from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.authentication.dependencies import (
    AuthenticatedUser,
    get_organization_context,
    require_permission,
    require_role,
)
from app.authentication.security import hash_password, validate_password_strength
from app.core.logging import get_logger
from app.database.connection import get_async_db
from app.models.user import Role, User
from app.schemas.user import (
    UserCreate,
    UserDeactivateRequest,
    UserDetailResponse,
    UserListResponse,
    UserUpdate,
)

logger = get_logger(__name__)
router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[UserListResponse])
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    role_id: Optional[str] = Query(None),
    org_context: AuthenticatedUser = Depends(get_organization_context),
    db: AsyncSession = Depends(get_async_db),
):
    """
    List users in the organization with pagination, filtering, and search.
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
            or_(
                User.email.ilike(search_pattern),
                User.first_name.ilike(search_pattern),
                User.last_name.ilike(search_pattern),
            )
        )

    if is_active is not None:
        query = query.where(User.is_active == is_active)

    if role_id:
        query = query.where(User.role_id == role_id)

    # Apply soft delete filter
    query = query.where(User.deleted_at.is_(None))

    # Get total count
    count_query = select(User.id).where(
        User.organization_id == org_context.organization.id
    )
    if search:
        search_pattern = f"%{search}%"
        count_query = count_query.where(
            or_(
                User.email.ilike(search_pattern),
                User.first_name.ilike(search_pattern),
                User.last_name.ilike(search_pattern),
            )
        )
    if is_active is not None:
        count_query = count_query.where(User.is_active == is_active)
    if role_id:
        count_query = count_query.where(User.role_id == role_id)
    count_query = count_query.where(User.deleted_at.is_(None))

    total_result = await db.execute(count_query)
    total = len(total_result.scalars().all())

    # Apply pagination
    query = query.order_by(User.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    users = result.scalars().all()

    logger.info(
        "Users listed",
        organization_id=org_context.organization.id,
        page=page,
        page_size=page_size,
        total=total,
    )

    return [
        UserListResponse(
            id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            avatar_url=user.avatar_url,
            job_title=user.job_title,
            department=user.department,
            is_active=user.is_active,
            is_verified=user.is_verified,
            role_id=str(user.role_id) if user.role_id else None,
            role_name=user.role.name if user.role else None,
            created_at=user.created_at,
        )
        for user in users
    ]


@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user(
    user_id: str,
    org_context: AuthenticatedUser = Depends(get_organization_context),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Get details of a specific user.
    """
    result = await db.execute(
        select(User)
        .where(User.id == user_id)
        .where(User.organization_id == org_context.organization.id)
        .where(User.deleted_at.is_(None))
        .options(selectinload(User.role))
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserDetailResponse(
        id=str(user.id),
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        avatar_url=user.avatar_url,
        job_title=user.job_title,
        department=user.department,
        timezone=user.timezone,
        locale=user.locale,
        is_active=user.is_active,
        is_verified=user.is_verified,
        last_login_at=user.last_login_at,
        role_id=str(user.role_id) if user.role_id else None,
        role_name=user.role.name if user.role else None,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.post("", response_model=UserDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    org_context: AuthenticatedUser = Depends(
        require_permission("manage_users")
    ),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Create a new user in the organization.
    """
    # Validate password strength
    is_valid, error_msg = validate_password_strength(user_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg,
        )

    # Check if email already exists in organization
    result = await db.execute(
        select(User)
        .where(User.email == user_data.email)
        .where(User.organization_id == org_context.organization.id)
        .where(User.deleted_at.is_(None))
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists in organization",
        )

    # Verify role exists and belongs to organization
    if user_data.role_id:
        # For now, roles are global, but we should verify it exists
        result = await db.execute(
            select(Role).where(Role.id == user_data.role_id)
        )
        role = result.scalar_one_or_none()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role not found",
            )

    # Create user
    hashed_password = hash_password(user_data.password)
    user = User(
        organization_id=org_context.organization.id,
        role_id=user_data.role_id,
        email=user_data.email,
        password_hash=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone,
        job_title=user_data.job_title,
        department=user_data.department,
        timezone=user_data.timezone,
        locale=user_data.locale,
        is_active=True,
        is_verified=False,
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Load role for response
    await db.refresh(user, ["role"])

    logger.info(
        "User created",
        user_id=user.id,
        email=user_data.email,
        organization_id=org_context.organization.id,
    )

    return UserDetailResponse(
        id=str(user.id),
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        avatar_url=user.avatar_url,
        job_title=user.job_title,
        department=user.department,
        timezone=user.timezone,
        locale=user.locale,
        is_active=user.is_active,
        is_verified=user.is_verified,
        last_login_at=user.last_login_at,
        role_id=str(user.role_id) if user.role_id else None,
        role_name=user.role.name if user.role else None,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.put("/{user_id}", response_model=UserDetailResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    org_context: AuthenticatedUser = Depends(
        require_permission("manage_users")
    ),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Update a user's information.
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

    # Update fields
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)

    # Load role for response
    await db.refresh(user, ["role"])

    logger.info(
        "User updated",
        user_id=user_id,
        organization_id=org_context.organization.id,
    )

    return UserDetailResponse(
        id=str(user.id),
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        avatar_url=user.avatar_url,
        job_title=user.job_title,
        department=user.department,
        timezone=user.timezone,
        locale=user.locale,
        is_active=user.is_active,
        is_verified=user.is_verified,
        last_login_at=user.last_login_at,
        role_id=str(user.role_id) if user.role_id else None,
        role_name=user.role.name if user.role else None,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.post("/{user_id}/deactivate")
async def deactivate_user(
    user_id: str,
    request: UserDeactivateRequest,
    org_context: AuthenticatedUser = Depends(
        require_permission("manage_users")
    ),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Deactivate a user account.
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

    # Prevent deactivating self
    if str(user.id) == str(org_context.user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account",
        )

    user.is_active = False
    await db.commit()

    logger.info(
        "User deactivated",
        user_id=user_id,
        organization_id=org_context.organization.id,
        reason=request.reason,
    )

    return {"message": "User deactivated successfully"}


@router.post("/{user_id}/activate")
async def activate_user(
    user_id: str,
    org_context: AuthenticatedUser = Depends(
        require_permission("manage_users")
    ),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Activate a deactivated user account.
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

    user.is_active = True
    await db.commit()

    logger.info(
        "User activated",
        user_id=user_id,
        organization_id=org_context.organization.id,
    )

    return {"message": "User activated successfully"}
