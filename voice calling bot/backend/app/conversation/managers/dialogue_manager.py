from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime

from app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class DialogueState:
    """State of the dialogue manager."""

    current_topic: Optional[str] = None
    conversation_objective: Optional[str] = None
    previous_responses: List[str] = field(default_factory=list)
    pending_questions: List[str] = field(default_factory=list)
    expected_user_response: Optional[str] = None
    conversation_transitions: List[Dict[str, Any]] = field(default_factory=list)
    fallback_triggered: bool = False
    context_preserved: bool = True


class DialogueManager:
    """
    Manager for dialogue state and flow.
    
    This manager is responsible for:
    - Current topic tracking
    - Conversation objective management
    - Previous response tracking
    - Pending question management
    - Expected user response tracking
    - Conversation transition handling
    - Fallback handling
    - Context preservation
    
    This is a framework for dialogue management. Business logic for
    specific dialogue flows should be implemented by modules that use this manager.
    """

    def __init__(self):
        """Initialize the dialogue manager."""
        self._dialogue_states: Dict[str, DialogueState] = {}

    def initialize_dialogue(
        self,
        session_id: str,
        objective: Optional[str] = None,
        initial_topic: Optional[str] = None,
    ) -> DialogueState:
        """
        Initialize dialogue state for a session.
        
        Args:
            session_id: Session ID
            objective: Conversation objective
            initial_topic: Initial topic
        
        Returns:
            Initialized dialogue state
        """
        state = DialogueState(
            current_topic=initial_topic,
            conversation_objective=objective,
        )
        
        self._dialogue_states[session_id] = state
        
        logger.info(
            "Dialogue initialized",
            session_id=session_id,
            objective=objective,
            initial_topic=initial_topic,
        )
        
        return state

    def get_dialogue_state(self, session_id: str) -> Optional[DialogueState]:
        """
        Get the dialogue state for a session.
        
        Args:
            session_id: Session ID
        
        Returns:
            Dialogue state or None if not found
        """
        return self._dialogue_states.get(session_id)

    def set_current_topic(
        self,
        session_id: str,
        topic: str,
    ) -> bool:
        """
        Set the current topic of the conversation.
        
        Args:
            session_id: Session ID
            topic: Current topic
        
        Returns:
            True if topic was set successfully
        """
        state = self._dialogue_states.get(session_id)
        
        if not state:
            return False
        
        # Record transition
        if state.current_topic != topic:
            state.conversation_transitions.append({
                "from_topic": state.current_topic,
                "to_topic": topic,
                "timestamp": datetime.utcnow().isoformat(),
            })
        
        state.current_topic = topic
        
        logger.debug("Current topic set", session_id=session_id, topic=topic)
        
        return True

    def get_current_topic(self, session_id: str) -> Optional[str]:
        """
        Get the current topic of the conversation.
        
        Args:
            session_id: Session ID
        
        Returns:
            Current topic or None
        """
        state = self._dialogue_states.get(session_id)
        
        if not state:
            return None
        
        return state.current_topic

    def set_conversation_objective(
        self,
        session_id: str,
        objective: str,
    ) -> bool:
        """
        Set the conversation objective.
        
        Args:
            session_id: Session ID
            objective: Conversation objective
        
        Returns:
            True if objective was set successfully
        """
        state = self._dialogue_states.get(session_id)
        
        if not state:
            return False
        
        state.conversation_objective = objective
        
        logger.debug("Conversation objective set", session_id=session_id, objective=objective)
        
        return True

    def get_conversation_objective(self, session_id: str) -> Optional[str]:
        """
        Get the conversation objective.
        
        Args:
            session_id: Session ID
        
        Returns:
            Conversation objective or None
        """
        state = self._dialogue_states.get(session_id)
        
        if not state:
            return None
        
        return state.conversation_objective

    def add_response(
        self,
        session_id: str,
        response: str,
    ) -> bool:
        """
        Add a response to the previous responses list.
        
        Args:
            session_id: Session ID
            response: Response to add
        
        Returns:
            True if response was added successfully
        """
        state = self._dialogue_states.get(session_id)
        
        if not state:
            return False
        
        state.previous_responses.append(response)
        
        # Keep only last 20 responses
        if len(state.previous_responses) > 20:
            state.previous_responses = state.previous_responses[-20:]
        
        logger.debug("Response added", session_id=session_id)
        
        return True

    def get_previous_responses(
        self,
        session_id: str,
        limit: int = 5,
    ) -> List[str]:
        """
        Get previous responses from the conversation.
        
        Args:
            session_id: Session ID
            limit: Number of responses to retrieve
        
        Returns:
            List of previous responses
        """
        state = self._dialogue_states.get(session_id)
        
        if not state:
            return []
        
        return state.previous_responses[-limit:] if state.previous_responses else []

    def add_pending_question(
        self,
        session_id: str,
        question: str,
    ) -> bool:
        """
        Add a pending question to the list.
        
        Args:
            session_id: Session ID
            question: Question to add
        
        Returns:
            True if question was added successfully
        """
        state = self._dialogue_states.get(session_id)
        
        if not state:
            return False
        
        state.pending_questions.append(question)
        
        logger.debug("Pending question added", session_id=session_id)
        
        return True

    def get_pending_questions(self, session_id: str) -> List[str]:
        """
        Get pending questions for the conversation.
        
        Args:
            session_id: Session ID
        
        Returns:
            List of pending questions
        """
        state = self._dialogue_states.get(session_id)
        
        if not state:
            return []
        
        return state.pending_questions.copy()

    def remove_pending_question(
        self,
        session_id: str,
        question: str,
    ) -> bool:
        """
        Remove a pending question from the list.
        
        Args:
            session_id: Session ID
            question: Question to remove
        
        Returns:
            True if question was removed successfully
        """
        state = self._dialogue_states.get(session_id)
        
        if not state or question not in state.pending_questions:
            return False
        
        state.pending_questions.remove(question)
        
        logger.debug("Pending question removed", session_id=session_id)
        
        return True

    def clear_pending_questions(self, session_id: str) -> bool:
        """
        Clear all pending questions.
        
        Args:
            session_id: Session ID
        
        Returns:
            True if questions were cleared successfully
        """
        state = self._dialogue_states.get(session_id)
        
        if not state:
            return False
        
        state.pending_questions.clear()
        
        logger.debug("Pending questions cleared", session_id=session_id)
        
        return True

    def set_expected_response(
        self,
        session_id: str,
        expected_response: str,
    ) -> bool:
        """
        Set the expected user response.
        
        Args:
            session_id: Session ID
            expected_response: Expected response type or content
        
        Returns:
            True if expected response was set successfully
        """
        state = self._dialogue_states.get(session_id)
        
        if not state:
            return False
        
        state.expected_user_response = expected_response
        
        logger.debug("Expected response set", session_id=session_id)
        
        return True

    def get_expected_response(self, session_id: str) -> Optional[str]:
        """
        Get the expected user response.
        
        Args:
            session_id: Session ID
        
        Returns:
            Expected response or None
        """
        state = self._dialogue_states.get(session_id)
        
        if not state:
            return None
        
        return state.expected_user_response

    def record_transition(
        self,
        session_id: str,
        from_topic: Optional[str],
        to_topic: str,
        reason: Optional[str] = None,
    ) -> bool:
        """
        Record a conversation transition.
        
        Args:
            session_id: Session ID
            from_topic: Previous topic
            to_topic: New topic
            reason: Reason for transition
        
        Returns:
            True if transition was recorded successfully
        """
        state = self._dialogue_states.get(session_id)
        
        if not state:
            return False
        
        state.conversation_transitions.append({
            "from_topic": from_topic,
            "to_topic": to_topic,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat(),
        })
        
        logger.debug(
            "Transition recorded",
            session_id=session_id,
            from_topic=from_topic,
            to_topic=to_topic,
        )
        
        return True

    def get_transition_history(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get the conversation transition history.
        
        Args:
            session_id: Session ID
        
        Returns:
            List of transitions
        """
        state = self._dialogue_states.get(session_id)
        
        if not state:
            return []
        
        return state.conversation_transitions.copy()

    def trigger_fallback(self, session_id: str) -> bool:
        """
        Trigger fallback handling.
        
        Args:
            session_id: Session ID
        
        Returns:
            True if fallback was triggered successfully
        """
        state = self._dialogue_states.get(session_id)
        
        if not state:
            return False
        
        state.fallback_triggered = True
        
        logger.warning("Fallback triggered", session_id=session_id)
        
        return True

    def is_fallback_triggered(self, session_id: str) -> bool:
        """
        Check if fallback has been triggered.
        
        Args:
            session_id: Session ID
        
        Returns:
            True if fallback was triggered
        """
        state = self._dialogue_states.get(session_id)
        
        if not state:
            return False
        
        return state.fallback_triggered

    def reset_fallback(self, session_id: str) -> bool:
        """
        Reset fallback trigger.
        
        Args:
            session_id: Session ID
        
        Returns:
            True if fallback was reset successfully
        """
        state = self._dialogue_states.get(session_id)
        
        if not state:
            return False
        
        state.fallback_triggered = False
        
        logger.debug("Fallback reset", session_id=session_id)
        
        return True

    def preserve_context(self, session_id: str, preserved: bool = True) -> bool:
        """
        Set context preservation flag.
        
        Args:
            session_id: Session ID
            preserved: Whether context should be preserved
        
        Returns:
            True if flag was set successfully
        """
        state = self._dialogue_states.get(session_id)
        
        if not state:
            return False
        
        state.context_preserved = preserved
        
        logger.debug("Context preservation set", session_id=session_id, preserved=preserved)
        
        return True

    def is_context_preserved(self, session_id: str) -> bool:
        """
        Check if context is being preserved.
        
        Args:
            session_id: Session ID
        
        Returns:
            True if context is preserved
        """
        state = self._dialogue_states.get(session_id)
        
        if not state:
            return True  # Default to preserved
        
        return state.context_preserved

    def clear_dialogue_state(self, session_id: str) -> bool:
        """
        Clear dialogue state for a session.
        
        Args:
            session_id: Session ID
        
        Returns:
            True if state was cleared successfully
        """
        if session_id in self._dialogue_states:
            del self._dialogue_states[session_id]
            logger.debug("Dialogue state cleared", session_id=session_id)
            return True
        
        return False

    def get_dialogue_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a summary of the dialogue state.
        
        Args:
            session_id: Session ID
        
        Returns:
            Dialogue summary or None if not found
        """
        state = self._dialogue_states.get(session_id)
        
        if not state:
            return None
        
        return {
            "current_topic": state.current_topic,
            "conversation_objective": state.conversation_objective,
            "response_count": len(state.previous_responses),
            "pending_questions_count": len(state.pending_questions),
            "expected_response": state.expected_user_response,
            "transition_count": len(state.conversation_transitions),
            "fallback_triggered": state.fallback_triggered,
            "context_preserved": state.context_preserved,
        }


# Global dialogue manager instance
_dialogue_manager: Optional[DialogueManager] = None


def get_dialogue_manager() -> DialogueManager:
    """
    Get the global dialogue manager instance.
    
    Returns:
        DialogueManager: The global dialogue manager
    """
    global _dialogue_manager
    if _dialogue_manager is None:
        _dialogue_manager = DialogueManager()
    return _dialogue_manager
