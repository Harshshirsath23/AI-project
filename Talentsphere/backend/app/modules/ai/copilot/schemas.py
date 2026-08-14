from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime

class CopilotChatRequest(BaseModel):
    message: str = Field(..., description="Recruiter query or command")
    conversation_id: Optional[str] = Field(None, description="Existing conversation UUID")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Active view context (e.g. selected job, active candidate)")

class CopilotChatResponse(BaseModel):
    conversation_id: str
    execution_id: str
    type: str = Field(..., description="Response payload type (TEXT, CANDIDATE_LIST, CANDIDATE_COMPARISON, JOB_SUMMARY, PIPELINE_SUMMARY, INTERVIEW_SUMMARY, RECOMMENDATION, ACTION_CONFIRMATION, HITL_REQUEST, ERROR)")
    message: str
    data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    reasoning_summary: Optional[str] = None
    confidence: float = 0.95
    evidence: List[str] = Field(default_factory=list)
    gaps: List[str] = Field(default_factory=list)
    hitl_required: bool = False
    hitl_request_id: Optional[str] = None
    trace_id: Optional[str] = None

class CopilotMessageResponse(BaseModel):
    id: str
    conversation_id: str
    sender_type: str = Field(..., description="user or assistant")
    message: str
    response_type: Optional[str] = "TEXT"
    data_payload: Optional[Dict[str, Any]] = None
    reasoning_summary: Optional[str] = None
    hitl_required: bool = False
    created_at: datetime

class CopilotConversationResponse(BaseModel):
    id: str
    title: str
    organization_id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    messages: List[CopilotMessageResponse] = Field(default_factory=list)

class CopilotResumeRequest(BaseModel):
    decision: str = Field(..., description="Approved or Rejected")
    decision_reason: Optional[str] = None

class CopilotExecutionEvent(BaseModel):
    event_id: str
    execution_id: str
    step_name: str
    agent_name: str
    status: str
    timestamp: str
    details: Dict[str, Any] = Field(default_factory=dict)
