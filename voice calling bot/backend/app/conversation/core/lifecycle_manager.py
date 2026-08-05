from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import asyncio

from app.conversation.events.event_bus import (
    publish_conversation_started,
    publish_conversation_ended,
    publish_error_occurred,
)
from app.conversation.managers.session_manager import get_session_manager
from app.core.logging import get_logger

logger = get_logger(__name__)


class ConversationLifecycleState(str, Enum):
    """Enumeration of conversation lifecycle states."""

    STARTING = "starting"
    ACTIVE = "active"
    IDLE = "idle"
    TIMEOUT = "timeout"
    COMPLETE = "complete"
    ARCHIVED = "archived"


class LifecycleManager:
    """
    Manager for conversation lifecycle.
    
    This manager handles the complete lifecycle of a conversation:
    - Conversation Start
    - Conversation Active
    - Conversation Idle
    - Conversation Timeout
    - Conversation Complete
    - Conversation Archived
    
    The lifecycle manager coordinates with the session manager and event bus
    to ensure proper lifecycle transitions and cleanup.
    """

    def __init__(self):
        """Initialize the lifecycle manager."""
        self._session_lifecycle_states: Dict[str, ConversationLifecycleState] = {}
        self._idle_timers: Dict[str, asyncio.Task] = {}
        self._session_manager = get_session_manager()

    async def start_conversation(
        self,
        organization_id: str,
        campaign_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        lead_id: Optional[str] = None,
        personality_id: Optional[str] = None,
        script_id: Optional[str] = None,
        call_id: Optional[str] = None,
        phone_number: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Start a new conversation.
        
        Args:
            organization_id: Organization ID
            campaign_id: Optional campaign ID
            agent_id: Optional agent ID
            lead_id: Optional lead ID
            personality_id: Optional personality ID
            script_id: Optional script ID
            call_id: Optional telephony call ID
            phone_number: Optional customer phone number
            metadata: Additional metadata
        
        Returns:
            Session ID of the new conversation
        """
        # Create session
        session = await self._session_manager.create_session(
            organization_id=organization_id,
            campaign_id=campaign_id,
            agent_id=agent_id,
            lead_id=lead_id,
            personality_id=personality_id,
            script_id=script_id,
            call_id=call_id,
            phone_number=phone_number,
            metadata=metadata,
        )
        
        # Set lifecycle state
        self._session_lifecycle_states[session.session_id] = ConversationLifecycleState.STARTING
        
        # Publish event
        await publish_conversation_started(
            session_id=session.session_id,
            data={
                "organization_id": organization_id,
                "campaign_id": campaign_id,
                "agent_id": agent_id,
                "lead_id": lead_id,
            },
        )
        
        # Transition to active
        await self.transition_to_active(session.session_id)
        
        logger.info(
            "Conversation started",
            session_id=session.session_id,
            organization_id=organization_id,
            lead_id=lead_id,
        )
        
        return session.session_id

    async def transition_to_active(self, session_id: str) -> None:
        """
        Transition conversation to active state.
        
        Args:
            session_id: Session ID
        """
        self._session_lifecycle_states[session_id] = ConversationLifecycleState.ACTIVE
        
        # Cancel any idle timer
        if session_id in self._idle_timers:
            self._idle_timers[session_id].cancel()
            del self._idle_timers[session_id]
        
        logger.debug("Conversation transitioned to active", session_id=session_id)

    async def transition_to_idle(
        self,
        session_id: str,
        idle_timeout: float = 60.0,
    ) -> None:
        """
        Transition conversation to idle state.
        
        Args:
            session_id: Session ID
            idle_timeout: Timeout before conversation is considered timed out
        """
        self._session_lifecycle_states[session_id] = ConversationLifecycleState.IDLE
        
        # Start idle timer
        async def idle_timer():
            await asyncio.sleep(idle_timeout)
            await self.transition_to_timeout(session_id)
        
        self._idle_timers[session_id] = asyncio.create_task(idle_timer())
        
        logger.debug("Conversation transitioned to idle", session_id=session_id)

    async def transition_to_timeout(self, session_id: str) -> None:
        """
        Transition conversation to timeout state.
        
        Args:
            session_id: Session ID
        """
        self._session_lifecycle_states[session_id] = ConversationLifecycleState.TIMEOUT
        
        # Cancel idle timer
        if session_id in self._idle_timers:
            self._idle_timers[session_id].cancel()
            del self._idle_timers[session_id]
        
        # Publish error event
        await publish_error_occurred(
            session_id=session_id,
            error="Conversation timeout",
            error_type="timeout",
        )
        
        # End conversation
        await self.end_conversation(session_id, status="failed")
        
        logger.warning("Conversation timed out", session_id=session_id)

    async def transition_to_complete(
        self,
        session_id: str,
        status: str = "completed",
    ) -> None:
        """
        Transition conversation to complete state.
        
        Args:
            session_id: Session ID
            status: Final status (completed, failed, transferred)
        """
        self._session_lifecycle_states[session_id] = ConversationLifecycleState.COMPLETE
        
        # Cancel idle timer
        if session_id in self._idle_timers:
            self._idle_timers[session_id].cancel()
            del self._idle_timers[session_id]
        
        # End conversation
        await self.end_conversation(session_id, status=status)
        
        logger.info("Conversation completed", session_id=session_id, status=status)

    async def end_conversation(
        self,
        session_id: str,
        status: str = "completed",
    ) -> None:
        """
        End a conversation.
        
        Args:
            session_id: Session ID
            status: Final status
        """
        # Close session
        await self._session_manager.close_session(session_id, status=status)
        
        # Publish event
        await publish_conversation_ended(
            session_id=session_id,
            data={"status": status},
        )
        
        # Transition to archived
        await self.transition_to_archived(session_id)
        
        logger.info("Conversation ended", session_id=session_id, status=status)

    async def transition_to_archived(self, session_id: str) -> None:
        """
        Transition conversation to archived state.
        
        Args:
            session_id: Session ID
        """
        self._session_lifecycle_states[session_id] = ConversationLifecycleState.ARCHIVED
        
        # Cleanup resources
        if session_id in self._idle_timers:
            self._idle_timers[session_id].cancel()
            del self._idle_timers[session_id]
        
        logger.debug("Conversation archived", session_id=session_id)

    def get_lifecycle_state(
        self,
        session_id: str,
    ) -> Optional[ConversationLifecycleState]:
        """
        Get the lifecycle state of a conversation.
        
        Args:
            session_id: Session ID
        
        Returns:
            Lifecycle state or None if not found
        """
        return self._session_lifecycle_states.get(session_id)

    def is_active(self, session_id: str) -> bool:
        """
        Check if a conversation is active.
        
        Args:
            session_id: Session ID
        
        Returns:
            True if conversation is active
        """
        state = self._session_lifecycle_states.get(session_id)
        return state == ConversationLifecycleState.ACTIVE

    def is_idle(self, session_id: str) -> bool:
        """
        Check if a conversation is idle.
        
        Args:
            session_id: Session ID
        
        Returns:
            True if conversation is idle
        """
        state = self._session_lifecycle_states.get(session_id)
        return state == ConversationLifecycleState.IDLE

    def is_complete(self, session_id: str) -> bool:
        """
        Check if a conversation is complete.
        
        Args:
            session_id: Session ID
        
        Returns:
            True if conversation is complete
        """
        state = self._session_lifecycle_states.get(session_id)
        return state == ConversationLifecycleState.COMPLETE

    def is_archived(self, session_id: str) -> bool:
        """
        Check if a conversation is archived.
        
        Args:
            session_id: Session ID
        
        Returns:
            True if conversation is archived
        """
        state = self._session_lifecycle_states.get(session_id)
        return state == ConversationLifecycleState.ARCHIVED

    async def cleanup_session(self, session_id: str) -> None:
        """
        Cleanup resources for a session.
        
        Args:
            session_id: Session ID
        """
        # Cancel idle timer
        if session_id in self._idle_timers:
            self._idle_timers[session_id].cancel()
            del self._idle_timers[session_id]
        
        # Remove lifecycle state
        if session_id in self._session_lifecycle_states:
            del self._session_lifecycle_states[session_id]
        
        logger.debug("Session cleanup completed", session_id=session_id)

    async def cleanup_expired_sessions(
        self,
        max_age_hours: float = 24.0,
    ) -> int:
        """
        Cleanup expired archived sessions.
        
        Args:
            max_age_hours: Maximum age in hours before cleanup
        
        Returns:
            Number of sessions cleaned up
        """
        cleaned_count = 0
        
        # Get all archived sessions
        archived_sessions = [
            session_id
            for session_id, state in self._session_lifecycle_states.items()
            if state == ConversationLifecycleState.ARCHIVED
        ]
        
        for session_id in archived_sessions:
            session = await self._session_manager.get_session(session_id, db=None)
            
            if session and session.end_time:
                age = (datetime.utcnow() - session.end_time).total_seconds() / 3600
                
                if age > max_age_hours:
                    await self.cleanup_session(session_id)
                    cleaned_count += 1
        
        if cleaned_count > 0:
            logger.info("Expired sessions cleaned up", count=cleaned_count)
        
        return cleaned_count

    def get_active_session_count(self) -> int:
        """
        Get the number of active sessions.
        
        Returns:
            Number of active sessions
        """
        return sum(
            1
            for state in self._session_lifecycle_states.values()
            if state == ConversationLifecycleState.ACTIVE
        )

    def get_idle_session_count(self) -> int:
        """
        Get the number of idle sessions.
        
        Returns:
            Number of idle sessions
        """
        return sum(
            1
            for state in self._session_lifecycle_states.values()
            if state == ConversationLifecycleState.IDLE
        )

    def get_lifecycle_summary(self) -> Dict[str, int]:
        """
        Get a summary of lifecycle states.
        
        Returns:
            Dictionary with counts for each lifecycle state
        """
        summary = {
            "starting": 0,
            "active": 0,
            "idle": 0,
            "timeout": 0,
            "complete": 0,
            "archived": 0,
        }
        
        for state in self._session_lifecycle_states.values():
            summary[state.value] += 1
        
        return summary


# Global lifecycle manager instance
_lifecycle_manager: Optional[LifecycleManager] = None


def get_lifecycle_manager() -> LifecycleManager:
    """
    Get the global lifecycle manager instance.
    
    Returns:
        LifecycleManager: The global lifecycle manager
    """
    global _lifecycle_manager
    if _lifecycle_manager is None:
        _lifecycle_manager = LifecycleManager()
    return _lifecycle_manager
