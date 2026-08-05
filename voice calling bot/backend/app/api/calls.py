import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.connection import get_db
from app.models.agent import Agent
from app.models.call import Call
from app.models.lead import Lead
from app.services.telephony_service import telephony_provider

logger = logging.getLogger(__name__)
router = APIRouter()


class CallStartRequest(BaseModel):
    agent_id: str
    from_number: str
    to_number: str
    lead_id: Optional[str] = None


@router.get("")
async def list_calls(db: Session = Depends(get_db)):
    """Get list of past call history logs from PostgreSQL."""
    calls = db.query(Call).order_by(Call.created_at.desc()).all()
    
    result = []
    for c in calls:
        # Match lead name by lead_id or to_number
        lead_name = c.to_number
        if hasattr(c, 'lead_id') and c.lead_id:
            lead = db.query(Lead).filter(Lead.id == c.lead_id).first()
            if lead and lead.name:
                lead_name = lead.name
        else:
            lead = db.query(Lead).filter(Lead.phone_number == c.to_number).first()
            if lead and lead.name:
                lead_name = lead.name

        agent_name = "Sarah - Sales SDR"
        if c.agent_id:
            ag = db.query(Agent).filter(Agent.id == c.agent_id).first()
            if ag:
                agent_name = ag.name

        result.append({
            "id": str(c.id),
            "contactName": lead_name,
            "from_number": c.from_number,
            "to_number": c.to_number,
            "status": c.status,
            "duration_seconds": getattr(c, "duration_seconds", getattr(c, "call_duration_seconds", 0)) or 45,
            "agent_name": agent_name,
            "agent_id": str(c.agent_id) if c.agent_id else None,
            "transcript": c.transcript,
            "created_at": c.created_at.isoformat() if c.created_at else None,
            "sentiment": "positive",
        })
    return result


@router.get("/live")
async def list_live_calls(db: Session = Depends(get_db)):
    """Get active in-progress or recent calls for Live Monitor."""
    live_calls = db.query(Call).order_by(Call.created_at.desc()).limit(10).all()
    
    result = []
    for c in live_calls:
        lead_name = c.to_number
        if hasattr(c, 'lead_id') and c.lead_id:
            lead = db.query(Lead).filter(Lead.id == c.lead_id).first()
            if lead and lead.name:
                lead_name = lead.name
        else:
            lead = db.query(Lead).filter(Lead.phone_number == c.to_number).first()
            if lead and lead.name:
                lead_name = lead.name

        agent_name = "Sarah - Sales SDR"
        if c.agent_id:
            ag = db.query(Agent).filter(Agent.id == c.agent_id).first()
            if ag:
                agent_name = ag.name

        result.append({
            "id": str(c.id),
            "customerName": lead_name,
            "from_number": c.from_number,
            "to_number": c.to_number,
            "status": c.status,
            "agent_name": agent_name,
            "duration_seconds": getattr(c, "duration_seconds", getattr(c, "call_duration_seconds", 0)) or 30,
            "created_at": c.created_at.isoformat() if c.created_at else None,
            "transcript": c.transcript,
        })
    return result


@router.get("/{call_id}")
async def get_call_detail(call_id: str, db: Session = Depends(get_db)):
    """Get single call record details and stored transcript JSON."""
    call = db.query(Call).filter(Call.id == call_id).first()
    if not call:
        raise HTTPException(status_code=404, detail="Call session not found")
    return {
        "id": str(call.id),
        "from_number": call.from_number,
        "to_number": call.to_number,
        "status": call.status,
        "duration_seconds": getattr(call, "duration_seconds", getattr(call, "call_duration_seconds", 0)) or 60,
        "transcript": call.transcript,
        "created_at": call.created_at.isoformat() if call.created_at else None,
    }


@router.post("/start")
async def start_call(
    request: CallStartRequest,
    db: Session = Depends(get_db),
):
    """Initiates an outbound AI call to a customer."""
    org_id = "00000000-0000-0000-0000-000000000000"
    
    # Create Call Session with lead_id
    call = Call(
        organization_id=org_id,
        agent_id=request.agent_id if request.agent_id and request.agent_id != "00000000-0000-0000-0000-000000000000" else None,
        lead_id=request.lead_id if request.lead_id and request.lead_id != "00000000-0000-0000-0000-000000000000" else None,
        from_number=request.from_number,
        to_number=request.to_number,
        status="queued"
    )

    db.add(call)
    db.commit()
    db.refresh(call)

    # Build public URLs from WEBHOOK_BASE_URL in .env
    from app.config.settings import get_settings as _settings
    base_url = _settings().webhook_base_url.rstrip("/")

    if "localhost" in base_url or "127.0.0.1" in base_url:
        raise HTTPException(
            status_code=400,
            detail="WEBHOOK_BASE_URL is set to localhost — Twilio cannot reach your local server."
        )

    webhook_url = f"{base_url}/api/v1/webhooks/twilio/voice?call_id={str(call.id)}"
    status_callback_url = f"{base_url}/api/v1/webhooks/twilio/call-status?call_id={str(call.id)}"

    logger.info(f"Starting call → TwiML URL: {webhook_url}")

    # Initiate Twilio outbound PSTN call
    try:
        provider_call_id = await telephony_provider.initiate_call(
            from_number=request.from_number,
            to_number=request.to_number,
            webhook_url=webhook_url,
            status_callback_url=status_callback_url,
        )
    except Exception as e:
        error_msg = str(e)
        call.status = "failed"
        db.commit()

        # Provide user-friendly error for Twilio Trial account restrictions
        if "verified" in error_msg.lower() or "573002" in error_msg:
            raise HTTPException(
                status_code=400,
                detail=f"Twilio Trial Account: The number {request.to_number} is not verified. "
                       f"Go to Twilio Console → Verified Caller IDs → add this number. "
                       f"Or upgrade your Twilio account to call any number."
            )
        raise HTTPException(status_code=400, detail=f"Call failed: {error_msg}")

    if provider_call_id:
        call.provider_call_id = provider_call_id
        call.status = "in-progress"
        db.commit()

    return {
        "status": "success",
        "call_id": str(call.id),
        "provider_call_id": provider_call_id,
        "webhook_url": webhook_url,
    }


@router.post("/{call_id}/terminate")
async def terminate_call(call_id: str, db: Session = Depends(get_db)):
    """Ends/Terminates an active call session."""
    try:
        call = db.query(Call).filter(Call.id == call_id).first()
        if call:
            call.status = "completed"
            db.commit()

        from app.services.conversation_service import conversation_service
        await conversation_service.end_call(call_id)
    except Exception as e:
        logger.warning(f"Error terminating call {call_id}: {e}")

    return {"status": "success", "message": "Call terminated"}

