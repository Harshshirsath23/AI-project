from datetime import datetime
from typing import Optional, Any, Dict, List
from pydantic import BaseModel, Field


# Session Schemas

class ConversationSessionCreate(BaseModel):
    """Schema for creating a new conversation session."""

    organization_id: str = Field(..., description="Organization ID")
    campaign_id: Optional[str] = Field(None, description="Campaign ID")
    agent_id: Optional[str] = Field(None, description="Agent ID")
    lead_id: Optional[str] = Field(None, description="Lead ID")
    personality_id: Optional[str] = Field(None, description="Personality ID")
    script_id: Optional[str] = Field(None, description="Script ID")
    call_id: Optional[str] = Field(None, description="Telephony call ID")
    phone_number: Optional[str] = Field(None, description="Customer phone number")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ConversationSessionUpdate(BaseModel):
    """Schema for updating a conversation session."""

    current_state: Optional[str] = Field(None, description="Current state")
    status: Optional[str] = Field(None, description="Session status")
    end_time: Optional[datetime] = Field(None, description="Session end time")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ConversationSessionResponse(BaseModel):
    """Schema for conversation session response."""

    id: str
    session_id: str
    organization_id: str
    campaign_id: Optional[str]
    agent_id: Optional[str]
    lead_id: Optional[str]
    current_state: str
    previous_state: Optional[str]
    start_time: datetime
    last_activity: datetime
    end_time: Optional[datetime]
    status: str
    metadata: Optional[Dict[str, Any]]
    total_turns: int
    total_duration: float
    agent_speak_duration: float
    customer_speak_duration: float
    personality_id: Optional[str]
    script_id: Optional[str]
    call_id: Optional[str]
    phone_number: Optional[str]
    created_at: datetime
    updated_at: datetime


# Turn Schemas

class ConversationTurnCreate(BaseModel):
    """Schema for creating a conversation turn."""

    session_id: str = Field(..., description="Session ID")
    turn_number: int = Field(..., description="Turn number")
    turn_type: str = Field(..., description="Turn type")
    content: Optional[str] = Field(None, description="Turn content")
    content_type: Optional[str] = Field(None, description="Content type")
    state: str = Field(..., description="State at this turn")
    tool_name: Optional[str] = Field(None, description="Tool name if applicable")
    tool_result: Optional[Dict[str, Any]] = Field(None, description="Tool result")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ConversationTurnResponse(BaseModel):
    """Schema for conversation turn response."""

    id: str
    session_id: str
    turn_number: int
    turn_type: str
    content: Optional[str]
    content_type: Optional[str]
    start_time: datetime
    end_time: Optional[datetime]
    duration: float
    state: str
    tool_name: Optional[str]
    tool_result: Optional[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime


# Context Schemas

class ConversationContextUpdate(BaseModel):
    """Schema for updating conversation context."""

    variables: Optional[Dict[str, Any]] = Field(None, description="Session variables")
    customer_info: Optional[Dict[str, Any]] = Field(None, description="Customer information")
    agent_info: Optional[Dict[str, Any]] = Field(None, description="Agent information")
    campaign_info: Optional[Dict[str, Any]] = Field(None, description="Campaign information")
    rag_context: Optional[Dict[str, Any]] = Field(None, description="RAG context")
    nlp_context: Optional[Dict[str, Any]] = Field(None, description="NLP context")
    tool_outputs: Optional[Dict[str, Any]] = Field(None, description="Tool outputs")


class ConversationContextResponse(BaseModel):
    """Schema for conversation context response."""

    id: str
    session_id: str
    variables: Dict[str, Any]
    customer_info: Optional[Dict[str, Any]]
    agent_info: Optional[Dict[str, Any]]
    campaign_info: Optional[Dict[str, Any]]
    rag_context: Optional[Dict[str, Any]]
    nlp_context: Optional[Dict[str, Any]]
    tool_outputs: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


# State Transition Schemas

class StateTransitionCreate(BaseModel):
    """Schema for creating a state transition."""

    session_id: str = Field(..., description="Session ID")
    from_state: Optional[str] = Field(None, description="Previous state")
    to_state: str = Field(..., description="New state")
    reason: Optional[str] = Field(None, description="Reason for transition")
    trigger: Optional[str] = Field(None, description="Transition trigger")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class StateTransitionResponse(BaseModel):
    """Schema for state transition response."""

    id: str
    session_id: str
    from_state: Optional[str]
    to_state: str
    reason: Optional[str]
    trigger: Optional[str]
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime


# Tool Execution Schemas

class ToolExecutionCreate(BaseModel):
    """Schema for creating a tool execution record."""

    session_id: str = Field(..., description="Session ID")
    turn_id: Optional[str] = Field(None, description="Turn ID")
    tool_name: str = Field(..., description="Tool name")
    tool_type: str = Field(..., description="Tool type")
    parameters: Dict[str, Any] = Field(..., description="Tool parameters")
    max_retries: int = Field(default=3, description="Maximum retry attempts")


class ToolExecutionResponse(BaseModel):
    """Schema for tool execution response."""

    id: str
    session_id: str
    turn_id: Optional[str]
    tool_name: str
    tool_type: str
    parameters: Dict[str, Any]
    result: Optional[Dict[str, Any]]
    status: str
    start_time: datetime
    end_time: Optional[datetime]
    duration: float
    error_message: Optional[str]
    error_code: Optional[str]
    retry_count: int
    max_retries: int
    created_at: datetime
    updated_at: datetime


# Memory Schemas

class ConversationMemoryUpdate(BaseModel):
    """Schema for updating conversation memory."""

    preferences: Optional[Dict[str, Any]] = Field(None, description="Customer preferences")
    last_conversation_summary: Optional[str] = Field(None, description="Last conversation summary")
    key_topics: Optional[List[str]] = Field(None, description="Key topics discussed")
    sentiment_history: Optional[List[Dict[str, Any]]] = Field(None, description="Sentiment history")


class ConversationMemoryResponse(BaseModel):
    """Schema for conversation memory response."""

    id: str
    organization_id: str
    lead_id: str
    preferences: Dict[str, Any]
    last_conversation_summary: Optional[str]
    conversation_count: int
    key_topics: List[str]
    sentiment_history: List[Dict[str, Any]]
    last_conversation_date: Optional[datetime]
    last_agent_id: Optional[str]
    created_at: datetime
    updated_at: datetime


# State Machine Schemas

class StateDefinition(BaseModel):
    """Schema for defining a state in the state machine."""

    name: str = Field(..., description="State name")
    description: Optional[str] = Field(None, description="State description")
    allowed_transitions: List[str] = Field(default_factory=list, description="Allowed transition states")
    entry_actions: List[str] = Field(default_factory=list, description="Actions on state entry")
    exit_actions: List[str] = Field(default_factory=list, description="Actions on state exit")
    timeout: Optional[float] = Field(None, description="State timeout in seconds")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class StateTransitionRule(BaseModel):
    """Schema for defining a state transition rule."""

    from_state: str = Field(..., description="Source state")
    to_state: str = Field(..., description="Target state")
    trigger: str = Field(..., description="Transition trigger")
    condition: Optional[str] = Field(None, description="Transition condition")
    priority: int = Field(default=0, description="Transition priority")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


# Tool Schemas

class ToolDefinition(BaseModel):
    """Schema for defining a tool."""

    name: str = Field(..., description="Tool name")
    type: str = Field(..., description="Tool type")
    description: str = Field(..., description="Tool description")
    parameters_schema: Dict[str, Any] = Field(..., description="Parameters schema")
    timeout: float = Field(default=30.0, description="Tool timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    enabled: bool = Field(default=True, description="Whether tool is enabled")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ToolRequest(BaseModel):
    """Schema for a tool request."""

    tool_name: str = Field(..., description="Tool name")
    parameters: Dict[str, Any] = Field(..., description="Tool parameters")
    session_id: str = Field(..., description="Session ID")
    turn_id: Optional[str] = Field(None, description="Turn ID")


class ToolResponse(BaseModel):
    """Schema for a tool response."""

    success: bool = Field(..., description="Whether tool execution succeeded")
    result: Optional[Dict[str, Any]] = Field(None, description="Tool result")
    error: Optional[str] = Field(None, description="Error message if failed")
    execution_time: float = Field(..., description="Execution time in seconds")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


# Event Schemas

class ConversationEvent(BaseModel):
    """Schema for a conversation event."""

    event_type: str = Field(..., description="Event type")
    session_id: str = Field(..., description="Session ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Event timestamp")
    data: Optional[Dict[str, Any]] = Field(None, description="Event data")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


# Personality Schemas

class PersonalityDefinition(BaseModel):
    """Schema for defining an agent personality."""

    id: str = Field(..., description="Personality ID")
    name: str = Field(..., description="Personality name")
    description: str = Field(..., description="Personality description")
    traits: Dict[str, Any] = Field(..., description="Personality traits")
    system_prompt_template: Optional[str] = Field(None, description="System prompt template")
    response_style: str = Field(default="professional", description="Response style")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


# Script Schemas

class ScriptStepDefinition(BaseModel):
    """Schema for defining a script step."""

    step_id: str = Field(..., description="Step ID")
    name: str = Field(..., description="Step name")
    description: Optional[str] = Field(None, description="Step description")
    required_state: Optional[str] = Field(None, description="Required state")
    actions: List[str] = Field(default_factory=list, description="Actions to perform")
    next_steps: List[str] = Field(default_factory=list, description="Possible next steps")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ScriptProgress(BaseModel):
    """Schema for script progress tracking."""

    script_id: str = Field(..., description="Script ID")
    completed_steps: List[str] = Field(default_factory=list, description="Completed step IDs")
    current_step: Optional[str] = Field(None, description="Current step ID")
    skipped_steps: List[str] = Field(default_factory=list, description="Skipped step IDs")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
