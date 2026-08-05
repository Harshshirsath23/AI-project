from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models.lead import Lead
from app.models.campaign import Campaign

class RetryEngine:
    """Handles logic for requeuing leads that failed or weren't answered."""

    def process_call_outcome(self, db: Session, lead_id: str, outcome: str):
        """
        Takes the final status of a Call (completed, failed, busy, no-answer)
        and updates the Lead accordingly.
        """
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            return
            
        campaign = db.query(Campaign).filter(Campaign.id == lead.campaign_id).first()
        if not campaign:
            return

        lead.final_disposition = outcome
        
        # Outcomes that require a retry
        if outcome in ["failed", "busy", "no-answer"]:
            if lead.retry_count < campaign.retry_count:
                lead.retry_count += 1
                lead.status = "queued"
                
                # Calculate next call time
                now = datetime.now(timezone.utc)
                next_time = now + timedelta(minutes=campaign.retry_delay_minutes)
                lead.next_call_at = next_time.isoformat()
            else:
                lead.status = "failed"
        else:
            # For completed, rejected, interested, etc.
            lead.status = outcome

        # Update Campaign Stats
        if lead.status == "completed" or lead.status in ["interested", "not_interested", "qualified", "converted"]:
            campaign.completed_calls += 1
            campaign.successful_calls += 1
        elif lead.status == "failed":
            campaign.failed_calls += 1
            
        if campaign.completed_calls > 0:
            campaign.success_rate = round((campaign.successful_calls / (campaign.completed_calls + campaign.failed_calls)) * 100, 2)
            
        db.commit()

retry_engine = RetryEngine()
