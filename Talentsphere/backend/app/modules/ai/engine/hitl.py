import uuid
import structlog
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ai.repository import HITLRepository, ExecutionRepository
from app.modules.ai.enums import ExecutionStatus, HITLDecision
from app.modules.ai.schemas import HITLRequest, HITLResponse
from app.core.observability import trace_hitl, update_trace_context

logger = structlog.get_logger(__name__)


class HITLGateManager:
    """
    Human-In-The-Loop gate manager evaluating risk, pausing graphs,
    persisting HITL states, and handling recruiter decision resumes.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.hitl_repo = HITLRepository(db)
        self.exec_repo = ExecutionRepository(db)

    async def check_and_create_hitl_gate(
        self,
        execution_id: uuid.UUID,
        agent_id: uuid.UUID,
        requested_by: uuid.UUID,
        action_name: str,
        risk_level: str,
        request_data: Dict[str, Any],
        reason: str = "High risk automated recruitment action requires approval."
    ) -> Dict[str, Any]:
        """
        Pause workflow execution and persist HITLState record in database.
        """
        # Update AIExecution status
        await self.exec_repo.update_execution_status(
            execution_id,
            ExecutionStatus.WAITING_HITL
        )

        # Create HITLState database record
        hitl_dict = {
            "execution_id": execution_id,
            "agent_id": agent_id,
            "status": "Pending",
            "request_data": {
                "action_name": action_name,
                "risk_level": risk_level,
                "reason": reason,
                **request_data
            },
            "requested_by": requested_by,
            "requested_at": datetime.now(),
            "timeout_at": datetime.now() + timedelta(hours=24)
        }
        hitl_record = await self.hitl_repo.create_hitl_state(hitl_dict)

        update_trace_context(
            hitl_id=hitl_record.id,
            execution_id=execution_id,
            agent_id=agent_id
        )

        # Record HITL telemetry span
        async with trace_hitl(
            execution_id=str(execution_id),
            agent_id=str(agent_id),
            hitl_reason=reason,
            risk_level=risk_level
        ) as span:
            span.end(outputs={"status": "WAITING_HITL", "hitl_id": str(hitl_record.id)})

        logger.info(
            "HITL gate triggered, execution paused",
            execution_id=str(execution_id),
            hitl_id=str(hitl_record.id),
            action=action_name
        )

        return {
            "status": "WAITING_HITL",
            "hitl_id": str(hitl_record.id),
            "execution_id": str(execution_id),
            "reason": reason,
            "risk_level": risk_level,
            "requested_at": hitl_dict["requested_at"].isoformat()
        }

    async def record_human_decision(
        self,
        hitl_id: uuid.UUID,
        responded_by: uuid.UUID,
        decision: str | HITLDecision,
        decision_reason: Optional[str] = None,
        modified_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Record recruiter approval/rejection decision and resume workflow context.
        """
        decision_str = decision.value if isinstance(decision, HITLDecision) else str(decision)
        
        await self.hitl_repo.update_hitl_decision(
            hitl_id=hitl_id,
            decision=decision_str,
            reason=decision_reason,
            modified_data=modified_data
        )

        hitl_record = await self.hitl_repo.get_hitl_state_by_id(hitl_id)
        if hitl_record and hitl_record.execution_id:
            new_exec_status = ExecutionStatus.RUNNING if decision_str in ["Approved", "Modified"] else ExecutionStatus.FAILED
            await self.exec_repo.update_execution_status(hitl_record.execution_id, new_exec_status)

        update_trace_context(
            hitl_id=hitl_id,
            hitl_decision=decision_str
        )

        return {
            "status": "success",
            "hitl_id": str(hitl_id),
            "decision": decision_str,
            "decision_reason": decision_reason,
            "modified_data": modified_data
        }
