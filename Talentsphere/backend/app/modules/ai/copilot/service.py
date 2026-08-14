import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ai.copilot.repository import CopilotRepository
from app.modules.ai.copilot.workflows.copilot_workflow import CopilotWorkflowRunner
from app.modules.ai.copilot.state import CopilotState
from app.modules.ai.copilot.schemas import CopilotChatRequest, CopilotChatResponse

class CopilotService:
    """
    High-level Copilot Service Gateway.
    Orchestrates persistence, workflow execution, Nemotron reasoning, and LangSmith tracing.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = CopilotRepository(db)

    async def process_chat(
        self,
        org_id: uuid.UUID,
        user_id: str,
        request_data: CopilotChatRequest
    ) -> CopilotChatResponse:
        # 1. Get or create conversation context
        conv = await self.repo.get_or_create_conversation(org_id, user_id, request_data.conversation_id)
        cid = conv["id"]
        exec_id = f"copilot-exec-{uuid.uuid4().hex[:10]}"

        # 2. Persist User Message
        await self.repo.add_message(
            conversation_id=cid,
            sender_type="user",
            message=request_data.message
        )

        # 3. Construct Initial LangGraph State
        history = await self.repo.get_messages(cid)
        initial_state: CopilotState = {
            "conversation_id": cid,
            "execution_id": exec_id,
            "organization_id": str(org_id),
            "user_id": user_id,
            "user_message": request_data.message,
            "conversation_history": history,
            "intent": "SEARCH_CANDIDATES",
            "intent_confidence": 0.95,
            "entities": request_data.context or {},
            "candidate_ids": [],
            "job_ids": [],
            "application_ids": [],
            "interview_ids": [],
            "reasoning": "",
            "tool_calls": [],
            "tool_results": [],
            "recommendations": [],
            "hitl_request": None,
            "human_decision": None,
            "final_response": {},
            "response_type": "TEXT",
            "errors": [],
            "metadata": {"langsmith_trace_id": f"tr-{uuid.uuid4().hex[:12]}"}
        }

        # 4. Run LangGraph Copilot Workflow
        runner = CopilotWorkflowRunner(self.db, org_id)
        final_state = await runner.run(initial_state)

        res_payload = final_state["final_response"]
        resp_type = final_state["response_type"]
        msg_content = res_payload.get("message", "Task completed.")

        # 5. Persist Assistant Response
        await self.repo.add_message(
            conversation_id=cid,
            sender_type="assistant",
            message=msg_content,
            response_type=resp_type,
            data_payload=res_payload.get("data"),
            reasoning_summary=res_payload.get("reasoning_summary"),
            hitl_required=res_payload.get("hitl_required", False)
        )

        # 6. Format API Response Payload
        return CopilotChatResponse(
            conversation_id=cid,
            execution_id=exec_id,
            type=resp_type,
            message=msg_content,
            data=res_payload.get("data", {}),
            reasoning_summary=res_payload.get("reasoning_summary"),
            confidence=res_payload.get("confidence", 0.95),
            evidence=res_payload.get("evidence", []),
            gaps=res_payload.get("gaps", []),
            hitl_required=res_payload.get("hitl_required", False),
            hitl_request_id=f"hitl-{exec_id}" if res_payload.get("hitl_required") else None,
            trace_id=final_state["metadata"].get("langsmith_trace_id")
        )

    async def get_conversations(self, org_id: uuid.UUID, user_id: str):
        return await self.repo.list_conversations(org_id, user_id)

    async def get_messages(self, conversation_id: str):
        return await self.repo.get_messages(conversation_id)
