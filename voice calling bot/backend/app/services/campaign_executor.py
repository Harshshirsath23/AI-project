import asyncio
from typing import Dict
from sqlalchemy.orm import Session
import httpx
from datetime import datetime, timezone

from app.database.connection import SessionLocal
from app.models.campaign import Campaign
from app.models.lead import Lead
from app.models.call import Call
from app.services.business_hours_engine import business_hours_engine
from app.services.queue_service import queue_service

class CampaignExecutor:
    """Background worker that continuously polls for running campaigns and executes calls."""
    
    def __init__(self):
        self.is_running = False
        self.active_calls_per_campaign: Dict[str, int] = {}
        
    async def start(self):
        self.is_running = True
        asyncio.create_task(self._worker_loop())
        
    async def stop(self):
        self.is_running = False
        
    async def _worker_loop(self):
        while self.is_running:
            try:
                db: Session = SessionLocal()
                # Find all running campaigns
                running_campaigns = db.query(Campaign).filter(Campaign.status == "running").all()
                
                for campaign in running_campaigns:
                    # 1. Check business hours
                    if not business_hours_engine.is_within_business_hours(
                        campaign.calling_timezone, 
                        campaign.calling_window_start, 
                        campaign.calling_window_end
                    ):
                        continue
                        
                    # 2. Check concurrency
                    active_count = db.query(Call).filter(
                        Call.campaign_id == campaign.id,
                        Call.status.in_(["queued", "in-progress", "ringing"])
                    ).count()
                    
                    available_slots = campaign.max_concurrent_calls - active_count
                    if available_slots <= 0:
                        continue
                        
                    # 3. Pull leads
                    leads_to_call = queue_service.get_next_leads(db, campaign.id, limit=available_slots)
                    
                    for lead in leads_to_call:
                        # 4. Dispatch Call (Internal HTTP request for MVP)
                        # Pick first agent and phone for MVP
                        agent_id = campaign.agent_ids.get("agents", [])[0] if campaign.agent_ids else campaign.agent_id
                        from_phone = campaign.phone_numbers.get("numbers", [])[0] if campaign.phone_numbers else "+1234567890"
                        
                        try:
                            # In production, this would use a proper internal service call or Celery task.
                            # We'll mock the trigger here to simulate hitting the /calls/start API
                            print(f"Executor: Starting call for Lead {lead.name} ({lead.phone_number})")
                        except Exception as e:
                            print(f"Failed to dial lead: {e}")
                            lead.status = "failed"
                            db.commit()
                            
                db.close()
            except Exception as e:
                print(f"Error in CampaignExecutor loop: {e}")
                
            await asyncio.sleep(5) # Poll every 5 seconds

campaign_executor = CampaignExecutor()
