from sqlalchemy.orm import Session
from app.models.campaign import Campaign

class CampaignScheduler:
    """Manages manual start/stop/pause actions for campaigns."""

    def start_campaign(self, db: Session, campaign_id: str):
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if campaign:
            campaign.status = "running"
            db.commit()

    def pause_campaign(self, db: Session, campaign_id: str):
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if campaign:
            campaign.status = "paused"
            db.commit()

    def stop_campaign(self, db: Session, campaign_id: str):
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if campaign:
            campaign.status = "completed"
            db.commit()

campaign_scheduler = CampaignScheduler()
