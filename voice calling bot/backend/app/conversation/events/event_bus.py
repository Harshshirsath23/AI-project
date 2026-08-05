from typing import Optional, Dict, Any, Callable, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import asyncio

from app.core.logging import get_logger

logger = get_logger(__name__)


class ConversationEventType(str, Enum):
    """Enumeration of conversation event types."""

    CONVERSATION_STARTED = "conversation_started"
    CONVERSATION_UPDATED = "conversation_updated"
    CONVERSATION_PAUSED = "conversation_paused"
    CONVERSATION_RESUMED = "conversation_resumed"
    CONVERSATION_ENDED = "conversation_ended"
    TOOL_REQUESTED = "tool_requested"
    TOOL_COMPLETED = "tool_completed"
    AGENT_RESPONSE_GENERATED = "agent_response_generated"
    CUSTOMER_RESPONSE_RECEIVED = "customer_response_received"
    STATE_TRANSITION = "state_transition"
    ERROR_OCCURRED = "error_occurred"


@dataclass
class ConversationEvent:
    """Conversation event data structure."""

    event_type: str
    session_id: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class EventBus:
    """
    Internal event bus for conversation events.
    
    This event bus provides a publish-subscribe mechanism for conversation events.
    Future modules can subscribe to these events to react to conversation
    lifecycle changes, tool executions, and other important events.
    
    Supported events:
    - Conversation Started
    - Conversation Updated
    - Conversation Paused
    - Conversation Resumed
    - Conversation Ended
    - Tool Requested
    - Tool Completed
    - Agent Response Generated
    - Customer Response Received
    - State Transition
    - Error Occurred
    """

    def __init__(self):
        """Initialize the event bus."""
        self._subscribers: Dict[str, List[Callable]] = {}
        self._event_history: List[ConversationEvent] = []
        self._max_history_size = 1000

    def subscribe(
        self,
        event_type: str,
        callback: Callable[[ConversationEvent], None],
    ) -> None:
        """
        Subscribe to an event type.
        
        Args:
            event_type: Event type to subscribe to
            callback: Callback function to invoke when event occurs
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        
        self._subscribers[event_type].append(callback)
        logger.debug("Event subscription added", event_type=event_type)

    def unsubscribe(
        self,
        event_type: str,
        callback: Callable[[ConversationEvent], None],
    ) -> bool:
        """
        Unsubscribe from an event type.
        
        Args:
            event_type: Event type to unsubscribe from
            callback: Callback function to remove
        
        Returns:
            True if callback was removed successfully
        """
        if event_type in self._subscribers:
            if callback in self._subscribers[event_type]:
                self._subscribers[event_type].remove(callback)
                logger.debug("Event subscription removed", event_type=event_type)
                return True
        return False

    async def publish(
        self,
        event: ConversationEvent,
    ) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event: Event to publish
        """
        # Add to history
        self._event_history.append(event)
        
        # Trim history if needed
        if len(self._event_history) > self._max_history_size:
            self._event_history = self._event_history[-self._max_history_size:]
        
        # Notify subscribers
        subscribers = self._subscribers.get(event.event_type, [])
        
        if subscribers:
            logger.debug(
                "Publishing event",
                event_type=event.event_type,
                session_id=event.session_id,
                subscriber_count=len(subscribers),
            )
            
            # Execute all subscribers asynchronously
            tasks = []
            for callback in subscribers:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        tasks.append(callback(event))
                    else:
                        callback(event)
                except Exception as e:
                    logger.error(
                        "Event callback failed",
                        event_type=event.event_type,
                        error=str(e),
                    )
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
        else:
            logger.debug(
                "No subscribers for event",
                event_type=event.event_type,
                session_id=event.session_id,
            )

    def get_event_history(
        self,
        session_id: Optional[str] = None,
        event_type: Optional[str] = None,
        limit: int = 100,
    ) -> List[ConversationEvent]:
        """
        Get event history.
        
        Args:
            session_id: Optional session ID to filter by
            event_type: Optional event type to filter by
            limit: Maximum number of events to return
        
        Returns:
            List of events
        """
        events = self._event_history
        
        if session_id:
            events = [e for e in events if e.session_id == session_id]
        
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        return events[-limit:] if events else []

    def clear_history(self) -> None:
        """Clear event history."""
        self._event_history.clear()
        logger.info("Event history cleared")

    def get_subscriber_count(self, event_type: str) -> int:
        """
        Get the number of subscribers for an event type.
        
        Args:
            event_type: Event type
        
        Returns:
            Number of subscribers
        """
        return len(self._subscribers.get(event_type, []))

    def list_event_types(self) -> List[str]:
        """
        List all event types with subscribers.
        
        Returns:
            List of event types
        """
        return list(self._subscribers.keys())


# Global event bus instance
_event_bus: Optional[EventBus] = None


def get_event_bus() -> EventBus:
    """
    Get the global event bus instance.
    
    Returns:
        EventBus: The global event bus
    """
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus


# Convenience functions for publishing common events

async def publish_conversation_started(
    session_id: str,
    data: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Publish a conversation started event.
    
    Args:
        session_id: Session ID
        data: Optional event data
    """
    event = ConversationEvent(
        event_type=ConversationEventType.CONVERSATION_STARTED,
        session_id=session_id,
        data=data,
    )
    await get_event_bus().publish(event)


async def publish_conversation_updated(
    session_id: str,
    data: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Publish a conversation updated event.
    
    Args:
        session_id: Session ID
        data: Optional event data
    """
    event = ConversationEvent(
        event_type=ConversationEventType.CONVERSATION_UPDATED,
        session_id=session_id,
        data=data,
    )
    await get_event_bus().publish(event)


async def publish_conversation_paused(
    session_id: str,
    data: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Publish a conversation paused event.
    
    Args:
        session_id: Session ID
        data: Optional event data
    """
    event = ConversationEvent(
        event_type=ConversationEventType.CONVERSATION_PAUSED,
        session_id=session_id,
        data=data,
    )
    await get_event_bus().publish(event)


async def publish_conversation_resumed(
    session_id: str,
    data: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Publish a conversation resumed event.
    
    Args:
        session_id: Session ID
        data: Optional event data
    """
    event = ConversationEvent(
        event_type=ConversationEventType.CONVERSATION_RESUMED,
        session_id=session_id,
        data=data,
    )
    await get_event_bus().publish(event)


async def publish_conversation_ended(
    session_id: str,
    data: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Publish a conversation ended event.
    
    Args:
        session_id: Session ID
        data: Optional event data
    """
    event = ConversationEvent(
        event_type=ConversationEventType.CONVERSATION_ENDED,
        session_id=session_id,
        data=data,
    )
    await get_event_bus().publish(event)


async def publish_tool_requested(
    session_id: str,
    tool_name: str,
    parameters: Dict[str, Any],
) -> None:
    """
    Publish a tool requested event.
    
    Args:
        session_id: Session ID
        tool_name: Tool name
        parameters: Tool parameters
    """
    event = ConversationEvent(
        event_type=ConversationEventType.TOOL_REQUESTED,
        session_id=session_id,
        data={
            "tool_name": tool_name,
            "parameters": parameters,
        },
    )
    await get_event_bus().publish(event)


async def publish_tool_completed(
    session_id: str,
    tool_name: str,
    success: bool,
    result: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None,
) -> None:
    """
    Publish a tool completed event.
    
    Args:
        session_id: Session ID
        tool_name: Tool name
        success: Whether tool execution succeeded
        result: Tool result
        error: Error message if failed
    """
    event = ConversationEvent(
        event_type=ConversationEventType.TOOL_COMPLETED,
        session_id=session_id,
        data={
            "tool_name": tool_name,
            "success": success,
            "result": result,
            "error": error,
        },
    )
    await get_event_bus().publish(event)


async def publish_agent_response_generated(
    session_id: str,
    response: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Publish an agent response generated event.
    
    Args:
        session_id: Session ID
        response: Generated response
        metadata: Optional metadata
    """
    event = ConversationEvent(
        event_type=ConversationEventType.AGENT_RESPONSE_GENERATED,
        session_id=session_id,
        data={
            "response": response,
            "metadata": metadata,
        },
    )
    await get_event_bus().publish(event)


async def publish_customer_response_received(
    session_id: str,
    response: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Publish a customer response received event.
    
    Args:
        session_id: Session ID
        response: Customer response
        metadata: Optional metadata
    """
    event = ConversationEvent(
        event_type=ConversationEventType.CUSTOMER_RESPONSE_RECEIVED,
        session_id=session_id,
        data={
            "response": response,
            "metadata": metadata,
        },
    )
    await get_event_bus().publish(event)


async def publish_state_transition(
    session_id: str,
    from_state: Optional[str],
    to_state: str,
    trigger: str,
) -> None:
    """
    Publish a state transition event.
    
    Args:
        session_id: Session ID
        from_state: Previous state
        to_state: New state
        trigger: Transition trigger
    """
    event = ConversationEvent(
        event_type=ConversationEventType.STATE_TRANSITION,
        session_id=session_id,
        data={
            "from_state": from_state,
            "to_state": to_state,
            "trigger": trigger,
        },
    )
    await get_event_bus().publish(event)


async def publish_error_occurred(
    session_id: str,
    error: str,
    error_type: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Publish an error occurred event.
    
    Args:
        session_id: Session ID
        error: Error message
        error_type: Error type
        metadata: Optional metadata
    """
    event = ConversationEvent(
        event_type=ConversationEventType.ERROR_OCCURRED,
        session_id=session_id,
        data={
            "error": error,
            "error_type": error_type,
            "metadata": metadata,
        },
    )
    await get_event_bus().publish(event)
