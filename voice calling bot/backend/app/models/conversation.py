from datetime import datetime
from typing import Optional

from sqlalchemy import Uuid, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import AuditMixin, BaseModel, SoftDeleteMixin


class ConversationSession(BaseModel, AuditMixin, SoftDeleteMixin):
    """
    Conversation session model for tracking active conversations.
    
    Each active call has an isolated conversation session with complete
    isolation from other sessions.
    """

    __tablename__ = "conversation_session"

    session_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    organization_id: Mapped[str] = mapped_column(Uuid, nullable=False, index=True)
    campaign_id: Mapped[Optional[str]] = mapped_column(Uuid, nullable=True, index=True)
    agent_id: Mapped[Optional[str]] = mapped_column(Uuid, nullable=True, index=True)
    lead_id: Mapped[Optional[str]] = mapped_column(Uuid, nullable=True, index=True)
    
    # State management
    current_state: Mapped[str] = mapped_column(String(50), nullable=False, default="initializing", index=True)
    previous_state: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Timing
    start_time: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    last_activity: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow, index=True)
    end_time: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)
    # Status values: active, paused, completed, failed, transferred, ended, archived
    
    # Metadata
    meta_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Performance metrics
    total_turns: Mapped[int] = mapped_column(default=0)
    total_duration: Mapped[float] = mapped_column(default=0.0)  # in seconds
    agent_speak_duration: Mapped[float] = mapped_column(default=0.0)
    customer_speak_duration: Mapped[float] = mapped_column(default=0.0)
    
    # Personality and script
    personality_id: Mapped[Optional[str]] = mapped_column(Uuid, nullable=True)
    script_id: Mapped[Optional[str]] = mapped_column(Uuid, nullable=True)
    
    # Telephony integration (future)
    call_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)


class ConversationTurn(BaseModel, AuditMixin):
    """
    Individual turn in a conversation.
    
    A turn represents one exchange between the customer and the agent.
    """

    __tablename__ = "conversation_turn"

    session_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    turn_number: Mapped[int] = mapped_column(nullable=False)
    
    # Turn type
    turn_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # Turn types: customer_input, agent_response, system_message, tool_request, tool_response
    
    # Content
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    # Content types: text, audio_url, structured_data
    
    # Timing
    start_time: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    end_time: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    duration: Mapped[float] = mapped_column(default=0.0)
    
    # State at this turn
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Tool execution (if applicable)
    tool_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    tool_result: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Metadata
    meta_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)


class ConversationContext(BaseModel, AuditMixin):
    """
    Conversation context for storing session variables and state.
    
    This model stores the context that persists throughout a conversation,
    including temporary variables, customer information, and other
    conversation-specific data.
    """

    __tablename__ = "conversation_context"

    session_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    
    # Context data
    variables: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    
    # Customer information
    customer_info: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Agent information
    agent_info: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Campaign information
    campaign_info: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # RAG context (future)
    rag_context: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # NLP context (future)
    nlp_context: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Tool outputs
    tool_outputs: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)


class ConversationStateTransition(BaseModel, AuditMixin):
    """
    Log of state transitions for a conversation.
    
    This provides an audit trail of all state changes during a conversation.
    """

    __tablename__ = "conversation_state_transition"

    session_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    
    # Transition details
    from_state: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    to_state: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Reason for transition
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Trigger
    trigger: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    # Trigger types: user_input, tool_result, timeout, error, manual, system
    
    # Metadata
    meta_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)


class ConversationToolExecution(BaseModel, AuditMixin):
    """
    Log of tool executions during aConversation.
    
    This tracks all tool invocations, their parameters, results,
    and execution time.
    """

    __tablename__ = "conversation_tool_execution"

    session_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    turn_id: Mapped[Optional[str]] = mapped_column(Uuid, nullable=True)
    
    # Tool details
    tool_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    tool_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # Tool types: crm, hrms, erp, calendar, email, whatsapp, rest_api, webhook, database, mcp, business_module
    
    # Parameters and result
    parameters: Mapped[dict] = mapped_column(JSON, nullable=False)
    result: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Execution details
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    # Status values: pending, executing, completed, failed, timeout
    
    start_time: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    end_time: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    duration: Mapped[float] = mapped_column(default=0.0)
    
    # Error handling
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Retry information
    retry_count: Mapped[int] = mapped_column(default=0)
    max_retries: Mapped[int] = mapped_column(default=3)


class ConversationMemory(BaseModel, AuditMixin):
    """
    Long-term conversation memory for customer preferences and summaries.
    
    This stores persistent information about customers that persists
    across conversations.
    """

    __tablename__ = "conversation_memory"

    organization_id: Mapped[str] = mapped_column(Uuid, nullable=False, index=True)
    lead_id: Mapped[str] = mapped_column(Uuid, nullable=False, index=True)
    
    # Memory data
    preferences: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    
    # Conversation summaries
    last_conversation_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    conversation_count: Mapped[int] = mapped_column(default=0)
    
    # Key insights
    key_topics: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    sentiment_history: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    
    # Last interaction
    last_conversation_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    last_agent_id: Mapped[Optional[str]] = mapped_column(Uuid, nullable=True)
