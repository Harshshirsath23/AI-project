from typing import Optional, Dict, List, Callable, Any
from dataclasses import dataclass, field
from enum import Enum

from app.core.logging import get_logger

logger = get_logger(__name__)


class ConversationState(str, Enum):
    """Enumeration of conversation states."""

    INITIALIZING = "initializing"
    GREETING = "greeting"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"
    WAITING = "waiting"
    TOOL_EXECUTION = "tool_execution"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    TRANSFERRED = "transferred"
    ENDED = "ended"


class TransitionTrigger(str, Enum):
    """Enumeration of transition triggers."""

    USER_INPUT = "user_input"
    TOOL_RESULT = "tool_result"
    TIMEOUT = "timeout"
    ERROR = "error"
    MANUAL = "manual"
    SYSTEM = "system"
    CALL_STARTED = "call_started"
    CALL_ENDED = "call_ended"
    TRANSFER_REQUESTED = "transfer_requested"


@dataclass
class StateDefinition:
    """Definition of a state in the state machine."""

    name: str
    description: Optional[str] = None
    allowed_transitions: List[str] = field(default_factory=list)
    entry_actions: List[str] = field(default_factory=list)
    exit_actions: List[str] = field(default_factory=list)
    timeout: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TransitionRule:
    """Rule for state transitions."""

    from_state: str
    to_state: str
    trigger: str
    condition: Optional[str] = None
    priority: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StateTransition:
    """Record of a state transition."""

    from_state: Optional[str]
    to_state: str
    trigger: str
    reason: Optional[str] = None
    timestamp: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class StateMachine:
    """
    Reusable state machine for conversation management.
    
    This state machine manages conversation state transitions with support for:
    - State definitions with entry/exit actions
    - Transition rules with conditions
    - Timeout handling
    - Transition history tracking
    - Event-driven transitions
    """

    def __init__(self):
        """Initialize the state machine."""
        self._states: Dict[str, StateDefinition] = {}
        self._transitions: List[TransitionRule] = []
        self._current_state: Optional[str] = None
        self._transition_history: List[StateTransition] = []
        self._state_entry_time: Optional[float] = None
        self._callbacks: Dict[str, List[Callable]] = {
            "on_enter": [],
            "on_exit": [],
            "on_transition": [],
            "on_timeout": [],
        }

    def add_state(self, state: StateDefinition) -> None:
        """
        Add a state definition to the state machine.
        
        Args:
            state: State definition to add
        """
        self._states[state.name] = state
        logger.debug("State added to state machine", state=state.name)

    def add_transition(self, transition: TransitionRule) -> None:
        """
        Add a transition rule to the state machine.
        
        Args:
            transition: Transition rule to add
        """
        self._transitions.append(transition)
        # Sort by priority (higher priority first)
        self._transitions.sort(key=lambda t: t.priority, reverse=True)
        logger.debug(
            "Transition added to state machine",
            from_state=transition.from_state,
            to_state=transition.to_state,
            trigger=transition.trigger,
        )

    def register_callback(
        self,
        event_type: str,
        callback: Callable,
    ) -> None:
        """
        Register a callback for state machine events.
        
        Args:
            event_type: Event type (on_enter, on_exit, on_transition, on_timeout)
            callback: Callback function
        """
        if event_type in self._callbacks:
            self._callbacks[event_type].append(callback)
            logger.debug("Callback registered", event_type=event_type)
        else:
            raise ValueError(f"Invalid event type: {event_type}")

    def initialize(self, initial_state: str = ConversationState.INITIALIZING) -> None:
        """
        Initialize the state machine with an initial state.
        
        Args:
            initial_state: Initial state to set
        """
        if initial_state not in self._states:
            raise ValueError(f"Initial state '{initial_state}' not defined")
        
        self._current_state = initial_state
        self._state_entry_time = self._get_current_time()
        
        # Execute entry actions
        self._execute_entry_actions(initial_state)
        
        logger.info("State machine initialized", initial_state=initial_state)

    def transition_to(
        self,
        new_state: str,
        trigger: str,
        reason: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Transition to a new state.
        
        Args:
            new_state: Target state
            trigger: Trigger for the transition
            reason: Reason for transition
            metadata: Additional metadata
        
        Returns:
            bool: True if transition was successful
        """
        if self._current_state is None:
            raise RuntimeError("State machine not initialized")
        
        # Check if transition is allowed
        if not self._is_transition_allowed(self._current_state, new_state, trigger):
            logger.warning(
                "Transition not allowed",
                from_state=self._current_state,
                to_state=new_state,
                trigger=trigger,
            )
            return False
        
        # Execute exit actions for current state
        self._execute_exit_actions(self._current_state)
        
        # Record transition
        transition = StateTransition(
            from_state=self._current_state,
            to_state=new_state,
            trigger=trigger,
            reason=reason,
            timestamp=self._get_current_time(),
            metadata=metadata or {},
        )
        self._transition_history.append(transition)
        
        # Update current state
        previous_state = self._current_state
        self._current_state = new_state
        self._state_entry_time = self._get_current_time()
        
        # Execute entry actions for new state
        self._execute_entry_actions(new_state)
        
        # Execute transition callbacks
        self._execute_callbacks("on_transition", transition)
        
        logger.info(
            "State transition executed",
            from_state=previous_state,
            to_state=new_state,
            trigger=trigger,
        )
        
        return True

    def can_transition(
        self,
        new_state: str,
        trigger: str,
    ) -> bool:
        """
        Check if a transition is possible.
        
        Args:
            new_state: Target state
            trigger: Trigger for the transition
        
        Returns:
            bool: True if transition is possible
        """
        if self._current_state is None:
            return False
        
        return self._is_transition_allowed(self._current_state, new_state, trigger)

    def get_current_state(self) -> Optional[str]:
        """
        Get the current state.
        
        Returns:
            Current state or None if not initialized
        """
        return self._current_state

    def get_state_definition(self, state: str) -> Optional[StateDefinition]:
        """
        Get the definition of a state.
        
        Args:
            state: State name
        
        Returns:
            State definition or None if not found
        """
        return self._states.get(state)

    def get_transition_history(self) -> List[StateTransition]:
        """
        Get the transition history.
        
        Returns:
            List of state transitions
        """
        return self._transition_history.copy()

    def get_time_in_current_state(self) -> float:
        """
        Get the time spent in the current state.
        
        Returns:
            Time in seconds since entering current state
        """
        if self._state_entry_time is None:
            return 0.0
        
        return self._get_current_time() - self._state_entry_time

    def check_timeout(self) -> Optional[str]:
        """
        Check if the current state has timed out.
        
        Returns:
            Timeout state if timed out, None otherwise
        """
        if self._current_state is None:
            return None
        
        state_def = self._states.get(self._current_state)
        if state_def and state_def.timeout:
            time_in_state = self.get_time_in_current_state()
            if time_in_state > state_def.timeout:
                logger.warning(
                    "State timeout",
                    state=self._current_state,
                    timeout=state_def.timeout,
                    time_in_state=time_in_state,
                )
                self._execute_callbacks("on_timeout", self._current_state)
                return self._current_state
        
        return None

    def reset(self) -> None:
        """Reset the state machine to initial state."""
        self._current_state = None
        self._transition_history.clear()
        self._state_entry_time = None
        logger.info("State machine reset")

    def _is_transition_allowed(
        self,
        from_state: str,
        to_state: str,
        trigger: str,
    ) -> bool:
        """
        Check if a transition is allowed based on rules.
        
        Args:
            from_state: Source state
            to_state: Target state
            trigger: Transition trigger
        
        Returns:
            bool: True if transition is allowed
        """
        # Check if target state exists
        if to_state not in self._states:
            return False
        
        # Find matching transition rule
        for rule in self._transitions:
            if (
                rule.from_state == from_state
                and rule.to_state == to_state
                and rule.trigger == trigger
            ):
                # Check condition if present
                if rule.condition:
                    # In a real implementation, this would evaluate the condition
                    # For now, we assume conditions are always met
                    pass
                return True
        
        # Check if transition is in allowed transitions
        state_def = self._states.get(from_state)
        if state_def and to_state in state_def.allowed_transitions:
            return True
        
        return False

    def _execute_entry_actions(self, state: str) -> None:
        """
        Execute entry actions for a state.
        
        Args:
            state: State to execute entry actions for
        """
        state_def = self._states.get(state)
        if state_def:
            for action in state_def.entry_actions:
                self._execute_callbacks("on_enter", (state, action))
                logger.debug("Entry action executed", state=state, action=action)

    def _execute_exit_actions(self, state: str) -> None:
        """
        Execute exit actions for a state.
        
        Args:
            state: State to execute exit actions for
        """
        state_def = self._states.get(state)
        if state_def:
            for action in state_def.exit_actions:
                self._execute_callbacks("on_exit", (state, action))
                logger.debug("Exit action executed", state=state, action=action)

    def _execute_callbacks(
        self,
        event_type: str,
        data: Any,
    ) -> None:
        """
        Execute callbacks for an event type.
        
        Args:
            event_type: Event type
            data: Data to pass to callbacks
        """
        for callback in self._callbacks.get(event_type, []):
            try:
                callback(data)
            except Exception as e:
                logger.error(
                    "Callback execution failed",
                    event_type=event_type,
                    error=str(e),
                )

    def _get_current_time(self) -> float:
        """
        Get the current time.
        
        Returns:
            Current time as float (seconds since epoch)
        """
        import time
        return time.time()


def create_default_state_machine() -> StateMachine:
    """
    Create a state machine with default conversation states.
    
    Returns:
        StateMachine configured with default states and transitions
    """
    machine = StateMachine()
    
    # Add default states
    default_states = [
        StateDefinition(
            name=ConversationState.INITIALIZING,
            description="Conversation is being initialized",
            allowed_transitions=[ConversationState.GREETING, ConversationState.FAILED],
        ),
        StateDefinition(
            name=ConversationState.GREETING,
            description="Agent is greeting the customer",
            allowed_transitions=[ConversationState.LISTENING, ConversationState.ENDED],
        ),
        StateDefinition(
            name=ConversationState.LISTENING,
            description="Agent is listening to customer input",
            allowed_transitions=[
                ConversationState.THINKING,
                ConversationState.WAITING,
                ConversationState.ENDED,
            ],
            timeout=30.0,
        ),
        StateDefinition(
            name=ConversationState.THINKING,
            description="Agent is processing and generating response",
            allowed_transitions=[
                ConversationState.SPEAKING,
                ConversationState.TOOL_EXECUTION,
                ConversationState.FAILED,
            ],
            timeout=10.0,
        ),
        StateDefinition(
            name=ConversationState.SPEAKING,
            description="Agent is speaking to the customer",
            allowed_transitions=[ConversationState.LISTENING, ConversationState.ENDED],
        ),
        StateDefinition(
            name=ConversationState.WAITING,
            description="Agent is waiting for customer response",
            allowed_transitions=[
                ConversationState.LISTENING,
                ConversationState.COMPLETED,
                ConversationState.ENDED,
            ],
            timeout=60.0,
        ),
        StateDefinition(
            name=ConversationState.TOOL_EXECUTION,
            description="Agent is executing a tool",
            allowed_transitions=[
                ConversationState.THINKING,
                ConversationState.SPEAKING,
                ConversationState.FAILED,
            ],
            timeout=30.0,
        ),
        StateDefinition(
            name=ConversationState.PAUSED,
            description="Conversation is paused",
            allowed_transitions=[
                ConversationState.LISTENING,
                ConversationState.ENDED,
            ],
        ),
        StateDefinition(
            name=ConversationState.COMPLETED,
            description="Conversation completed successfully",
            allowed_transitions=[ConversationState.ENDED],
        ),
        StateDefinition(
            name=ConversationState.FAILED,
            description="Conversation failed",
            allowed_transitions=[ConversationState.ENDED],
        ),
        StateDefinition(
            name=ConversationState.TRANSFERRED,
            description="Conversation was transferred",
            allowed_transitions=[ConversationState.ENDED],
        ),
        StateDefinition(
            name=ConversationState.ENDED,
            description="Conversation has ended",
            allowed_transitions=[],
        ),
    ]
    
    for state in default_states:
        machine.add_state(state)
    
    # Add default transitions
    default_transitions = [
        TransitionRule(
            from_state=ConversationState.INITIALIZING,
            to_state=ConversationState.GREETING,
            trigger=TransitionTrigger.CALL_STARTED,
            priority=10,
        ),
        TransitionRule(
            from_state=ConversationState.INITIALIZING,
            to_state=ConversationState.FAILED,
            trigger=TransitionTrigger.ERROR,
            priority=10,
        ),
        TransitionRule(
            from_state=ConversationState.GREETING,
            to_state=ConversationState.LISTENING,
            trigger=TransitionTrigger.SYSTEM,
            priority=10,
        ),
        TransitionRule(
            from_state=ConversationState.LISTENING,
            to_state=ConversationState.THINKING,
            trigger=TransitionTrigger.USER_INPUT,
            priority=10,
        ),
        TransitionRule(
            from_state=ConversationState.LISTENING,
            to_state=ConversationState.ENDED,
            trigger=TransitionTrigger.CALL_ENDED,
            priority=10,
        ),
        TransitionRule(
            from_state=ConversationState.LISTENING,
            to_state=ConversationState.ENDED,
            trigger=TransitionTrigger.TIMEOUT,
            priority=5,
        ),
        TransitionRule(
            from_state=ConversationState.THINKING,
            to_state=ConversationState.SPEAKING,
            trigger=TransitionTrigger.SYSTEM,
            priority=10,
        ),
        TransitionRule(
            from_state=ConversationState.THINKING,
            to_state=ConversationState.TOOL_EXECUTION,
            trigger=TransitionTrigger.SYSTEM,
            priority=10,
        ),
        TransitionRule(
            from_state=ConversationState.THINKING,
            to_state=ConversationState.FAILED,
            trigger=TransitionTrigger.ERROR,
            priority=10,
        ),
        TransitionRule(
            from_state=ConversationState.SPEAKING,
            to_state=ConversationState.LISTENING,
            trigger=TransitionTrigger.SYSTEM,
            priority=10,
        ),
        TransitionRule(
            from_state=ConversationState.SPEAKING,
            to_state=ConversationState.ENDED,
            trigger=TransitionTrigger.CALL_ENDED,
            priority=10,
        ),
        TransitionRule(
            from_state=ConversationState.WAITING,
            to_state=ConversationState.LISTENING,
            trigger=TransitionTrigger.USER_INPUT,
            priority=10,
        ),
        TransitionRule(
            from_state=ConversationState.WAITING,
            to_state=ConversationState.COMPLETED,
            trigger=TransitionTrigger.SYSTEM,
            priority=10,
        ),
        TransitionRule(
            from_state=ConversationState.WAITING,
            to_state=ConversationState.ENDED,
            trigger=TransitionTrigger.TIMEOUT,
            priority=5,
        ),
        TransitionRule(
            from_state=ConversationState.TOOL_EXECUTION,
            to_state=ConversationState.THINKING,
            trigger=TransitionTrigger.TOOL_RESULT,
            priority=10,
        ),
        TransitionRule(
            from_state=ConversationState.TOOL_EXECUTION,
            to_state=ConversationState.FAILED,
            trigger=TransitionTrigger.ERROR,
            priority=10,
        ),
        TransitionRule(
            from_state=ConversationState.TOOL_EXECUTION,
            to_state=ConversationState.FAILED,
            trigger=TransitionTrigger.TIMEOUT,
            priority=5,
        ),
        TransitionRule(
            from_state=ConversationState.PAUSED,
            to_state=ConversationState.LISTENING,
            trigger=TransitionTrigger.MANUAL,
            priority=10,
        ),
        TransitionRule(
            from_state=ConversationState.PAUSED,
            to_state=ConversationState.ENDED,
            trigger=TransitionTrigger.MANUAL,
            priority=10,
        ),
        TransitionRule(
            from_state=ConversationState.COMPLETED,
            to_state=ConversationState.ENDED,
            trigger=TransitionTrigger.SYSTEM,
            priority=10,
        ),
        TransitionRule(
            from_state=ConversationState.FAILED,
            to_state=ConversationState.ENDED,
            trigger=TransitionTrigger.SYSTEM,
            priority=10,
        ),
        TransitionRule(
            from_state=ConversationState.TRANSFERRED,
            to_state=ConversationState.ENDED,
            trigger=TransitionTrigger.TRANSFER_REQUESTED,
            priority=10,
        ),
    ]
    
    for transition in default_transitions:
        machine.add_transition(transition)
    
    return machine
