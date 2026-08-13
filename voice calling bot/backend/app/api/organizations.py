from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.authentication.dependencies import (
    AuthenticatedUser,
    get_organization_context,
    require_permission,
    require_role,
)
from app.core.logging import get_logger
from app.database.connection import get_async_db
from app.models.organization import Organization, OrganizationSettings
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationDetailResponse,
    OrganizationResponse,
    OrganizationSettingsUpdate,
    OrganizationUpdate,
)

logger = get_logger(__name__)
router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get("", response_model=list[OrganizationResponse])
async def list_organizations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    auth: AuthenticatedUser = Depends(require_role("super_admin")),
    db: AsyncSession = Depends(get_async_db),
):
    """
    List all organizations (super admin only).
    """
    # Build base query
    query = select(Organization)

    # Apply filters
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            Organization.name.ilike(search_pattern)
            | Organization.slug.ilike(search_pattern)
        )

    if is_active is not None:
        query = query.where(Organization.is_active == is_active)

    # Apply soft delete filter
    query = query.where(Organization.deleted_at.is_(None))

    # Get total count
    count_query = select(Organization.id)
    if search:
        search_pattern = f"%{search}%"
        count_query = count_query.where(
            Organization.name.ilike(search_pattern)
            | Organization.slug.ilike(search_pattern)
        )
    if is_active is not None:
        count_query = count_query.where(Organization.is_active == is_active)
    count_query = count_query.where(Organization.deleted_at.is_(None))

    total_result = await db.execute(count_query)
    total = len(total_result.scalars().all())

    # Apply pagination
    query = query.order_by(Organization.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    organizations = result.scalars().all()

    logger.info(
        "Organizations listed",
        page=page,
        page_size=page_size,
        total=total,
    )

    return [
        OrganizationResponse.model_validate(org) for org in organizations
    ]


@router.get("/current", response_model=OrganizationDetailResponse)
async def get_current_organization(
    org_context: AuthenticatedUser = Depends(get_organization_context),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Get the current user's organization details with settings.
    """
    result = await db.execute(
        select(Organization)
        .where(Organization.id == org_context.organization.id)
        .options(selectinload(Organization.settings))
    )
    organization = result.scalar_one_or_none()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    settings_dict = None
    if organization.settings:
        settings_dict = {
            "timezone": organization.settings.timezone,
            "locale": organization.settings.locale,
            "currency": organization.settings.currency,
            "default_language": organization.settings.default_language,
            "max_concurrent_calls": organization.settings.max_concurrent_calls,
            "call_recording_enabled": organization.settings.call_recording_enabled,
            "auto_transcription_enabled": organization.settings.auto_transcription_enabled,
            "retention_days": organization.settings.retention_days,
            "custom_branding_enabled": organization.settings.custom_branding_enabled,
            "api_rate_limit": organization.settings.api_rate_limit,
        }

    return OrganizationDetailResponse(
        id=str(organization.id),
        name=organization.name,
        slug=organization.slug,
        description=organization.description,
        website=organization.website,
        logo_url=organization.logo_url,
        industry=organization.industry,
        company_size=organization.company_size,
        contact_email=organization.contact_email,
        contact_phone=organization.contact_phone,
        is_active=organization.is_active,
        created_at=organization.created_at,
        updated_at=organization.updated_at,
        settings=settings_dict,
    )


@router.get("/{organization_id}", response_model=OrganizationDetailResponse)
async def get_organization(
    organization_id: str,
    auth: AuthenticatedUser = Depends(require_role("super_admin")),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Get organization details by ID (super admin only).
    """
    result = await db.execute(
        select(Organization)
        .where(Organization.id == organization_id)
        .where(Organization.deleted_at.is_(None))
        .options(selectinload(Organization.settings))
    )
    organization = result.scalar_one_or_none()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    settings_dict = None
    if organization.settings:
        settings_dict = {
            "timezone": organization.settings.timezone,
            "locale": organization.settings.locale,
            "currency": organization.settings.currency,
            "default_language": organization.settings.default_language,
            "max_concurrent_calls": organization.settings.max_concurrent_calls,
            "call_recording_enabled": organization.settings.call_recording_enabled,
            "auto_transcription_enabled": organization.settings.auto_transcription_enabled,
            "retention_days": organization.settings.retention_days,
            "custom_branding_enabled": organization.settings.custom_branding_enabled,
            "api_rate_limit": organization.settings.api_rate_limit,
        }

    return OrganizationDetailResponse(
        id=str(organization.id),
        name=organization.name,
        slug=organization.slug,
        description=organization.description,
        website=organization.website,
        logo_url=organization.logo_url,
        industry=organization.industry,
        company_size=organization.company_size,
        contact_email=organization.contact_email,
        contact_phone=organization.contact_phone,
        is_active=organization.is_active,
        created_at=organization.created_at,
        updated_at=organization.updated_at,
        settings=settings_dict,
    )


@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    org_data: OrganizationCreate,
    auth: AuthenticatedUser = Depends(require_role("super_admin")),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Create a new organization (super admin only).
    """
    # Check if slug already exists
    result = await db.execute(
        select(Organization).where(Organization.slug == org_data.slug)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization slug already exists",
        )

    # Create organization
    organization = Organization(
        name=org_data.name,
        slug=org_data.slug,
        description=org_data.description,
        website=org_data.website,
        industry=org_data.industry,
        company_size=org_data.company_size,
        contact_email=org_data.contact_email,
        contact_phone=org_data.contact_phone,
        is_active=True,
    )

    db.add(organization)
    await db.commit()
    await db.refresh(organization)

    logger.info(
        "Organization created",
        organization_id=organization.id,
        slug=org_data.slug,
    )

    return OrganizationResponse.model_validate(organization)


@router.put("/{organization_id}", response_model=OrganizationResponse)
async def update_organization(
    organization_id: str,
    org_data: OrganizationUpdate,
    auth: AuthenticatedUser = Depends(require_permission("manage_organization")),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Update organization details.
    """
    result = await db.execute(
        select(Organization)
        .where(Organization.id == organization_id)
        .where(Organization.deleted_at.is_(None))
    )
    organization = result.scalar_one_or_none()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    # Verify user belongs to organization or is super admin
    if str(organization.id) != str(auth.organization.id):
        # Check if user is super admin
        if not auth.role or auth.role.slug != "super_admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this organization",
            )

    # Update fields
    update_data = org_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(organization, field, value)

    await db.commit()
    await db.refresh(organization)

    logger.info(
        "Organization updated",
        organization_id=organization_id,
    )

    return OrganizationResponse.model_validate(organization)


@router.put("/{organization_id}/settings")
async def update_organization_settings(
    organization_id: str,
    settings_data: OrganizationSettingsUpdate,
    auth: AuthenticatedUser = Depends(require_permission("manage_organization")),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Update organization settings.
    """
    result = await db.execute(
        select(Organization)
        .where(Organization.id == organization_id)
        .where(Organization.deleted_at.is_(None))
        .options(selectinload(Organization.settings))
    )
    organization = result.scalar_one_or_none()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    # Verify user belongs to organization or is super admin
    if str(organization.id) != str(auth.organization.id):
        if not auth.role or auth.role.slug != "super_admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this organization",
            )

    # Get or create settings
    if not organization.settings:
        organization.settings = OrganizationSettings(
            organization_id=organization.id,
        )

    # Update settings
    update_data = settings_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(organization.settings, field, value)

    await db.commit()

    logger.info(
        "Organization settings updated",
        organization_id=organization_id,
    )

    return {"message": "Organization settings updated successfully"}


@router.post("/{organization_id}/deactivate")
async def deactivate_organization(
    organization_id: str,
    auth: AuthenticatedUser = Depends(require_role("super_admin")),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Deactivate an organization (super admin only).
    """
    result = await db.execute(
        select(Organization)
        .where(Organization.id == organization_id)
        .where(Organization.deleted_at.is_(None))
    )
    organization = result.scalar_one_or_none()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    organization.is_active = False
    await db.commit()

    logger.info(
        "Organization deactivated",
        organization_id=organization_id,
    )

    return {"message": "Organization deactivated successfully"}


@router.post("/{organization_id}/activate")
async def activate_organization(
    organization_id: str,
    auth: AuthenticatedUser = Depends(require_role("super_admin")),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Activate a deactivated organization (super admin only).
    """
    result = await db.execute(
        select(Organization)
        .where(Organization.id == organization_id)
        .where(Organization.deleted_at.is_(None))
    )
    organization = result.scalar_one_or_none()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    organization.is_active = True
    await db.commit()

    logger.info(
        "Organization activated",
        organization_id=organization_id,
    )

    return {"message": "Organization activated successfully"}
