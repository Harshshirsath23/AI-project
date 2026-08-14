import uuid
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.modules.recruitment.repository import ApplicationRepository, PipelineRepository
from app.modules.recruitment.transition_engine import TransitionEngine
from app.modules.recruitment.rules_engine import WorkflowRulesEngine
from app.modules.recruitment.automation_hooks import AutomationHookDispatcher

class WorkflowEngine:
    """
    Main Workflow Orchestration Engine.
    Executes database-driven stage transitions, enforces workflow rules, and dispatches automation hooks.
    """
    def __init__(self, db: AsyncSession):
        self.db = db
        self.app_repo = ApplicationRepository(db)
        self.pipeline_repo = PipelineRepository(db)

    async def execute_stage_transition(
        self,
        application_id: uuid.UUID,
        to_stage_id: uuid.UUID,
        user_id: uuid.UUID,
        notes: Optional[str] = None,
        trigger_hook: bool = True
    ) -> Dict[str, Any]:
        # 1. Fetch application
        app = await self.app_repo.get_by_id(application_id)
        if not app:
            raise HTTPException(status_code=404, detail="Application not found")

        # 2. Fetch stages
        from_stage = None
        stages = await self.pipeline_repo.get_pipeline_stages(app.pipeline_id) if app.pipeline_id else []
        stage_map = {s.id: s for s in stages}

        if app.current_stage_id:
            from_stage = stage_map.get(app.current_stage_id)
        to_stage = stage_map.get(to_stage_id)

        if not to_stage:
            # Fallback if stage belongs to general stages
            stages = await self.pipeline_repo.get_stages(app.job.organization_id if hasattr(app, 'job') and app.job else uuid.uuid4())
            stage_map = {s.id: s for s in stages}
            to_stage = stage_map.get(to_stage_id)

        if not to_stage:
            raise HTTPException(status_code=400, detail="Target stage not found in pipeline")

        # 3. Validate Transition
        TransitionEngine.validate_transition(from_stage, to_stage, notes)

        # 4. Evaluate Workflow Rules
        rule_eval = WorkflowRulesEngine.evaluate_stage_rules(to_stage.stage_name)
        if not rule_eval["rules_passed"]:
            raise HTTPException(status_code=400, detail=f"Workflow Rule Violation: {rule_eval['reason']}")

        # 5. Execute DB Update
        updated_app = await self.app_repo.update_stage(
            application_id=app.id,
            from_stage_id=app.current_stage_id,
            to_stage_id=to_stage_id,
            status=to_stage.stage_name,
            user_id=user_id
        )

        # 6. Dispatch Automation Hooks for LangGraph AI
        hook_payload = None
        if trigger_hook:
            hook_payload = await AutomationHookDispatcher.dispatch_stage_hook(
                application_id=app.id,
                from_stage_id=app.current_stage_id,
                to_stage_id=to_stage_id,
                stage_name=to_stage.stage_name
            )

        return {
            "application_id": app.id,
            "from_stage_id": app.current_stage_id,
            "to_stage_id": to_stage_id,
            "application_status": to_stage.stage_name,
            "transitioned_at": updated_app.created_at,
            "automation_hook_status": hook_payload.get("status") if hook_payload else "HOOK_SKIPPED"
        }
