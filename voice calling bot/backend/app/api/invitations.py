from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.authentication.dependencies import (
    AuthenticatedUser,
    get_organization_context,
    require_permission,
)
from app.authentication.security import generate_secure_token
from app.core.logging import get_logger
from app.database.connection import get_db
from app.models.invitation import OrganizationInvitation
from app.models.user import Role
from app.schemas.organization_member import (
    OrganizationInviteCreate,
    OrganizationInviteResponse,
)

logger = get_logger(__name__)
router = APIRouter(prefix="/organizations/invitations", tags=["Organization Invitations"])


@router.get("", response_model=list[OrganizationInviteResponse])
async def list_invitations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status_filter: str = Query(None, alias="status"),
    org_context: AuthenticatedUser = Depends(get_organization_context),
    db: AsyncSession = Depends(get_db),
):
    """
    List all invitations for the current organization.
    """
    # Build base query with organization scoping
    query = select(OrganizationInvitation).where(
        OrganizationInvitation.organization_id == org_context.organization.id
    )

    # Apply status filter
    if status_filter:
        query = query.where(OrganizationInvitation.status == status_filter)

    # Apply soft delete filter
    query = query.where(OrganizationInvitation.deleted_at.is_(None))

    # Apply pagination
    query = query.order_by(OrganizationInvitation.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    invitations = result.scalars().all()

    logger.info(
        "Organization invitations listed",
        organization_id=org_context.organization.id,
        page=page,
        page_size=page_size,
    )

    # Get role names
    responses = []
    for invite in invitations:
        result = await db.execute(
            select(Role).where(Role.id == invite.role_id)
        )
        role = result.scalar_one_or_none()
        
        responses.append(
            OrganizationInviteResponse(
                id=str(invite.id),
                email=invite.email,
                role_id=str(invite.role_id),
                role_name=role.name if role else "",
                status=invite.status,
                expires_at=invite.expires_at,
                created_at=invite.created_at,
            )
        )

    return responses


@router.post("", response_model=OrganizationInviteResponse, status_code=status.HTTP_201_CREATED)
async def create_invitation(
    invite_data: OrganizationInviteCreate,
    org_context: AuthenticatedUser = Depends(require_permission("manage_users")),
    db: AsyncSession = Depends(get_db),
):
    """
    Create an invitation for a user to join the organization.
    
    In production, this would send an email with the invitation link.
    """
    # Check if there's already a pending invitation for this email
    result = await db.execute(
        select(OrganizationInvitation)
        .where(OrganizationInvitation.email == invite_data.email)
        .where(OrganizationInvitation.organization_id == org_context.organization.id)
        .where(OrganizationInvitation.status == "pending")
        .where(OrganizationInvitation.deleted_at.is_(None))
    )
    existing_invite = result.scalar_one_or_none()

    if existing_invite:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pending invitation already exists for this email",
        )

    # Verify role exists
    result = await db.execute(
        select(Role).where(Role.id == invite_data.role_id)
    )
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role not found",
        )

    # Generate invitation token
    token = generate_secure_token(48)
    expires_at = datetime.utcnow() + timedelta(days=7)  # 7 days expiry

    # Create invitation
    invitation = OrganizationInvitation(
        organization_id=org_context.organization.id,
        email=invite_data.email,
        role_id=invite_data.role_id,
        token=token,
        status="pending",
        message=invite_data.message,
        invited_by=str(org_context.user.id),
        expires_at=expires_at,
    )

    db.add(invitation)
    await db.commit()
    await db.refresh(invitation)

    logger.info(
        "Organization invitation created",
        invitation_id=invitation.id,
        email=invite_data.email,
        organization_id=org_context.organization.id,
    )

    # In production, send email with invitation link
    # For now, return the token for testing
    return OrganizationInviteResponse(
        id=str(invitation.id),
        email=invitation.email,
        role_id=str(invitation.role_id),
        role_name=role.name,
        status=invitation.status,
        expires_at=invitation.expires_at,
        created_at=invitation.created_at,
    )


@router.post("/{invitation_id}/accept")
async def accept_invitation(
    invitation_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Accept an organization invitation.
    
    This endpoint would typically be called after a user clicks the invitation link.
    """
    result = await db.execute(
        select(OrganizationInvitation)
        .where(OrganizationInvitation.id == invitation_id)
        .where(OrganizationInvitation.deleted_at.is_(None))
    )
    invitation = result.scalar_one_or_none()

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found",
        )

    if invitation.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invitation is {invitation.status}",
        )

    if datetime.utcnow() > invitation.expires_at:
        invitation.status = "expired"
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invitation has expired",
        )

    # Mark as accepted
    invitation.status = "accepted"
    invitation.accepted_at = datetime.utcnow()
    await db.commit()

    logger.info(
        "Organization invitation accepted",
        invitation_id=invitation_id,
        email=invitation.email,
    )

    return {"message": "Invitation accepted successfully"}


@router.post("/{invitation_id}/decline")
async def decline_invitation(
    invitation_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Decline an organization invitation.
    """
    result = await db.execute(
        select(OrganizationInvitation)
        .where(OrganizationInvitation.id == invitation_id)
        .where(OrganizationInvitation.deleted_at.is_(None))
    )
    invitation = result.scalar_one_or_none()

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found",
        )

    if invitation.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invitation is {invitation.status}",
        )

    # Mark as declined
    invitation.status = "declined"
    invitation.declined_at = datetime.utcnow()
    await db.commit()

    logger.info(
        "Organization invitation declined",
        invitation_id=invitation_id,
        email=invitation.email,
    )

    return {"message": "Invitation declined successfully"}


@router.delete("/{invitation_id}")
async def cancel_invitation(
    invitation_id: str,
    org_context: AuthenticatedUser = Depends(require_permission("manage_users")),
    db: AsyncSession = Depends(get_db),
):
    """
    Cancel a pending invitation.
    """
    result = await db.execute(
        select(OrganizationInvitation)
        .where(OrganizationInvitation.id == invitation_id)
        .where(OrganizationInvitation.organization_id == org_context.organization.id)
        .where(OrganizationInvitation.deleted_at.is_(None))
    )
    invitation = result.scalar_one_or_none()

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found",
        )

    if invitation.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel a non-pending invitation",
        )

    # Soft delete
    invitation.deleted_at = datetime.utcnow()
    await db.commit()

    logger.info(
        "Organization invitation cancelled",
        invitation_id=invitation_id,
        organization_id=org_context.organization.id,
    )

    return {"message": "Invitation cancelled successfully"}
