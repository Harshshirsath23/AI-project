from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from datetime import datetime, timedelta

from app.modules.interviews.models import (
    InterviewTemplate, InterviewTemplateRound, InterviewTemplateCriterion,
    Interview, InterviewPanel, InterviewPanelMember, InterviewFeedback,
    FeedbackCriterionScore, InterviewScorecard, InterviewDecision,
    AssessmentTemplate, Assessment, AssessmentAttempt, EvaluationCriterion
)
from app.modules.interviews.schemas import (
    InterviewTemplateCreate, InterviewCreate, InterviewUpdate,
    InterviewRescheduleRequest, InterviewCancelRequest, InterviewPanelCreate,
    FeedbackCreate, DecisionCreate, AssessmentTemplateCreate, AssessmentCreate,
    EvaluationCriterionCreate
)
from app.modules.interviews.enums import (
    InterviewStatus, FeedbackStatus, DecisionType, RecommendationType
)
from app.modules.interviews.validators import (
    InterviewValidator, FeedbackValidator, ScorecardValidator,
    AssessmentValidator, DecisionValidator, TemplateValidator, PanelValidator
)
from app.modules.interviews.exceptions import (
    TemplateNotFound, InterviewNotFound, InterviewAlreadyCompletedException,
    InterviewCancelledException, InvalidScheduleException,
    FeedbackAlreadySubmittedException, IncompleteFeedbackException,
    DecisionAlreadyMadeException, InvalidDecisionException
)
from app.modules.interviews.repository import (
    InterviewTemplateRepository, InterviewRepository, PanelRepository,
    FeedbackRepository, ScorecardRepository, DecisionRepository,
    AssessmentRepository, EvaluationCriterionRepository
)
from app.modules.interviews.workflow_hooks import InterviewWorkflowHooks


class InterviewTemplateService:
    """Service for interview template management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.template_repo = InterviewTemplateRepository(db)
    
    async def create_template(
        self, 
        org_id: uuid.UUID, 
        template_data: InterviewTemplateCreate
    ) -> Dict[str, Any]:
        """Create a new interview template"""
        # Validate template structure
        TemplateValidator.validate_template_rounds(template_data.rounds)
        
        for round_data in template_data.rounds:
            if "criteria" in round_data:
                TemplateValidator.validate_criteria_configuration(round_data["criteria"])
        
        # Create template
        template_dict = template_data.dict()
        template = await self.template_repo.create_template(org_id, template_dict)
        
        return {
            "status": "success",
            "template_id": str(template.id),
            "message": "Interview template created successfully"
        }
    
    async def get_template(
        self, 
        org_id: uuid.UUID, 
        template_id: uuid.UUID
    ) -> Optional[InterviewTemplate]:
        """Get template by ID"""
        template = await self.template_repo.get_template_by_id(org_id, template_id)
        if not template:
            raise TemplateNotFound(str(template_id))
        return template
    
    async def get_templates(
        self, 
        org_id: uuid.UUID, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[InterviewTemplate]:
        """Get all templates for organization"""
        return await self.template_repo.get_templates_by_org(org_id, skip, limit)
    
    async def get_default_template(
        self, 
        org_id: uuid.UUID
    ) -> Optional[InterviewTemplate]:
        """Get default template for organization"""
        return await self.template_repo.get_default_template(org_id)
    
    async def delete_template(
        self, 
        org_id: uuid.UUID, 
        template_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Delete template"""
        template = await self.template_repo.get_template_by_id(org_id, template_id)
        if not template:
            raise TemplateNotFound(str(template_id))
        
        await self.template_repo.delete_template(template_id)
        return {
            "status": "success",
            "message": "Template deleted successfully"
        }


class InterviewService:
    """Service for interview management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.interview_repo = InterviewRepository(db)
        self.workflow_hooks = InterviewWorkflowHooks(db)
    
    async def create_interview(
        self, 
        org_id: uuid.UUID, 
        interview_data: InterviewCreate
    ) -> Dict[str, Any]:
        """Create a new interview"""
        # Validate schedule
        InterviewValidator.validate_schedule_time(
            interview_data.schedule.scheduled_start,
            interview_data.schedule.scheduled_end,
            interview_data.schedule.timezone
        )
        
        # Create interview
        interview_dict = interview_data.dict()
        interview_dict["organization_id"] = org_id
        interview_dict.update(interview_data.schedule.dict())
        
        interview = await self.interview_repo.create_interview(interview_dict)
        
        # Trigger workflow hook
        await self.workflow_hooks.on_interview_scheduled(
            interview.id, 
            org_id,
            interview.candidate_application_id
        )
        
        return {
            "status": "success",
            "interview_id": str(interview.id),
            "message": "Interview created successfully"
        }
    
    async def get_interview(
        self, 
        org_id: uuid.UUID, 
        interview_id: uuid.UUID
    ) -> Optional[Interview]:
        """Get interview by ID"""
        interview = await self.interview_repo.get_interview_by_id(org_id, interview_id)
        if not interview:
            raise InterviewNotFound(str(interview_id))
        return interview
    
    async def get_interviews(
        self, 
        org_id: uuid.UUID, 
        filters: Dict[str, Any] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Interview]:
        """Get interviews with filters"""
        return await self.interview_repo.get_interviews_by_org(org_id, filters, skip, limit)
    
    async def update_interview(
        self, 
        org_id: uuid.UUID, 
        interview_id: uuid.UUID, 
        update_data: InterviewUpdate
    ) -> Dict[str, Any]:
        """Update interview"""
        interview = await self.interview_repo.get_interview_by_id(org_id, interview_id)
        if not interview:
            raise InterviewNotFound(str(interview_id))
        
        # Validate status for updates
        if interview.status in [InterviewStatus.COMPLETED, InterviewStatus.DECISION_PUBLISHED]:
            raise InterviewAlreadyCompletedException(str(interview_id))
        
        if interview.status == InterviewStatus.CANCELLED:
            raise InterviewCancelledException(str(interview_id))
        
        # Update interview
        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
        await self.interview_repo.update_interview(interview_id, update_dict)
        
        return {
            "status": "success",
            "message": "Interview updated successfully"
        }
    
    async def reschedule_interview(
        self, 
        org_id: uuid.UUID, 
        interview_id: uuid.UUID, 
        reschedule_data: InterviewRescheduleRequest,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Reschedule interview"""
        interview = await self.interview_repo.get_interview_by_id(org_id, interview_id)
        if not interview:
            raise InterviewNotFound(str(interview_id))
        
        # Get template round for rescheduling rules
        # For now, use default 24 hours
        min_hours = 24
        
        # Validate rescheduling
        InterviewValidator.validate_rescheduling(
            interview.status,
            interview.scheduled_start,
            reschedule_data.new_start_time,
            min_hours
        )
        
        # Validate new schedule
        InterviewValidator.validate_schedule_time(
            reschedule_data.new_start_time,
            reschedule_data.new_end_time,
            interview.timezone
        )
        
        # Update interview
        await self.interview_repo.update_interview(
            interview_id,
            {
                "scheduled_start": reschedule_data.new_start_time,
                "scheduled_end": reschedule_data.new_end_time
            }
        )
        
        # Add audit log
        await self.interview_repo.add_audit_log(
            interview_id, 
            "Reschedule", 
            user_id
        )
        
        # Trigger workflow hook
        await self.workflow_hooks.on_interview_rescheduled(
            interview_id,
            org_id,
            reschedule_data.new_start_time,
            reschedule_data.new_end_time,
            reschedule_data.reason
        )
        
        return {
            "status": "success",
            "message": "Interview rescheduled successfully"
        }
    
    async def cancel_interview(
        self, 
        org_id: uuid.UUID, 
        interview_id: uuid.UUID, 
        cancel_data: InterviewCancelRequest,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Cancel interview"""
        interview = await self.interview_repo.get_interview_by_id(org_id, interview_id)
        if not interview:
            raise InterviewNotFound(str(interview_id))
        
        # Validate cancellation
        InterviewValidator.validate_cancellation(interview.status)
        
        # Update status
        await self.interview_repo.update_interview_status(
            interview_id, 
            InterviewStatus.CANCELLED
        )
        
        # Add audit log
        await self.interview_repo.add_audit_log(
            interview_id, 
            "Cancel", 
            user_id
        )
        
        # Trigger workflow hook
        await self.workflow_hooks.on_interview_cancelled(
            interview_id,
            org_id,
            cancel_data.reason
        )
        
        return {
            "status": "success",
            "message": "Interview cancelled successfully"
        }
    
    async def start_interview(
        self, 
        org_id: uuid.UUID, 
        interview_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Mark interview as started"""
        interview = await self.interview_repo.get_interview_by_id(org_id, interview_id)
        if not interview:
            raise InterviewNotFound(str(interview_id))
        
        # Update status and actual start time
        await self.interview_repo.update_interview(
            interview_id,
            {
                "status": InterviewStatus.STARTED,
                "actual_start": datetime.now()
            }
        )
        
        # Trigger workflow hook
        await self.workflow_hooks.on_interview_started(interview_id, org_id)
        
        return {
            "status": "success",
            "message": "Interview started successfully"
        }
    
    async def complete_interview(
        self, 
        org_id: uuid.UUID, 
        interview_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Mark interview as completed"""
        interview = await self.interview_repo.get_interview_by_id(org_id, interview_id)
        if not interview:
            raise InterviewNotFound(str(interview_id))
        
        # Update status and actual end time
        await self.interview_repo.update_interview(
            interview_id,
            {
                "status": InterviewStatus.COMPLETED,
                "actual_end": datetime.now()
            }
        )
        
        # Trigger workflow hook
        await self.workflow_hooks.on_interview_completed(interview_id, org_id)
        
        return {
            "status": "success",
            "message": "Interview completed successfully"
        }


class PanelService:
    """Service for interview panel management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.panel_repo = PanelRepository(db)
    
    async def create_panel(
        self, 
        interview_id: uuid.UUID, 
        panel_data: InterviewPanelCreate
    ) -> Dict[str, Any]:
        """Create interview panel"""
        # Validate panel composition
        PanelValidator.validate_panel_composition(
            len(panel_data.members),
            1,  # At least 1 required
            sum(1 for m in panel_data.members if m.is_primary)
        )
        
        panel_dict = panel_data.dict()
        panel = await self.panel_repo.create_panel(interview_id, panel_dict)
        
        return {
            "status": "success",
            "panel_id": str(panel.id),
            "message": "Panel created successfully"
        }
    
    async def get_panel(
        self, 
        interview_id: uuid.UUID
    ) -> Optional[InterviewPanel]:
        """Get panel for interview"""
        return await self.panel_repo.get_panel_by_interview(interview_id)
    
    async def add_panel_member(
        self, 
        panel_id: uuid.UUID, 
        member_data: dict
    ) -> Dict[str, Any]:
        """Add member to panel"""
        member = await self.panel_repo.add_panel_member(panel_id, member_data)
        return {
            "status": "success",
            "member_id": str(member.id),
            "message": "Panel member added successfully"
        }


class FeedbackService:
    """Service for interview feedback management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.feedback_repo = FeedbackRepository(db)
        self.interview_repo = InterviewRepository(db)
        self.panel_repo = PanelRepository(db)
        self.workflow_hooks = InterviewWorkflowHooks(db)
    
    async def submit_feedback(
        self, 
        org_id: uuid.UUID, 
        interview_id: uuid.UUID, 
        feedback_data: FeedbackCreate
    ) -> Dict[str, Any]:
        """Submit interview feedback"""
        interview = await self.interview_repo.get_interview_by_id(org_id, interview_id)
        if not interview:
            raise InterviewNotFound(str(interview_id))
        
        # Check if feedback already exists
        existing_feedback = await self.feedback_repo.get_feedback_by_interviewer(
            interview_id, 
            feedback_data.interviewer_id
        )
        if existing_feedback:
            raise FeedbackAlreadySubmittedException(str(feedback_data.interviewer_id))
        
        # Validate feedback completeness
        required_criteria = len([c for c in feedback_data.criterion_scores if c.is_required])
        scored_criteria = len(feedback_data.criterion_scores)
        
        FeedbackValidator.validate_feedback_submission(
            interview.status,
            "Pending",  # New feedback
            required_criteria,
            scored_criteria
        )
        
        # Validate individual scores
        for score_data in feedback_data.criterion_scores:
            FeedbackValidator.validate_criterion_score(
                score_data.score,
                score_data.max_score,
                "Score"  # Default evaluation type
            )
        
        # Validate recommendation if provided
        if feedback_data.recommendation:
            FeedbackValidator.validate_recommendation(feedback_data.recommendation)
        
        # Create feedback
        feedback_dict = feedback_data.dict()
        feedback_dict["interview_id"] = interview_id
        feedback = await self.feedback_repo.create_feedback(feedback_dict)
        
        # Update panel member feedback status if applicable
        if feedback_data.panel_member_id:
            await self.panel_repo.update_member_feedback_status(
                feedback_data.panel_member_id,
                FeedbackStatus.SUBMITTED
            )
        
        # Get total feedback count for the interview
        all_feedback = await self.feedback_repo.get_feedback_by_interview(interview_id)
        
        # Trigger workflow hook
        await self.workflow_hooks.on_feedback_submitted(
            interview_id,
            org_id,
            len(all_feedback),
            1  # Required feedback count (should come from template)
        )
        
        return {
            "status": "success",
            "feedback_id": str(feedback.id),
            "message": "Feedback submitted successfully"
        }
    
    async def get_feedback(
        self, 
        interview_id: uuid.UUID
    ) -> List[InterviewFeedback]:
        """Get all feedback for interview"""
        return await self.feedback_repo.get_feedback_by_interview(interview_id)


class ScorecardService:
    """Service for scorecard management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.scorecard_repo = ScorecardRepository(db)
        self.feedback_repo = FeedbackRepository(db)
        self.interview_repo = InterviewRepository(db)
        self.workflow_hooks = InterviewWorkflowHooks(db)
    
    async def calculate_scorecard(
        self, 
        org_id: uuid.UUID, 
        interview_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Calculate interview scorecard from all feedback"""
        interview = await self.interview_repo.get_interview_by_id(org_id, interview_id)
        if not interview:
            raise InterviewNotFound(str(interview_id))
        
        # Get all feedback
        feedback_list = await self.feedback_repo.get_feedback_by_interview(interview_id)
        
        if not feedback_list:
            raise IncompleteFeedbackException("No feedback available for scorecard calculation")
        
        # Calculate weighted scores
        total_score = 0.0
        max_possible_score = 0.0
        total_weight = 0.0
        
        for feedback in feedback_list:
            if feedback.overall_score:
                total_score += feedback.overall_score
                max_possible_score += 10.0  # Assuming max score of 10
                total_weight += 1.0
        
        # Calculate percentage
        percentage_score = (total_score / max_possible_score * 100) if max_possible_score > 0 else 0.0
        
        # Determine recommendation based on percentage
        if percentage_score >= 80:
            recommendation = "Pass"
            confidence = 0.9
        elif percentage_score >= 60:
            recommendation = "Hold"
            confidence = 0.7
        else:
            recommendation = "Fail"
            confidence = 0.8
        
        # Create scorecard
        scorecard_data = {
            "interview_id": interview_id,
            "template_round_id": interview.template_round_id,
            "overall_score": total_score,
            "max_possible_score": max_possible_score,
            "percentage_score": percentage_score,
            "recommendation": recommendation,
            "recommendation_confidence": confidence,
            "summary": f"Overall score: {percentage_score:.1f}%. Recommendation: {recommendation}",
            "required_feedback_count": 1,
            "received_feedback_count": len(feedback_list)
        }
        
        scorecard = await self.scorecard_repo.create_scorecard(scorecard_data)
        
        # Trigger workflow hook
        await self.workflow_hooks.on_scorecard_calculated(
            interview_id,
            org_id,
            scorecard_data
        )
        
        return {
            "status": "success",
            "scorecard_id": str(scorecard.id),
            "overall_score": total_score,
            "percentage_score": percentage_score,
            "recommendation": recommendation
        }
    
    async def get_scorecard(
        self, 
        interview_id: uuid.UUID
    ) -> Optional[InterviewScorecard]:
        """Get scorecard for interview"""
        return await self.scorecard_repo.get_scorecard_by_interview(interview_id)


class DecisionService:
    """Service for interview decision management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.decision_repo = DecisionRepository(db)
        self.interview_repo = InterviewRepository(db)
        self.workflow_hooks = InterviewWorkflowHooks(db)
    
    async def make_decision(
        self, 
        org_id: uuid.UUID, 
        interview_id: uuid.UUID, 
        decision_data: DecisionCreate,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Make final hiring decision"""
        interview = await self.interview_repo.get_interview_by_id(org_id, interview_id)
        if not interview:
            raise InterviewNotFound(str(interview_id))
        
        # Check if decision already exists
        existing_decision = await self.decision_repo.get_decision_by_interview(interview_id)
        if existing_decision:
            raise DecisionAlreadyMadeException(str(interview_id))
        
        # Validate decision value
        DecisionValidator.validate_decision_value(decision_data.decision)
        
        # Validate interview status
        DecisionValidator.validate_decision_creation(
            interview.status,
            existing_decision is not None
        )
        
        # Create decision
        decision_dict = decision_data.dict()
        decision_dict["interview_id"] = interview_id
        decision_dict["decision_maker_id"] = user_id
        decision = await self.decision_repo.create_decision(decision_dict)
        
        # Add audit log
        await self.interview_repo.add_audit_log(
            interview_id, 
            "Make Decision", 
            user_id
        )
        
        # Trigger workflow hook
        await self.workflow_hooks.on_decision_made(
            interview_id,
            org_id,
            decision_data.decision,
            interview.candidate_application_id
        )
        
        return {
            "status": "success",
            "decision_id": str(decision.id),
            "decision": decision_data.decision,
            "message": "Decision recorded successfully"
        }
    
    async def get_decision(
        self, 
        interview_id: uuid.UUID
    ) -> Optional[InterviewDecision]:
        """Get decision for interview"""
        return await self.decision_repo.get_decision_by_interview(interview_id)


class AssessmentService:
    """Service for assessment management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.assessment_repo = AssessmentRepository(db)
    
    async def create_assessment_template(
        self, 
        org_id: uuid.UUID, 
        template_data: AssessmentTemplateCreate
    ) -> Dict[str, Any]:
        """Create assessment template"""
        template_dict = template_data.dict()
        template = await self.assessment_repo.create_assessment_template(org_id, template_dict)
        
        return {
            "status": "success",
            "template_id": str(template.id),
            "message": "Assessment template created successfully"
        }
    
    async def create_assessment(
        self, 
        org_id: uuid.UUID, 
        assessment_data: AssessmentCreate
    ) -> Dict[str, Any]:
        """Create assessment"""
        assessment_dict = assessment_data.dict()
        assessment_dict["organization_id"] = org_id
        assessment = await self.assessment_repo.create_assessment(assessment_dict)
        
        return {
            "status": "success",
            "assessment_id": str(assessment.id),
            "message": "Assessment created successfully"
        }


class EvaluationCriterionService:
    """Service for evaluation criterion management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.criterion_repo = EvaluationCriterionRepository(db)
    
    async def create_criterion(
        self, 
        org_id: uuid.UUID, 
        criterion_data: EvaluationCriterionCreate
    ) -> Dict[str, Any]:
        """Create evaluation criterion"""
        criterion_dict = criterion_data.dict()
        criterion = await self.criterion_repo.create_criterion(org_id, criterion_dict)
        
        return {
            "status": "success",
            "criterion_id": str(criterion.id),
            "message": "Evaluation criterion created successfully"
        }
    
    async def get_criteria(
        self, 
        org_id: uuid.UUID, 
        category: Optional[str] = None
    ) -> List[EvaluationCriterion]:
        """Get evaluation criteria for organization"""
        return await self.criterion_repo.get_criteria_by_org(org_id, category)