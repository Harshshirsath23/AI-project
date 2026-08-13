import asyncio
import logging
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.campaign import Campaign
from app.models.lead import Lead
from app.models.phone_number import PhoneNumber
from app.services.telephony_service import telephony_provider
from app.config.settings import get_settings

logger = logging.getLogger(__name__)

class CampaignScheduler:
    """Manages manual start/stop/pause actions and background dialing for campaigns."""

    def __init__(self):
        self._active_tasks = {}

    def start_campaign(self, db: Session, campaign_id: str):
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if campaign:
            campaign.status = "running"
            db.commit()
            
            # Cancel any existing task for this campaign
            if campaign_id in self._active_tasks and not self._active_tasks[campaign_id].done():
                self._active_tasks[campaign_id].cancel()

            # Spawn background execution worker
            task = asyncio.create_task(self._run_campaign_dialer(campaign_id))
            self._active_tasks[campaign_id] = task

    def pause_campaign(self, db: Session, campaign_id: str):
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if campaign:
            campaign.status = "paused"
            db.commit()
            if campaign_id in self._active_tasks and not self._active_tasks[campaign_id].done():
                self._active_tasks[campaign_id].cancel()

    def stop_campaign(self, db: Session, campaign_id: str):
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if campaign:
            campaign.status = "completed"
            db.commit()
            if campaign_id in self._active_tasks and not self._active_tasks[campaign_id].done():
                self._active_tasks[campaign_id].cancel()

    async def _dial_single_lead(self, semaphore: asyncio.Semaphore, campaign_id: str, lead_id: str, from_num: str, base_url: str):
        """Worker function to dial a single lead respecting the campaign's concurrency semaphore."""
        async with semaphore:
            with SessionLocal() as db:
                campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
                lead = db.query(Lead).filter(Lead.id == lead_id).first()

                if not campaign or not lead or campaign.status != "running":
                    return

                lead.status = "calling"
                lead.call_attempts += 1
                db.commit()

                webhook_url = f"{base_url}/api/v1/webhooks/twilio/voice?lead_id={lead.id}"
                status_callback_url = f"{base_url}/api/v1/webhooks/twilio/call-status?lead_id={lead.id}"

                try:
                    logger.info(f"Campaign {campaign_id}: Concurrency Dialing lead {lead.name} ({lead.phone_number})...")
                    call_sid = await telephony_provider.initiate_call(
                        from_number=from_num,
                        to_number=lead.phone_number,
                        webhook_url=webhook_url,
                        status_callback_url=status_callback_url
                    )
                    lead.status = "completed"
                    campaign.completed_calls += 1
                    campaign.successful_calls += 1
                except Exception as e:
                    logger.error(f"Campaign {campaign_id}: Call failed for lead {lead.id}: {e}")
                    lead.status = "failed"
                    campaign.completed_calls += 1
                    campaign.failed_calls += 1

                total = campaign.total_leads or 1
                campaign.success_rate = round((campaign.successful_calls / total) * 100, 1)
                db.commit()

    async def _run_campaign_dialer(self, campaign_id: str):
        """Background worker that dials pending leads up to max_concurrent_calls in parallel."""
        logger.info(f"Campaign {campaign_id}: Concurrency Dialer task started.")
        try:
            with SessionLocal() as db:
                campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
                if not campaign:
                    return

                max_concurrent = campaign.max_concurrent_calls or 5

                # Get from_number
                from_num = None
                if campaign.phone_numbers and isinstance(campaign.phone_numbers, dict):
                    from_num = campaign.phone_numbers.get("from_number")
                if not from_num:
                    default_phone = db.query(PhoneNumber).filter_by(status="active").first()
                    from_num = default_phone.number if default_phone else "+17372212163"

                # Get pending leads
                leads = db.query(Lead).filter(
                    Lead.campaign_id == campaign_id,
                    Lead.status.in_(["pending", "queued"])
                ).all()

                if not leads:
                    logger.info(f"Campaign {campaign_id}: No pending leads found.")
                    campaign.status = "completed"
                    db.commit()
                    return

                lead_ids = [str(l.id) for l in leads]

            settings = get_settings()
            base_url = getattr(settings, "webhook_base_url", "http://localhost:8000").rstrip("/")

            # Enforce max_concurrent_calls concurrency limit
            semaphore = asyncio.Semaphore(max_concurrent)
            logger.info(f"Campaign {campaign_id}: Dialing {len(lead_ids)} leads with Max Concurrency = {max_concurrent}")

            dial_tasks = [
                self._dial_single_lead(semaphore, campaign_id, lead_id, from_num, base_url)
                for lead_id in lead_ids
            ]
            await asyncio.gather(*dial_tasks, return_exceptions=True)

            with SessionLocal() as db:
                campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
                if campaign and campaign.completed_calls >= campaign.total_leads:
                    campaign.status = "completed"
                    db.commit()

        except asyncio.CancelledError:
            logger.info(f"Campaign {campaign_id}: Dialer task cancelled.")
        except Exception as e:
            logger.error(f"Campaign {campaign_id}: Dialer worker error: {e}")

campaign_scheduler = CampaignScheduler()
