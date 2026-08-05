import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.conversation.core.state_machine import StateMachine, create_default_state_machine
from app.core.logging import get_logger
from app.database.connection import get_db
from app.models.conversation import (
    ConversationSession,
    ConversationContext,
    ConversationStateTransition,
)

logger = get_logger(__name__)


class SessionManager:
    """
    Manager for conversation session lifecycle.
    
    This manager handles the creation, resumption, pausing, closing,
    and cleanup of conversation sessions. Each active call has an
    isolated conversation session with complete isolation from others.
    """

    def __init__(self):
        """Initialize the session manager."""
        self._active_sessions: Dict[str, ConversationSession] = {}
        self._session_state_machines: Dict[str, StateMachine] = {}

    async def create_session(
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
        db: AsyncSession = None,
    ) -> ConversationSession:
        """
        Create a new conversation session.
        
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
            db: Database session
        
        Returns:
            Created conversation session
        """
        session_id = str(uuid.uuid4())
        
        # Create session record
        session = ConversationSession(
            session_id=session_id,
            organization_id=organization_id,
            campaign_id=campaign_id,
            agent_id=agent_id,
            lead_id=lead_id,
            current_state="initializing",
            start_time=datetime.utcnow(),
            last_activity=datetime.utcnow(),
            status="active",
            personality_id=personality_id,
            script_id=script_id,
            call_id=call_id,
            phone_number=phone_number,
            metadata=metadata or {},
        )
        
        if db:
            db.add(session)
            await db.commit()
            await db.refresh(session)
        
        # Create state machine for this session
        state_machine = create_default_state_machine()
        state_machine.initialize()
        
        # Store in memory
        self._active_sessions[session_id] = session
        self._session_state_machines[session_id] = state_machine
        
        # Create context record
        context = ConversationContext(
            session_id=session_id,
            variables={},
            customer_info={},
            agent_info={},
            campaign_info={},
            rag_context={},
            nlp_context={},
            tool_outputs={},
        )
        
        if db:
            db.add(context)
            await db.commit()
        
        logger.info(
            "Conversation session created",
            session_id=session_id,
            organization_id=organization_id,
            lead_id=lead_id,
        )
        
        return session

    async def get_session(
        self,
        session_id: str,
        db: Optional[AsyncSession] = None,
    ) -> Optional[ConversationSession]:
        """
        Get a conversation session by ID.
        
        Args:
            session_id: Session ID
            db: Database session
        
        Returns:
            Conversation session or None if not found
        """
        # Check memory first
        if session_id in self._active_sessions:
            return self._active_sessions[session_id]
        
        # Check database
        if db:
            result = await db.execute(
                select(ConversationSession)
                .where(ConversationSession.session_id == session_id)
                .where(ConversationSession.deleted_at.is_(None))
            )
            session = result.scalar_one_or_none()
            
            if session:
                # Load into memory
                self._active_sessions[session_id] = session
                state_machine = create_default_state_machine()
                state_machine.initialize(session.current_state)
                self._session_state_machines[session_id] = state_machine
            
            return session
        
        return None

    async def resume_session(
        self,
        session_id: str,
        db: AsyncSession,
    ) -> Optional[ConversationSession]:
        """
        Resume a paused session.
        
        Args:
            session_id: Session ID
            db: Database session
        
        Returns:
            Resumed session or None if not found
        """
        session = await self.get_session(session_id, db)
        
        if not session:
            logger.warning("Session not found for resume", session_id=session_id)
            return None
        
        if session.status != "paused":
            logger.warning(
                "Session is not paused",
                session_id=session_id,
                status=session.status,
            )
            return session
        
        # Update status
        session.status = "active"
        session.last_activity = datetime.utcnow()
        
        await db.commit()
        await db.refresh(session)
        
        logger.info("Session resumed", session_id=session_id)
        
        return session

    async def pause_session(
        self,
        session_id: str,
        db: AsyncSession,
    ) -> Optional[ConversationSession]:
        """
        Pause an active session.
        
        Args:
            session_id: Session ID
            db: Database session
        
        Returns:
            Paused session or None if not found
        """
        session = await self.get_session(session_id, db)
        
        if not session:
            logger.warning("Session not found for pause", session_id=session_id)
            return None
        
        if session.status != "active":
            logger.warning(
                "Session is not active",
                session_id=session_id,
                status=session.status,
            )
            return session
        
        # Update status
        session.status = "paused"
        session.last_activity = datetime.utcnow()
        
        await db.commit()
        await db.refresh(session)
        
        logger.info("Session paused", session_id=session_id)
        
        return session

    async def close_session(
        self,
        session_id: str,
        status: str = "completed",
        db: AsyncSession = None,
    ) -> Optional[ConversationSession]:
        """
        Close a conversation session.
        
        Args:
            session_id: Session ID
            status: Final status (completed, failed, transferred, ended)
            db: Database session
        
        Returns:
            Closed session or None if not found
        """
        session = await self.get_session(session_id, db)
        
        if not session:
            logger.warning("Session not found for close", session_id=session_id)
            return None
        
        # Update session
        session.status = status
        session.end_time = datetime.utcnow()
        session.last_activity = datetime.utcnow()
        
        # Calculate total duration
        if session.start_time:
            session.total_duration = (session.end_time - session.start_time).total_seconds()
        
        if db:
            await db.commit()
            await db.refresh(session)
        
        # Remove from memory
        if session_id in self._active_sessions:
            del self._active_sessions[session_id]
        if session_id in self._session_state_machines:
            del self._session_state_machines[session_id]
        
        logger.info(
            "Session closed",
            session_id=session_id,
            status=status,
            duration=session.total_duration,
        )
        
        return session

    async def update_session_state(
        self,
        session_id: str,
        new_state: str,
        trigger: str,
        reason: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        db: AsyncSession = None,
    ) -> bool:
        """
        Update the state of a conversation session.
        
        Args:
            session_id: Session ID
            new_state: New state
            trigger: Transition trigger
            reason: Reason for transition
            metadata: Additional metadata
            db: Database session
        
        Returns:
            True if state was updated successfully
        """
        session = await self.get_session(session_id, db)
        
        if not session:
            logger.warning("Session not found for state update", session_id=session_id)
            return False
        
        # Get state machine
        state_machine = self._session_state_machines.get(session_id)
        if not state_machine:
            state_machine = create_default_state_machine()
            state_machine.initialize(session.current_state)
            self._session_state_machines[session_id] = state_machine
        
        # Attempt transition
        success = state_machine.transition_to(new_state, trigger, reason, metadata)
        
        if success:
            # Update session
            previous_state = session.current_state
            session.current_state = new_state
            session.previous_state = previous_state
            session.last_activity = datetime.utcnow()
            
            if db:
                # Record transition
                transition = ConversationStateTransition(
                    session_id=session_id,
                    from_state=previous_state,
                    to_state=new_state,
                    reason=reason,
                    trigger=trigger,
                    metadata=metadata or {},
                )
                db.add(transition)
                
                await db.commit()
                await db.refresh(session)
            
            logger.info(
                "Session state updated",
                session_id=session_id,
                from_state=previous_state,
                to_state=new_state,
                trigger=trigger,
            )
        
        return success

    async def update_session_activity(
        self,
        session_id: str,
        db: AsyncSession,
    ) -> bool:
        """
        Update the last activity timestamp for a session.
        
        Args:
            session_id: Session ID
            db: Database session
        
        Returns:
            True if updated successfully
        """
        session = await self.get_session(session_id, db)
        
        if not session:
            return False
        
        session.last_activity = datetime.utcnow()
        
        if db:
            await db.commit()
        
        return True

    async def check_session_timeout(
        self,
        session_id: str,
        timeout_seconds: float = 300.0,
        db: AsyncSession = None,
    ) -> bool:
        """
        Check if a session has timed out.
        
        Args:
            session_id: Session ID
            timeout_seconds: Timeout in seconds
            db: Database session
        
        Returns:
            True if session has timed out
        """
        session = await self.get_session(session_id, db)
        
        if not session:
            return False
        
        if session.status != "active":
            return False
        
        # Check state timeout
        state_machine = self._session_state_machines.get(session_id)
        if state_machine:
            timeout_state = state_machine.check_timeout()
            if timeout_state:
                logger.warning(
                    "Session state timeout",
                    session_id=session_id,
                    state=timeout_state,
                )
                return True
        
        # Check session timeout
        time_since_activity = (datetime.utcnow() - session.last_activity).total_seconds()
        
        if time_since_activity > timeout_seconds:
            logger.warning(
                "Session timeout",
                session_id=session_id,
                time_since_activity=time_since_activity,
                timeout=timeout_seconds,
            )
            return True
        
        return False

    async def cleanup_expired_sessions(
        self,
        timeout_seconds: float = 3600.0,
        db: AsyncSession = None,
    ) -> int:
        """
        Cleanup expired sessions from memory.
        
        Args:
            timeout_seconds: Timeout in seconds
            db: Database session
        
        Returns:
            Number of sessions cleaned up
        """
        cleaned_count = 0
        current_time = datetime.utcnow()
        
        sessions_to_remove = []
        
        for session_id, session in self._active_sessions.items():
            if session.status in ["completed", "failed", "transferred", "ended"]:
                # Session is already closed, remove from memory
                sessions_to_remove.append(session_id)
            else:
                time_since_activity = (current_time - session.last_activity).total_seconds()
                if time_since_activity > timeout_seconds:
                    sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            if session_id in self._active_sessions:
                del self._active_sessions[session_id]
            if session_id in self._session_state_machines:
                del self._session_state_machines[session_id]
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
        return len(self._active_sessions)

    def get_session_state_machine(self, session_id: str) -> Optional[StateMachine]:
        """
        Get the state machine for a session.
        
        Args:
            session_id: Session ID
        
        Returns:
            State machine or None if not found
        """
        return self._session_state_machines.get(session_id)

    async def get_session_context(
        self,
        session_id: str,
        db: AsyncSession,
    ) -> Optional[ConversationContext]:
        """
        Get the context for a session.
        
        Args:
            session_id: Session ID
            db: Database session
        
        Returns:
            Conversation context or None if not found
        """
        result = await db.execute(
            select(ConversationContext)
            .where(ConversationContext.session_id == session_id)
        )
        return result.scalar_one_or_none()


# Global session manager instance
_session_manager: Optional[SessionManager] = None


def get_session_manager() -> SessionManager:
    """
    Get the global session manager instance.
    
    Returns:
        SessionManager: The global session manager
    """
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
