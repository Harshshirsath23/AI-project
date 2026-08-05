from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timezone

from app.models.lead import Lead

class QueueService:
    """Manages pulling pending and retry leads from the database for active campaigns."""

    def get_next_leads(self, db: Session, campaign_id: str, limit: int = 10) -> list[Lead]:
        """
        Pulls leads that are 'pending' or 'queued' (for retries that reached their next_call_at).
        Prioritizes by priority field (higher is better).
        """
        now = datetime.now(timezone.utc).isoformat()
        
        leads = db.query(Lead).filter(
            Lead.campaign_id == campaign_id,
            Lead.is_deleted == False,
            or_(
                Lead.status == "pending",
                (Lead.status == "queued") & (Lead.next_call_at <= now)
            )
        ).order_by(Lead.priority.desc()).limit(limit).all()
        
        # Mark as queued to prevent other workers from grabbing them
        for lead in leads:
            lead.status = "calling"
            lead.last_call_at = now
            lead.call_attempts += 1
            
        db.commit()
        return leads

queue_service = QueueService()
