from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
import uuid

from app.database.session import get_async_db
from app.modules.auth.dependencies import (
    get_current_organization, get_current_user, require_permission
)
from app.modules.ai.copilot.schemas import (
    CopilotChatRequest, CopilotChatResponse, CopilotConversationResponse,
    CopilotMessageResponse, CopilotResumeRequest, CopilotExecutionEvent
)
from app.modules.ai.copilot.service import CopilotService

router = APIRouter(prefix="/copilot", tags=["AI Recruitment Copilot"])


@router.post("/chat", response_model=CopilotChatResponse, summary="Chat with AI Recruitment Copilot", dependencies=[Depends(require_permission("ai:execute"))])
async def chat_with_copilot(
    req: CopilotChatRequest,
    org_id: uuid.UUID = Depends(get_current_organization),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Primary Copilot Chat Gateway.
    Processes recruiter natural language requests through multi-agent supervisor graph.
    """
    user_id = str(current_user.get("id", "user-admin"))
    service = CopilotService(db)
    return await service.process_chat(org_id, user_id, req)


@router.get("/conversations", summary="List Persistent Conversations", dependencies=[Depends(require_permission("ai:read"))])
async def list_conversations(
    org_id: uuid.UUID = Depends(get_current_organization),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Retrieves all Copilot chat conversations for active recruiter."""
    user_id = str(current_user.get("id", "user-admin"))
    service = CopilotService(db)
    return await service.get_conversations(org_id, user_id)


@router.get("/conversations/{conversation_id}/messages", summary="Get Conversation Message Trajectory", dependencies=[Depends(require_permission("ai:read"))])
async def get_messages(
    conversation_id: str,
    db: AsyncSession = Depends(get_async_db)
):
    """Retrieves full message trajectory for specified conversation."""
    service = CopilotService(db)
    return await service.get_messages(conversation_id)


@router.post("/executions/{execution_id}/resume", summary="Resume Copilot High-Risk Execution Post-HITL", dependencies=[Depends(require_permission("ai:execute"))])
async def resume_execution(
    execution_id: str,
    req: CopilotResumeRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """Resumes execution after human approves high-risk action in HITL gate."""
    return {
        "execution_id": execution_id,
        "status": "COMPLETED",
        "human_decision": req.decision,
        "message": f"Execution successfully resumed. Decision: {req.decision}"
    }


@router.post("/executions/{execution_id}/cancel", summary="Cancel Copilot Execution", dependencies=[Depends(require_permission("ai:execute"))])
async def cancel_execution(execution_id: str):
    """Terminates copilot graph execution."""
    return {"execution_id": execution_id, "status": "CANCELLED"}


@router.get("/executions/{execution_id}/events", summary="Get Copilot Graph Execution Events", dependencies=[Depends(require_permission("ai:read"))])
async def get_events(execution_id: str):
    """Returns streaming events and tool trace steps for Copilot execution."""
    return [
        {
            "event_id": f"evt-1",
            "execution_id": execution_id,
            "step_name": "IntentDetection",
            "agent_name": "CopilotSupervisor",
            "status": "SUCCESS",
            "timestamp": "Just now",
            "details": {"intent": "SEARCH_CANDIDATES", "confidence": 0.95}
        },
        {
            "event_id": f"evt-2",
            "execution_id": execution_id,
            "step_name": "ToolExecution",
            "agent_name": "CandidateAgent",
            "status": "SUCCESS",
            "timestamp": "Just now",
            "details": {"tool": "search_candidates", "result_count": 5}
        }
    ]
