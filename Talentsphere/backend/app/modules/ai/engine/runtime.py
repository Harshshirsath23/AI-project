import uuid
import time
import structlog
from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ai.models import AIAgent, AIExecution, ExecutionStatus
from app.modules.ai.schemas import AIExecutionCreate, HITLResponse
from app.modules.ai.repository import AgentRepository, ExecutionRepository, HITLRepository
from app.modules.ai.exceptions import AgentNotFoundException, ExecutionNotFoundException
from app.modules.ai.engine.state import (
    AgentExecutionStateDict, create_initial_agent_state, AgentExecutionStateModel
)
from app.modules.ai.engine.tools import ToolExecutionFramework
from app.modules.ai.engine.hitl import HITLGateManager
from app.core.observability import (
    update_trace_context, trace_agent, trace_workflow, get_current_trace_context
)

logger = structlog.get_logger(__name__)


class AgentRuntime:
    """
    Central Agent Runtime Gateway responsible for:
    - Agent & version resolution
    - Tool authorization checks
    - LangGraph execution & state management
    - Error handling, retries, fallbacks
    - HITL gate pause/resume management
    - Database state persistence
    - Non-blocking LangSmith telemetry emission
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.agent_repo = AgentRepository(db)
        self.exec_repo = ExecutionRepository(db)
        self.hitl_repo = HITLRepository(db)
        self.tool_framework = ToolExecutionFramework(db)
        self.hitl_manager = HITLGateManager(db)

    async def execute(
        self,
        organization_id: uuid.UUID,
        user_id: uuid.UUID,
        agent_id: uuid.UUID,
        input_data: Dict[str, Any],
        workflow_id: Optional[uuid.UUID] = None,
        user_permissions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Primary execution entrypoint for registered agents.
        """
        # 1. Resolve agent and version
        agent = await self.agent_repo.get_agent_by_id(agent_id)
        if not agent:
            raise AgentNotFoundException(str(agent_id))

        agent_version = agent.current_version
        model_name = agent.model_name
        model_provider = agent.model_provider

        # 2. Initialize execution context and state
        ctx = update_trace_context(
            organization_id=organization_id,
            user_id=user_id,
            agent_id=agent_id,
            agent_version=agent_version,
            workflow_id=workflow_id
        )

        # 3. Create PostgreSQL AIExecution database record
        exec_create = AIExecutionCreate(
            agent_id=agent_id,
            workflow_id=workflow_id,
            input_data=input_data
        )
        
        exec_dict = {
            "organization_id": organization_id,
            "agent_id": agent_id,
            "agent_version": agent_version,
            "workflow_id": workflow_id,
            "execution_id": str(uuid.uuid4()),
            "status": ExecutionStatus.RUNNING,
            "input_data": input_data,
            "model_provider": model_provider,
            "model_name": model_name,
            "langsmith_trace_id": ctx.trace_id,
            "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        db_execution = await self.exec_repo.create_execution(exec_dict)
        execution_id = db_execution.id
        update_trace_context(execution_id=execution_id)

        initial_state = create_initial_agent_state(
            organization_id=organization_id,
            user_id=user_id,
            agent_id=agent_id,
            agent_version=agent_version,
            workflow_id=workflow_id,
            request_data=input_data,
            execution_id=execution_id
        )

        start_time = time.time()

        # 4. Instrument agent execution trace
        async with trace_agent(
            agent_name=agent.agent_name,
            agent_id=str(agent_id),
            agent_version=agent_version,
            inputs=input_data
        ) as span:
            try:
                if input_data.get("workflow_type") == "sourcing" or ("job_id" in input_data and "candidate_id" not in input_data):
                    from app.modules.ai.workflows.sourcing_workflow import IntelligentSourcingWorkflow
                    workflow = IntelligentSourcingWorkflow(self.db)
                else:
                    from app.modules.ai.workflows.candidate_screening import CandidateScreeningWorkflow
                    workflow = CandidateScreeningWorkflow(self.db)
                
                final_state = await workflow.run(
                    state=initial_state,
                    org_id=organization_id,
                    user_id=user_id,
                    user_permissions=user_permissions or []
                )

                latency_ms = int((time.time() - start_time) * 1000)
                status = final_state.get("status", "COMPLETED")

                if status == ExecutionStatus.WAITING_HITL:
                    span.end(outputs={"status": "WAITING_HITL", "hitl_request": final_state.get("hitl_request")})
                    return {
                        "status": "WAITING_HITL",
                        "execution_id": str(execution_id),
                        "langsmith_trace_id": ctx.trace_id,
                        "hitl_request": final_state.get("hitl_request"),
                        "message": "Workflow paused awaiting recruiter decision."
                    }

                # Complete execution
                output_data = final_state.get("final_output", {})
                await self.exec_repo.update_execution_status(
                    execution_id=execution_id,
                    new_status=ExecutionStatus.COMPLETED,
                    output_data=output_data,
                    langsmith_trace_id=ctx.trace_id
                )

                span.end(outputs=output_data, extra_metadata={"latency_ms": latency_ms})

                return {
                    "status": "COMPLETED",
                    "execution_id": str(execution_id),
                    "langsmith_trace_id": ctx.trace_id,
                    "output_data": output_data,
                    "latency_ms": latency_ms
                }

            except Exception as exc:
                logger.error("Agent execution failed", execution_id=str(execution_id), error=str(exc))
                await self.exec_repo.update_execution_status(
                    execution_id=execution_id,
                    new_status=ExecutionStatus.FAILED,
                    error_message=str(exc),
                    langsmith_trace_id=ctx.trace_id
                )
                span.end(error=exc)
                raise

    async def resume(
        self,
        execution_id: uuid.UUID,
        hitl_response: HITLResponse,
        user_permissions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Resume workflow execution following human decision.
        """
        db_execution = await self.exec_repo.get_execution_by_id(execution_id)
        if not db_execution:
            raise ExecutionNotFoundException(str(execution_id))

        hitl_record = await self.hitl_repo.get_hitl_state_by_execution(execution_id)
        if not hitl_record:
            raise ExecutionNotFoundException(f"No active HITL state found for execution {execution_id}")

        # Update HITL decision
        await self.hitl_manager.record_human_decision(
            hitl_id=hitl_record.id,
            responded_by=uuid.uuid4(),
            decision=hitl_response.decision,
            decision_reason=hitl_response.decision_reason,
            modified_data=hitl_response.modified_data
        )

        if hitl_response.decision in ["Rejected", "REJECT"]:
            await self.exec_repo.update_execution_status(
                execution_id=execution_id,
                new_status=ExecutionStatus.FAILED,
                error_message="Recruiter rejected recommendation"
            )
            return {
                "status": "REJECTED",
                "execution_id": str(execution_id),
                "message": "Execution rejected by recruiter decision."
            }

        # Re-run workflow from checkpoint with human_decision attached
        initial_state = create_initial_agent_state(
            organization_id=db_execution.organization_id,
            user_id=uuid.uuid4(),
            agent_id=db_execution.agent_id,
            agent_version=db_execution.agent_version,
            workflow_id=db_execution.workflow_id,
            request_data=db_execution.input_data,
            execution_id=execution_id
        )
        initial_state["human_decision"] = {
            "decision": hitl_response.decision,
            "decision_reason": hitl_response.decision_reason,
            "modified_data": hitl_response.modified_data
        }

        from app.modules.ai.workflows.candidate_screening import CandidateScreeningWorkflow
        workflow = CandidateScreeningWorkflow(self.db)
        final_state = await workflow.run(
            state=initial_state,
            org_id=db_execution.organization_id,
            user_id=uuid.uuid4(),
            user_permissions=user_permissions or []
        )

        output_data = final_state.get("final_output", {})
        await self.exec_repo.update_execution_status(
            execution_id=execution_id,
            new_status=ExecutionStatus.COMPLETED,
            output_data=output_data
        )

        return {
            "status": "COMPLETED",
            "execution_id": str(execution_id),
            "output_data": output_data,
            "message": "Execution resumed and completed successfully."
        }
