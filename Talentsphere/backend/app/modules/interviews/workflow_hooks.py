from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from datetime import datetime

from app.modules.interviews.enums import InterviewStatus, DecisionType
from app.modules.interviews.exceptions import InterviewException
from app.modules.interviews.repository import (
    InterviewRepository, DecisionRepository, ScorecardRepository
)


class InterviewWorkflowHooks:
    """
    Integration hooks between Interview system and Recruitment Workflow.
    These hooks connect interview lifecycle events to recruitment pipeline transitions.
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.interview_repo = InterviewRepository(db)
        self.decision_repo = DecisionRepository(db)
        self.scorecard_repo = ScorecardRepository(db)
    
    async def on_interview_scheduled(
        self, 
        interview_id: uuid.UUID, 
        organization_id: uuid.UUID,
        application_id: uuid.UUID
    ) -> Dict[str, Any]:
        """
        Hook called when interview is scheduled.
        Can trigger notifications, calendar events, and workflow updates.
        """
        interview = await self.interview_repo.get_interview_by_id(
            organization_id, 
            interview_id
        )
        
        if not interview:
            raise InterviewException("Interview not found")
        
        # Timeline event is already added in repository
        # Additional workflow logic can be added here
        
        return {
            "status": "success",
            "message": "Interview scheduled hook processed",
            "interview_id": str(interview_id),
            "application_id": str(application_id),
            "scheduled_start": interview.scheduled_start.isoformat()
        }
    
    async def on_interview_started(
        self, 
        interview_id: uuid.UUID,
        organization_id: uuid.UUID
    ) -> Dict[str, Any]:
        """
        Hook called when interview starts.
        Updates interview status and triggers any start-time events.
        """
        interview = await self.interview_repo.get_interview_by_id(
            organization_id, 
            interview_id
        )
        
        if not interview:
            raise InterviewException("Interview not found")
        
        # Update status to Started
        await self.interview_repo.update_interview_status(
            interview_id, 
            InterviewStatus.STARTED
        )
        
        # Add timeline event
        await self.interview_repo._add_timeline_event(
            interview_id, 
            "Interview Started"
        )
        
        return {
            "status": "success",
            "message": "Interview started hook processed",
            "interview_id": str(interview_id),
            "actual_start": datetime.now().isoformat()
        }
    
    async def on_interview_completed(
        self, 
        interview_id: uuid.UUID,
        organization_id: uuid.UUID
    ) -> Dict[str, Any]:
        """
        Hook called when interview completes.
        Updates status and triggers feedback request workflow.
        """
        interview = await self.interview_repo.get_interview_by_id(
            organization_id, 
            interview_id
        )
        
        if not interview:
            raise InterviewException("Interview not found")
        
        # Update status to Completed
        await self.interview_repo.update_interview_status(
            interview_id, 
            InterviewStatus.COMPLETED
        )
        
        # Update actual end time
        await self.interview_repo.update_interview(
            interview_id, 
            {"actual_end": datetime.now()}
        )
        
        # Add timeline event
        await self.interview_repo._add_timeline_event(
            interview_id, 
            "Interview Completed"
        )
        
        # Trigger feedback request notifications
        # This would integrate with notification system
        
        return {
            "status": "success",
            "message": "Interview completed hook processed",
            "interview_id": str(interview_id),
            "actual_end": datetime.now().isoformat(),
            "next_action": "request_feedback"
        }
    
    async def on_feedback_submitted(
        self, 
        interview_id: uuid.UUID, 
        organization_id: uuid.UUID,
        feedback_count: int, 
        required_count: int
    ) -> Dict[str, Any]:
        """
        Hook called when feedback is submitted.
        Checks if all required feedback is received and triggers evaluation.
        """
        interview = await self.interview_repo.get_interview_by_id(
            organization_id, 
            interview_id
        )
        
        if not interview:
            raise InterviewException("Interview not found")
        
        # Add timeline event
        await self.interview_repo._add_timeline_event(
            interview_id, 
            "Feedback Submitted"
        )
        
        # Check if all required feedback is received
        if feedback_count >= required_count:
            # Update interview status
            await self.interview_repo.update_interview_status(
                interview_id, 
                InterviewStatus.FEEDBACK_SUBMITTED
            )
            
            return {
                "status": "success",
                "message": "All feedback received, ready for evaluation",
                "interview_id": str(interview_id),
                "feedback_count": feedback_count,
                "required_count": required_count,
                "next_action": "calculate_scorecard"
            }
        
        return {
            "status": "success",
            "message": "Feedback submitted, awaiting more feedback",
            "interview_id": str(interview_id),
            "feedback_count": feedback_count,
            "required_count": required_count,
            "next_action": "await_feedback"
        }
    
    async def on_scorecard_calculated(
        self, 
        interview_id: uuid.UUID, 
        organization_id: uuid.UUID,
        scorecard_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Hook called when scorecard is calculated.
        Updates interview status and prepares for decision.
        """
        interview = await self.interview_repo.get_interview_by_id(
            organization_id, 
            interview_id
        )
        
        if not interview:
            raise InterviewException("Interview not found")
        
        # Update interview status
        await self.interview_repo.update_interview_status(
            interview_id, 
            InterviewStatus.EVALUATION_COMPLETED
        )
        
        # Add timeline event
        await self.interview_repo._add_timeline_event(
            interview_id, 
            "Evaluation Generated"
        )
        
        return {
            "status": "success",
            "message": "Scorecard calculated hook processed",
            "interview_id": str(interview_id),
            "overall_score": scorecard_data["overall_score"],
            "recommendation": scorecard_data["recommendation"],
            "next_action": "await_decision"
        }
    
    async def on_decision_made(
        self, 
        interview_id: uuid.UUID, 
        organization_id: uuid.UUID,
        decision: str, 
        application_id: uuid.UUID
    ) -> Dict[str, Any]:
        """
        Hook called when hiring decision is made.
        This is the critical integration point with recruitment workflow.
        Triggers pipeline transition based on decision.
        """
        interview = await self.interview_repo.get_interview_by_id(
            organization_id, 
            interview_id
        )
        
        if not interview:
            raise InterviewException("Interview not found")
        
        # Update interview status
        await self.interview_repo.update_interview_status(
            interview_id, 
            InterviewStatus.DECISION_PUBLISHED
        )
        
        # Add timeline event
        await self.interview_repo._add_timeline_event(
            interview_id, 
            "Decision Made"
        )
        
        # Determine recruitment workflow action based on decision
        workflow_action = self._map_decision_to_workflow_action(decision)
        
        # This would integrate with the recruitment workflow engine
        # For now, we return the action that should be taken
        return {
            "status": "success",
            "message": "Decision made hook processed",
            "interview_id": str(interview_id),
            "application_id": str(application_id),
            "decision": decision,
            "workflow_action": workflow_action,
            "next_step": self._get_next_stage_for_decision(decision)
        }
    
    async def on_interview_rescheduled(
        self, 
        interview_id: uuid.UUID, 
        organization_id: uuid.UUID,
        new_start: datetime, 
        new_end: datetime, 
        reason: str
    ) -> Dict[str, Any]:
        """
        Hook called when interview is rescheduled.
        Updates schedule and triggers notifications.
        """
        interview = await self.interview_repo.get_interview_by_id(
            organization_id, 
            interview_id
        )
        
        if not interview:
            raise InterviewException("Interview not found")
        
        # Update interview status
        await self.interview_repo.update_interview_status(
            interview_id, 
            InterviewStatus.RESCHEDULED
        )
        
        # Update schedule
        await self.interview_repo.update_interview(
            interview_id, 
            {
                "scheduled_start": new_start,
                "scheduled_end": new_end
            }
        )
        
        # Add timeline event
        await self.interview_repo._add_timeline_event(
            interview_id, 
            "Interview Rescheduled"
        )
        
        # Trigger rescheduling notifications
        # This would integrate with notification system
        
        return {
            "status": "success",
            "message": "Interview rescheduled hook processed",
            "interview_id": str(interview_id),
            "new_start": new_start.isoformat(),
            "new_end": new_end.isoformat(),
            "reason": reason
        }
    
    async def on_interview_cancelled(
        self, 
        interview_id: uuid.UUID, 
        organization_id: uuid.UUID,
        reason: str
    ) -> Dict[str, Any]:
        """
        Hook called when interview is cancelled.
        Updates status and triggers notifications.
        """
        interview = await self.interview_repo.get_interview_by_id(
            organization_id, 
            interview_id
        )
        
        if not interview:
            raise InterviewException("Interview not found")
        
        # Update interview status
        await self.interview_repo.update_interview_status(
            interview_id, 
            InterviewStatus.CANCELLED
        )
        
        # Add timeline event
        await self.interview_repo._add_timeline_event(
            interview_id, 
            "Interview Cancelled"
        )
        
        # Trigger cancellation notifications
        # This would integrate with notification system
        
        return {
            "status": "success",
            "message": "Interview cancelled hook processed",
            "interview_id": str(interview_id),
            "reason": reason
        }
    
    async def on_interview_no_show(
        self, 
        interview_id: uuid.UUID,
        organization_id: uuid.UUID
    ) -> Dict[str, Any]:
        """
        Hook called when candidate doesn't show up for interview.
        Updates status and may trigger rescheduling or rejection workflow.
        """
        interview = await self.interview_repo.get_interview_by_id(
            organization_id, 
            interview_id
        )
        
        if not interview:
            raise InterviewException("Interview not found")
        
        # Update interview status
        await self.interview_repo.update_interview_status(
            interview_id, 
            InterviewStatus.NO_SHOW
        )
        
        # Add timeline event
        await self.interview_repo._add_timeline_event(
            interview_id, 
            "No Show"
        )
        
        return {
            "status": "success",
            "message": "No show hook processed",
            "interview_id": str(interview_id),
            "next_action": "review_no_show"
        }
    
    def _map_decision_to_workflow_action(self, decision: str) -> str:
        """Map interview decision to recruitment workflow action"""
        decision_mapping = {
            DecisionType.PASS: "advance_to_next_stage",
            DecisionType.FAIL: "reject_candidate",
            DecisionType.HOLD: "hold_for_review",
            DecisionType.REVIEW_REQUIRED: "escalate_to_manager"
        }
        return decision_mapping.get(decision, "unknown")
    
    def _get_next_stage_for_decision(self, decision: str) -> Optional[str]:
        """Get next recruitment stage based on decision"""
        if decision == DecisionType.PASS:
            return "next_interview_round_or_offer"
        elif decision == DecisionType.FAIL:
            return "rejected"
        elif decision == DecisionType.HOLD:
            return "on_hold"
        elif decision == DecisionType.REVIEW_REQUIRED:
            return "manager_review"
        return None


class RecruitmentWorkflowIntegration:
    """
    Integration service for connecting interview decisions to recruitment workflow.
    This would extend the existing RecruitmentWorkflowEngine from the recruitment module.
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.workflow_hooks = InterviewWorkflowHooks(db)
    
    async def process_interview_decision_for_workflow(
        self, 
        interview_id: uuid.UUID, 
        organization_id: uuid.UUID,
        decision: str, 
        application_id: uuid.UUID
    ) -> Dict[str, Any]:
        """
        Process interview decision and integrate with recruitment workflow.
        This method would call the existing recruitment workflow engine.
        """
        # First process the interview decision hook
        hook_result = await self.workflow_hooks.on_decision_made(
            interview_id, 
            organization_id,
            decision, 
            application_id
        )
        
        # Here you would integrate with the existing RecruitmentWorkflowEngine
        # from app.modules.recruitment.workflow_engine import WorkflowEngine
        # workflow_engine = WorkflowEngine(self.db)
        # transition_result = await workflow_engine.execute_stage_transition(...)
        
        # For now, return the hook result with workflow integration placeholder
        return {
            **hook_result,
            "workflow_integration": "pending_recruitment_module_integration",
            "note": "This should integrate with RecruitmentWorkflowEngine from recruitment module"
        }
    
    async def get_interview_context_for_workflow(
        self, 
        interview_id: uuid.UUID,
        organization_id: uuid.UUID
    ) -> Dict[str, Any]:
        """
        Get interview context for recruitment workflow decision making.
        """
        interview = await self.workflow_hooks.interview_repo.get_interview_by_id(
            organization_id, 
            interview_id
        )
        
        if not interview:
            raise InterviewException("Interview not found")
        
        # Get scorecard if exists
        scorecard = await self.workflow_hooks.scorecard_repo.get_scorecard_by_interview(
            interview_id
        )
        
        # Get decision if exists
        decision = await self.workflow_hooks.decision_repo.get_decision_by_interview(
            interview_id
        )
        
        return {
            "interview_id": str(interview_id),
            "interview_status": interview.status,
            "scheduled_start": interview.scheduled_start.isoformat(),
            "scheduled_end": interview.scheduled_end.isoformat(),
            "scorecard": {
                "overall_score": scorecard.overall_score if scorecard else None,
                "recommendation": scorecard.recommendation if scorecard else None,
                "percentage_score": scorecard.percentage_score if scorecard else None
            } if scorecard else None,
            "decision": {
                "decision": decision.decision if decision else None,
                "decision_maker_role": decision.decision_maker_role if decision else None,
                "justification": decision.justification if decision else None
            } if decision else None
        }