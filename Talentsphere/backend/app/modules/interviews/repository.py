from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, update, delete
from sqlalchemy.orm import selectinload
import uuid
from datetime import datetime, timedelta

from app.modules.interviews.models import (
    InterviewTemplate, InterviewTemplateRound, InterviewTemplateCriterion,
    InterviewType, InterviewMode, Interview, InterviewPanel, InterviewPanelMember,
    InterviewerAssignment, EvaluationCriterion, InterviewFeedback, FeedbackCriterionScore,
    InterviewScorecard, InterviewDecision, AssessmentType, AssessmentTemplate,
    AssessmentQuestion, Assessment, AssessmentAttempt, AssessmentAnswer,
    CodingTest, CodingSubmission, InterviewTimeline, InterviewAuditLog,
    AiInterviewAnalysis, AiInterviewScore, AiBehaviorAnalysis
)
from app.modules.interviews.enums import InterviewStatus, FeedbackStatus


class InterviewTemplateRepository:
    """Repository for interview template operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_template(
        self, 
        org_id: uuid.UUID, 
        template_data: dict
    ) -> InterviewTemplate:
        """Create a new interview template"""
        template = InterviewTemplate(
            organization_id=org_id,
            template_name=template_data["template_name"],
            description=template_data.get("description"),
            job_category=template_data.get("job_category"),
            is_default=template_data.get("is_default", False)
        )
        self.db.add(template)
        await self.db.flush()
        
        # Create rounds
        for round_data in template_data["rounds"]:
            round_record = InterviewTemplateRound(
                template_id=template.id,
                round_name=round_data["round_name"],
                sequence_number=round_data["sequence_number"],
                duration_minutes=round_data["duration_minutes"],
                interview_mode=round_data["interview_mode"],
                required_interviewers=round_data["required_interviewers"],
                panel_required=round_data["panel_required"],
                interviewer_role_requirements=round_data.get("interviewer_role_requirements"),
                rescheduling_allowed=round_data["rescheduling_allowed"],
                min_rescheduling_hours=round_data["min_rescheduling_hours"],
                passing_threshold=round_data["passing_threshold"],
                feedback_required=round_data["feedback_required"]
            )
            self.db.add(round_record)
            await self.db.flush()
            
            # Create criteria for this round
            if "criteria" in round_data:
                for criterion_data in round_data["criteria"]:
                    criterion = InterviewTemplateCriterion(
                        round_id=round_record.id,
                        criterion_name=criterion_data["criterion_name"],
                        description=criterion_data.get("description"),
                        weight=criterion_data["weight"],
                        max_score=criterion_data["max_score"],
                        is_required=criterion_data["is_required"],
                        evaluation_type=criterion_data["evaluation_type"]
                    )
                    self.db.add(criterion)
        
        await self.db.commit()
        return template
    
    async def get_template_by_id(
        self, 
        org_id: uuid.UUID, 
        template_id: uuid.UUID
    ) -> Optional[InterviewTemplate]:
        """Get template by ID with rounds and criteria"""
        query = select(InterviewTemplate).where(
            and_(
                InterviewTemplate.id == template_id,
                InterviewTemplate.organization_id == org_id
            )
        ).options(
            selectinload(InterviewTemplate.rounds).selectinload(
                InterviewTemplateRound.criteria
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_templates_by_org(
        self, 
        org_id: uuid.UUID, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[InterviewTemplate]:
        """Get all templates for an organization"""
        query = select(InterviewTemplate).where(
            InterviewTemplate.organization_id == org_id
        ).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_default_template(
        self, 
        org_id: uuid.UUID
    ) -> Optional[InterviewTemplate]:
        """Get default template for organization"""
        query = select(InterviewTemplate).where(
            and_(
                InterviewTemplate.organization_id == org_id,
                InterviewTemplate.is_default == True
            )
        ).options(
            selectinload(InterviewTemplate.rounds).selectinload(
                InterviewTemplateRound.criteria
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_template(
        self, 
        template_id: uuid.UUID, 
        update_data: dict
    ) -> Optional[InterviewTemplate]:
        """Update template"""
        query = update(InterviewTemplate).where(
            InterviewTemplate.id == template_id
        ).values(**update_data)
        await self.db.execute(query)
        await self.db.commit()
        return await self.get_template_by_id(
            update_data.get("organization_id"), 
            template_id
        )
    
    async def delete_template(self, template_id: uuid.UUID) -> bool:
        """Delete template"""
        query = delete(InterviewTemplate).where(
            InterviewTemplate.id == template_id
        )
        await self.db.execute(query)
        await self.db.commit()
        return True


class InterviewRepository:
    """Repository for interview operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_interview(self, interview_data: dict) -> Interview:
        """Create a new interview"""
        interview = Interview(
            organization_id=interview_data["organization_id"],
            candidate_application_id=interview_data["candidate_application_id"],
            template_round_id=interview_data["template_round_id"],
            interview_type_id=interview_data["interview_type_id"],
            interview_mode_id=interview_data["interview_mode_id"],
            job_id=interview_data["job_id"],
            candidate_id=interview_data["candidate_id"],
            scheduled_start=interview_data["scheduled_start"],
            scheduled_end=interview_data["scheduled_end"],
            timezone=interview_data["timezone"],
            location=interview_data.get("location"),
            meeting_url=interview_data.get("meeting_url"),
            meeting_password=interview_data.get("meeting_password"),
            notes=interview_data.get("notes"),
            internal_notes=interview_data.get("internal_notes"),
            status=InterviewStatus.SCHEDULED
        )
        self.db.add(interview)
        await self.db.flush()
        
        # Create timeline event
        await self._add_timeline_event(
            interview.id, 
            "Interview Scheduled"
        )
        
        await self.db.commit()
        return interview
    
    async def get_interview_by_id(
        self, 
        org_id: uuid.UUID, 
        interview_id: uuid.UUID
    ) -> Optional[Interview]:
        """Get interview by ID"""
        query = select(Interview).where(
            and_(
                Interview.id == interview_id,
                Interview.organization_id == org_id
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_interviews_by_org(
        self, 
        org_id: uuid.UUID, 
        filters: dict = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Interview]:
        """Get interviews for organization with filters"""
        conditions = [Interview.organization_id == org_id]
        
        if filters:
            if filters.get("status"):
                conditions.append(Interview.status == filters["status"])
            if filters.get("job_id"):
                conditions.append(Interview.job_id == filters["job_id"])
            if filters.get("candidate_id"):
                conditions.append(Interview.candidate_id == filters["candidate_id"])
            if filters.get("date_from"):
                conditions.append(Interview.scheduled_start >= filters["date_from"])
            if filters.get("date_to"):
                conditions.append(Interview.scheduled_start <= filters["date_to"])
        
        query = select(Interview).where(
            and_(*conditions)
        ).offset(skip).limit(limit).order_by(Interview.scheduled_start.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_interview(
        self, 
        interview_id: uuid.UUID, 
        update_data: dict
    ) -> Optional[Interview]:
        """Update interview"""
        query = update(Interview).where(
            Interview.id == interview_id
        ).values(**update_data)
        await self.db.execute(query)
        await self.db.commit()
        
        # Get the interview for return
        query = select(Interview).where(Interview.id == interview_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_interview_status(
        self, 
        interview_id: uuid.UUID, 
        new_status: str
    ) -> Optional[Interview]:
        """Update interview status"""
        return await self.update_interview(
            interview_id, 
            {"status": new_status}
        )
    
    async def get_upcoming_interviews(
        self, 
        org_id: uuid.UUID, 
        hours: int = 24
    ) -> List[Interview]:
        """Get upcoming interviews within specified hours"""
        time_threshold = datetime.now() + timedelta(hours=hours)
        query = select(Interview).where(
            and_(
                Interview.organization_id == org_id,
                Interview.scheduled_start >= datetime.now(),
                Interview.scheduled_start <= time_threshold,
                Interview.status.in_([
                    InterviewStatus.SCHEDULED, 
                    InterviewStatus.CONFIRMED
                ])
            )
        ).order_by(Interview.scheduled_start)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def _add_timeline_event(
        self, 
        interview_id: uuid.UUID, 
        event_name: str
    ) -> None:
        """Add timeline event for interview"""
        event = InterviewTimeline(
            interview_id=interview_id,
            event_name=event_name
        )
        self.db.add(event)
    
    async def add_audit_log(
        self, 
        interview_id: uuid.UUID, 
        action: str, 
        user_id: uuid.UUID
    ) -> None:
        """Add audit log entry"""
        log = InterviewAuditLog(
            interview_id=interview_id,
            action=action,
            action_by=user_id
        )
        self.db.add(log)


class PanelRepository:
    """Repository for interview panel operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_panel(
        self, 
        interview_id: uuid.UUID, 
        panel_data: dict
    ) -> InterviewPanel:
        """Create interview panel"""
        panel = InterviewPanel(
            interview_id=interview_id,
            panel_name=panel_data["panel_name"]
        )
        self.db.add(panel)
        await self.db.flush()
        
        # Add panel members
        for member_data in panel_data["members"]:
            member = InterviewPanelMember(
                panel_id=panel.id,
                user_id=member_data["user_id"],
                role=member_data["role"],
                is_primary=member_data["is_primary"]
            )
            self.db.add(member)
        
        await self.db.commit()
        return panel
    
    async def get_panel_by_interview(
        self, 
        interview_id: uuid.UUID
    ) -> Optional[InterviewPanel]:
        """Get panel for interview"""
        query = select(InterviewPanel).where(
            InterviewPanel.interview_id == interview_id
        ).options(selectinload(InterviewPanel.members))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def add_panel_member(
        self, 
        panel_id: uuid.UUID, 
        member_data: dict
    ) -> InterviewPanelMember:
        """Add member to panel"""
        member = InterviewPanelMember(
            panel_id=panel_id,
            user_id=member_data["user_id"],
            role=member_data["role"],
            is_primary=member_data["is_primary"]
        )
        self.db.add(member)
        await self.db.commit()
        return member
    
    async def update_member_feedback_status(
        self, 
        member_id: uuid.UUID, 
        status: str
    ) -> None:
        """Update panel member feedback status"""
        query = update(InterviewPanelMember).where(
            InterviewPanelMember.id == member_id
        ).values(
            feedback_status=status,
            feedback_submitted_at=datetime.now() if status == FeedbackStatus.SUBMITTED else None
        )
        await self.db.execute(query)
        await self.db.commit()
    
    async def remove_panel_member(
        self, 
        member_id: uuid.UUID
    ) -> bool:
        """Remove panel member"""
        query = delete(InterviewPanelMember).where(
            InterviewPanelMember.id == member_id
        )
        await self.db.execute(query)
        await self.db.commit()
        return True


class FeedbackRepository:
    """Repository for interview feedback operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_feedback(
        self, 
        feedback_data: dict
    ) -> InterviewFeedback:
        """Create interview feedback"""
        feedback = InterviewFeedback(
            interview_id=feedback_data["interview_id"],
            interviewer_id=feedback_data["interviewer_id"],
            panel_member_id=feedback_data.get("panel_member_id"),
            overall_rating=feedback_data.get("overall_rating"),
            recommendation=feedback_data.get("recommendation"),
            strengths=feedback_data.get("strengths"),
            weaknesses=feedback_data.get("weaknesses"),
            detailed_comments=feedback_data.get("detailed_comments"),
            status=FeedbackStatus.SUBMITTED,
            submitted_at=datetime.now(),
            is_complete=True
        )
        self.db.add(feedback)
        await self.db.flush()
        
        # Add criterion scores
        for score_data in feedback_data["criterion_scores"]:
            criterion_score = FeedbackCriterionScore(
                feedback_id=feedback.id,
                criterion_id=score_data["criterion_id"],
                score=score_data["score"],
                max_score=score_data.get("max_score", 10.0),
                weight=score_data.get("weight", 1.0),
                comments=score_data.get("comments"),
                evidence=score_data.get("evidence"),
                is_required=score_data.get("is_required", True),
                passes_threshold=score_data.get("passes_threshold", True)
            )
            self.db.add(criterion_score)
        
        await self.db.commit()
        return feedback
    
    async def get_feedback_by_interview(
        self, 
        interview_id: uuid.UUID
    ) -> List[InterviewFeedback]:
        """Get all feedback for an interview"""
        query = select(InterviewFeedback).where(
            InterviewFeedback.interview_id == interview_id
        ).options(selectinload(InterviewFeedback.criterion_scores))
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_feedback_by_interviewer(
        self, 
        interview_id: uuid.UUID, 
        interviewer_id: uuid.UUID
    ) -> Optional[InterviewFeedback]:
        """Get feedback by interviewer for an interview"""
        query = select(InterviewFeedback).where(
            and_(
                InterviewFeedback.interview_id == interview_id,
                InterviewFeedback.interviewer_id == interviewer_id
            )
        ).options(selectinload(InterviewFeedback.criterion_scores))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_feedback(
        self, 
        feedback_id: uuid.UUID, 
        update_data: dict
    ) -> Optional[InterviewFeedback]:
        """Update feedback"""
        query = update(InterviewFeedback).where(
            InterviewFeedback.id == feedback_id
        ).values(**update_data)
        await self.db.execute(query)
        await self.db.commit()
        
        query = select(InterviewFeedback).where(
            InterviewFeedback.id == feedback_id
        ).options(selectinload(InterviewFeedback.criterion_scores))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def lock_feedback(self, feedback_id: uuid.UUID) -> bool:
        """Lock feedback to prevent further modifications"""
        query = update(InterviewFeedback).where(
            InterviewFeedback.id == feedback_id
        ).values(status=FeedbackStatus.LOCKED)
        await self.db.execute(query)
        await self.db.commit()
        return True


class ScorecardRepository:
    """Repository for scorecard operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_scorecard(
        self, 
        scorecard_data: dict
    ) -> InterviewScorecard:
        """Create interview scorecard"""
        scorecard = InterviewScorecard(
            interview_id=scorecard_data["interview_id"],
            template_round_id=scorecard_data["template_round_id"],
            overall_score=scorecard_data["overall_score"],
            max_possible_score=scorecard_data["max_possible_score"],
            percentage_score=scorecard_data["percentage_score"],
            recommendation=scorecard_data["recommendation"],
            recommendation_confidence=scorecard_data.get("recommendation_confidence", 0.0),
            summary=scorecard_data.get("summary"),
            calculated_at=datetime.now(),
            is_final=scorecard_data.get("is_final", False),
            required_feedback_count=scorecard_data["required_feedback_count"],
            received_feedback_count=scorecard_data["received_feedback_count"]
        )
        self.db.add(scorecard)
        await self.db.commit()
        return scorecard
    
    async def get_scorecard_by_interview(
        self, 
        interview_id: uuid.UUID
    ) -> Optional[InterviewScorecard]:
        """Get scorecard for interview"""
        query = select(InterviewScorecard).where(
            InterviewScorecard.interview_id == interview_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_scorecard(
        self, 
        scorecard_id: uuid.UUID, 
        update_data: dict
    ) -> Optional[InterviewScorecard]:
        """Update scorecard"""
        query = update(InterviewScorecard).where(
            InterviewScorecard.id == scorecard_id
        ).values(**update_data)
        await self.db.execute(query)
        await self.db.commit()
        
        query = select(InterviewScorecard).where(
            InterviewScorecard.id == scorecard_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


class DecisionRepository:
    """Repository for interview decision operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_decision(
        self, 
        decision_data: dict
    ) -> InterviewDecision:
        """Create interview decision"""
        decision = InterviewDecision(
            interview_id=decision_data["interview_id"],
            decision=decision_data["decision"],
            decision_maker_id=decision_data["decision_maker_id"],
            decision_maker_role=decision_data["decision_maker_role"],
            justification=decision_data.get("justification"),
            ai_recommendation=decision_data.get("ai_recommendation"),
            ai_confidence=decision_data.get("ai_confidence"),
            ai_evidence=decision_data.get("ai_evidence"),
            overrides_ai=decision_data.get("overrides_ai", False),
            next_step=decision_data.get("next_step")
        )
        self.db.add(decision)
        await self.db.commit()
        return decision
    
    async def get_decision_by_interview(
        self, 
        interview_id: uuid.UUID
    ) -> Optional[InterviewDecision]:
        """Get decision for interview"""
        query = select(InterviewDecision).where(
            InterviewDecision.interview_id == interview_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


class AssessmentRepository:
    """Repository for assessment operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_assessment_template(
        self, 
        org_id: uuid.UUID, 
        template_data: dict
    ) -> AssessmentTemplate:
        """Create assessment template"""
        template = AssessmentTemplate(
            organization_id=org_id,
            assessment_type_id=template_data["assessment_type_id"],
            template_name=template_data["template_name"],
            description=template_data.get("description"),
            duration_minutes=template_data["duration_minutes"],
            passing_score=template_data["passing_score"],
            max_attempts=template_data["max_attempts"],
            instructions=template_data.get("instructions"),
            configuration=template_data.get("configuration")
        )
        self.db.add(template)
        await self.db.flush()
        
        # Add questions
        for question_data in template_data["questions"]:
            question = AssessmentQuestion(
                template_id=template.id,
                question_text=question_data["question_text"],
                question_type=question_data["question_type"],
                options=question_data.get("options"),
                correct_answer=question_data.get("correct_answer"),
                points=question_data["points"],
                sequence_order=question_data["sequence_order"],
                explanation=question_data.get("explanation"),
                is_required=question_data["is_required"]
            )
            self.db.add(question)
        
        await self.db.commit()
        return template
    
    async def create_assessment(
        self, 
        assessment_data: dict
    ) -> Assessment:
        """Create assessment"""
        assessment = Assessment(
            organization_id=assessment_data["organization_id"],
            job_id=assessment_data["job_id"],
            assessment_template_id=assessment_data["assessment_template_id"],
            assessment_name=assessment_data["assessment_name"],
            description=assessment_data.get("description"),
            interview_round_id=assessment_data.get("interview_round_id"),
            duration_minutes=assessment_data["duration_minutes"],
            due_date=assessment_data.get("due_date")
        )
        self.db.add(assessment)
        await self.db.commit()
        return assessment
    
    async def get_assessments_by_org(
        self, 
        org_id: uuid.UUID, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Assessment]:
        """Get assessments for organization"""
        query = select(Assessment).where(
            Assessment.organization_id == org_id
        ).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def create_assessment_attempt(
        self, 
        attempt_data: dict
    ) -> AssessmentAttempt:
        """Create assessment attempt"""
        attempt = AssessmentAttempt(
            assessment_id=attempt_data["assessment_id"],
            candidate_id=attempt_data["candidate_id"],
            attempt_number=attempt_data["attempt_number"],
            started_at=datetime.now(),
            status="InProgress"
        )
        self.db.add(attempt)
        await self.db.commit()
        return attempt
    
    async def submit_assessment_answer(
        self, 
        answer_data: dict
    ) -> AssessmentAnswer:
        """Submit assessment answer"""
        answer = AssessmentAnswer(
            attempt_id=answer_data["attempt_id"],
            question_id=answer_data["question_id"],
            answer_text=answer_data["answer_text"],
            time_spent_seconds=answer_data.get("time_spent_seconds"),
            answered_at=datetime.now()
        )
        self.db.add(answer)
        await self.db.commit()
        return answer
    
    async def complete_assessment_attempt(
        self, 
        attempt_id: uuid.UUID, 
        score_data: dict
    ) -> AssessmentAttempt:
        """Complete assessment attempt"""
        query = update(AssessmentAttempt).where(
            AssessmentAttempt.id == attempt_id
        ).values(
            submitted_at=datetime.now(),
            score=score_data["score"],
            percentage_score=score_data["percentage_score"],
            status="Evaluated"
        )
        await self.db.execute(query)
        await self.db.commit()
        
        query = select(AssessmentAttempt).where(
            AssessmentAttempt.id == attempt_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


class EvaluationCriterionRepository:
    """Repository for evaluation criteria operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_criterion(
        self, 
        org_id: uuid.UUID, 
        criterion_data: dict
    ) -> EvaluationCriterion:
        """Create evaluation criterion"""
        criterion = EvaluationCriterion(
            organization_id=org_id,
            criterion_name=criterion_data["criterion_name"],
            description=criterion_data.get("description"),
            category=criterion_data.get("category"),
            evaluation_type=criterion_data["evaluation_type"],
            default_weight=criterion_data["default_weight"],
            default_max_score=criterion_data["default_max_score"]
        )
        self.db.add(criterion)
        await self.db.commit()
        return criterion
    
    async def get_criteria_by_org(
        self, 
        org_id: uuid.UUID, 
        category: Optional[str] = None
    ) -> List[EvaluationCriterion]:
        """Get evaluation criteria for organization"""
        conditions = [EvaluationCriterion.organization_id == org_id]
        if category:
            conditions.append(EvaluationCriterion.category == category)
        
        query = select(EvaluationCriterion).where(
            and_(*conditions)
        ).where(EvaluationCriterion.is_active == True)
        
        result = await self.db.execute(query)
        return result.scalars().all()


class AIAnalysisRepository:
    """Repository for AI analysis operations (for future LangGraph integration)"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_analysis(
        self, 
        analysis_data: dict
    ) -> AiInterviewAnalysis:
        """Create AI analysis"""
        analysis = AiInterviewAnalysis(
            interview_id=analysis_data["interview_id"],
            analysis_type=analysis_data["analysis_type"],
            analysis_text=analysis_data["analysis_text"],
            confidence_score=analysis_data["confidence_score"],
            model_version=analysis_data.get("model_version"),
            generated_at=datetime.now()
        )
        self.db.add(analysis)
        await self.db.commit()
        return analysis
    
    async def get_analysis_by_interview(
        self, 
        interview_id: uuid.UUID
    ) -> List[AiInterviewAnalysis]:
        """Get all AI analyses for interview"""
        query = select(AiInterviewAnalysis).where(
            AiInterviewAnalysis.interview_id == interview_id
        )
        result = await self.db.execute(query)
        return result.scalars().all()