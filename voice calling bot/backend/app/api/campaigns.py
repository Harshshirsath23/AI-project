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


class CampaignCreateSchema(BaseModel):
    name: str
    description: Optional[str] = ""
    agent_id: Optional[str] = None
    calling_window_start: str = "09:00"
    calling_window_end: str = "17:00"
    max_concurrent_calls: int = 5


@router.get("")
async def list_campaigns(db: Session = Depends(get_db)):
    """Get list of campaigns."""
    campaigns = db.query(Campaign).filter(Campaign.deleted_at.is_(None)).order_by(Campaign.created_at.desc()).all()

    if not campaigns:
        default_camp = Campaign(
            organization_id="00000000-0000-0000-0000-000000000000",
            name="Q3 Outbound Sales Outreach",
            description="Automated SDR calling campaign targeting inbound trial leads.",
            campaign_type="outbound",
            status="running",
            total_leads=150,
            completed_calls=38,
            successful_calls=34,
            failed_calls=4,
            success_rate=89.4,
            max_concurrent_calls=5,
        )
        db.add(default_camp)
        db.commit()
        db.refresh(default_camp)
        campaigns = [default_camp]

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
            "created_at": c.created_at.isoformat() if c.created_at else None,
        }
        for c in campaigns
    ]


@router.post("")
async def create_campaign(data: CampaignCreateSchema, db: Session = Depends(get_db)):
    """Create a new campaign."""
    campaign = Campaign(
        organization_id="00000000-0000-0000-0000-000000000000",
        name=data.name,
        description=data.description,
        agent_id=data.agent_id if data.agent_id and data.agent_id != "00000000-0000-0000-0000-000000000000" else None,
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
    return {"status": "success", "id": str(campaign.id), "name": campaign.name}


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
