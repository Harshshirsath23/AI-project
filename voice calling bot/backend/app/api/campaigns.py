from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from pydantic import BaseModel
import asyncio
import json

from app.database.connection import get_db
from app.authentication.dependencies import get_current_user
from app.models.campaign import Campaign
from app.services.campaign_scheduler import campaign_scheduler

router = APIRouter()

from typing import Optional


from typing import Optional, List

class CampaignCreateSchema(BaseModel):
    name: str
    description: Optional[str] = ""
    agent_id: Optional[str] = None
    from_number: Optional[str] = None
    lead_ids: Optional[List[str]] = None
    calling_window_start: str = "09:00"
    calling_window_end: str = "17:00"
    max_concurrent_calls: int = 5


class CampaignUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    agent_id: Optional[str] = None
    from_number: Optional[str] = None
    max_concurrent_calls: Optional[int] = None
    status: Optional[str] = None


@router.get("")
async def list_campaigns(db: Session = Depends(get_db)):
    """Get list of campaigns."""
    campaigns = db.query(Campaign).filter(Campaign.deleted_at.is_(None)).order_by(Campaign.created_at.desc()).all()

    return [
        {
            "id": str(c.id),
            "name": c.name,
            "description": c.description,
            "status": c.status,
            "total_leads": c.total_leads,
            "completed_calls": c.completed_calls,
            "successful_calls": c.successful_calls,
            "failed_calls": c.failed_calls,
            "success_rate": c.success_rate,
            "agent_id": str(c.agent_id) if c.agent_id else None,
            "from_number": c.phone_numbers.get("from_number") if c.phone_numbers and isinstance(c.phone_numbers, dict) else None,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        }
        for c in campaigns
    ]


@router.post("")
async def create_campaign(data: CampaignCreateSchema, db: Session = Depends(get_db)):
    """Create a new campaign and attach leads."""
    from app.models.lead import Lead

    org_id = "00000000-0000-0000-0000-000000000000"
    phone_data = {"from_number": data.from_number} if data.from_number else None

    campaign = Campaign(
        organization_id=org_id,
        name=data.name,
        description=data.description,
        agent_id=data.agent_id if data.agent_id and data.agent_id != "00000000-0000-0000-0000-000000000000" else None,
        phone_numbers=phone_data,
        campaign_type="outbound",
        calling_window_start=data.calling_window_start,
        calling_window_end=data.calling_window_end,
        max_concurrent_calls=data.max_concurrent_calls,
        status="running",
        total_leads=0,
        completed_calls=0,
        successful_calls=0,
        failed_calls=0,
        success_rate=0.0,
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)

    # Attach leads to this campaign
    if data.lead_ids:
        leads = db.query(Lead).filter(Lead.id.in_(data.lead_ids)).all()
        for l in leads:
            l.campaign_id = campaign.id
        campaign.total_leads = len(leads)
    else:
        # Assign all unassigned leads to this campaign
        unassigned_leads = db.query(Lead).filter(Lead.campaign_id.is_(None)).all()
        for l in unassigned_leads:
            l.campaign_id = campaign.id
        campaign.total_leads = len(unassigned_leads)

    db.commit()
    db.refresh(campaign)

    # Automatically start background dialing for the campaign
    campaign_scheduler.start_campaign(db, str(campaign.id))

    return {"status": "success", "id": str(campaign.id), "name": campaign.name}


@router.get("/{campaign_id}")
async def get_campaign_detail(campaign_id: str, db: Session = Depends(get_db)):
    """Get single campaign details."""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
        
    return {
        "id": str(campaign.id),
        "name": campaign.name,
        "description": campaign.description,
        "status": campaign.status,
        "agent_id": str(campaign.agent_id) if campaign.agent_id else None,
        "from_number": campaign.phone_numbers.get("from_number") if campaign.phone_numbers and isinstance(campaign.phone_numbers, dict) else None,
        "max_concurrent_calls": campaign.max_concurrent_calls,
        "total_leads": campaign.total_leads,
        "completed_calls": campaign.completed_calls,
        "successful_calls": campaign.successful_calls,
        "failed_calls": campaign.failed_calls,
        "success_rate": campaign.success_rate,
        "created_at": campaign.created_at.isoformat() if campaign.created_at else None,
    }


@router.put("/{campaign_id}")
async def update_campaign(campaign_id: str, data: CampaignUpdateSchema, db: Session = Depends(get_db)):
    """Update campaign properties."""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    if data.name is not None:
        campaign.name = data.name
    if data.description is not None:
        campaign.description = data.description
    if data.agent_id is not None:
        campaign.agent_id = data.agent_id if data.agent_id and data.agent_id != "00000000-0000-0000-0000-000000000000" else None
    if data.from_number is not None:
        campaign.phone_numbers = {"from_number": data.from_number}
    if data.max_concurrent_calls is not None:
        campaign.max_concurrent_calls = data.max_concurrent_calls
    if data.status is not None:
        campaign.status = data.status

    db.commit()
    db.refresh(campaign)

    return {
        "status": "success",
        "message": "Campaign updated successfully",
        "id": str(campaign.id),
        "name": campaign.name
    }


@router.delete("/{campaign_id}")
async def delete_campaign(campaign_id: str, db: Session = Depends(get_db)):
    """Soft delete a campaign."""
    from datetime import datetime, UTC
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
        
    campaign.deleted_at = datetime.now(UTC)
    campaign.status = "cancelled"
    db.commit()
    return {"status": "success", "message": "Campaign deleted successfully"}


@router.post("/{campaign_id}/start")
async def start_campaign(campaign_id: str, db: Session = Depends(get_db)):
    campaign_scheduler.start_campaign(db, campaign_id)
    return {"status": "success", "message": "Campaign started"}

@router.post("/{campaign_id}/pause")
async def pause_campaign(campaign_id: str, db: Session = Depends(get_db)):
    campaign_scheduler.pause_campaign(db, campaign_id)
    return {"status": "success", "message": "Campaign paused"}

@router.post("/{campaign_id}/stop")
async def stop_campaign(campaign_id: str, db: Session = Depends(get_db)):
    campaign_scheduler.stop_campaign(db, campaign_id)
    return {"status": "success", "message": "Campaign stopped"}

@router.get("/{campaign_id}/progress")
async def get_campaign_progress(campaign_id: str, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
        
    return {
        "status": campaign.status,
        "total_leads": campaign.total_leads,
        "completed": campaign.completed_calls,
        "failed": campaign.failed_calls,
        "success_rate": campaign.success_rate
    }

# WebSockets for live progress tracking
@router.websocket("/ws/{campaign_id}")
async def campaign_progress_ws(websocket: WebSocket, campaign_id: str):
    await websocket.accept()
    
    # Normally we would use Redis PubSub to broadcast to all clients efficiently.
    # For MVP, we will poll the DB and push to the connected client.
    try:
        from app.database.connection import SessionLocal
        while True:
            db = SessionLocal()
            campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
            if campaign:
                payload = {
                    "status": campaign.status,
                    "completed": campaign.completed_calls,
                    "failed": campaign.failed_calls,
                    "success_rate": campaign.success_rate,
                    "active_calls": 0 # This would be queried from Calls table
                }
                await websocket.send_text(json.dumps(payload))
            db.close()
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        print(f"Client disconnected from campaign {campaign_id} WS")
