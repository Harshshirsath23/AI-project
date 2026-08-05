from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime

from app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ScriptStep:
    """Definition of a script step."""

    step_id: str
    name: str
    description: Optional[str] = None
    required_state: Optional[str] = None
    actions: List[str] = field(default_factory=list)
    next_steps: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ScriptProgress:
    """Progress tracking for a script execution."""

    script_id: str
    completed_steps: List[str] = field(default_factory=list)
    current_step: Optional[str] = None
    skipped_steps: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ScriptManager:
    """
    Manager for conversation script state and progress.
    
    This manager tracks the progress of a conversation through a predefined
    script or flow. It maintains the state of script execution including:
    - Greeting completed
    - Qualification completed
    - Discovery completed
    - Product discussion
    - Objection handling
    - Closing
    
    The implementation is generic and does not assume any specific script.
    Future script builders should plug into this manager to define their
    own steps and flows.
    """

    def __init__(self):
        """Initialize the script manager."""
        self._scripts: Dict[str, List[ScriptStep]] = {}
        self._session_progress: Dict[str, ScriptProgress] = {}

        # Initialize default script
        self._initialize_default_script()

    def _initialize_default_script(self) -> None:
        """Initialize the default conversation script."""
        default_steps = [
            ScriptStep(
                step_id="greeting",
                name="Greeting",
                description="Initial greeting and introduction",
                required_state="greeting",
                actions=["introduce_agent", "state_purpose"],
                next_steps=["qualification"],
            ),
            ScriptStep(
                step_id="qualification",
                name="Qualification",
                description="Qualify the lead and understand needs",
                required_state="listening",
                actions=["ask_qualification_questions", "assess_fit"],
                next_steps=["discovery", "closing"],
            ),
            ScriptStep(
                step_id="discovery",
                name="Discovery",
                description="Deep dive into customer needs and pain points",
                required_state="listening",
                actions=["explore_needs", "identify_pain_points"],
                next_steps=["product_discussion", "objjection_handling"],
            ),
            ScriptStep(
                step_id="product_discussion",
                name="Product Discussion",
                description="Present relevant products or services",
                required_state="speaking",
                actions=["present_solution", "highlight_benefits"],
                next_steps=["objjection_handling", "closing"],
            ),
            ScriptStep(
                step_id="objection_handling",
                name="Objection Handling",
                description="Address and overcome objections",
                required_state="listening",
                actions=["acknowledge_objection", "provide_reassurance"],
                next_steps=["closing", "product_discussion"],
            ),
            ScriptStep(
                step_id="closing",
                name="Closing",
                description="Close the conversation with next steps",
                required_state="speaking",
                actions=["summarize", "call_to_action"],
                next_steps=[],
            ),
        ]

        self._scripts["default"] = default_steps

        logger.info("Default script initialized", steps=len(default_steps))

    def register_script(
        self,
        script_id: str,
        steps: List[ScriptStep],
    ) -> None:
        """
        Register a new script.
        
        Args:
            script_id: Script ID
            steps: List of script steps
        """
        self._scripts[script_id] = steps
        logger.info("Script registered", script_id=script_id, steps=len(steps))

    def get_script(self, script_id: str) -> Optional[List[ScriptStep]]:
        """
        Get a script by ID.
        
        Args:
            script_id: Script ID
        
        Returns:
            List of script steps or None if not found
        """
        return self._scripts.get(script_id)

    def get_step(self, script_id: str, step_id: str) -> Optional[ScriptStep]:
        """
        Get a specific step from a script.
        
        Args:
            script_id: Script ID
            step_id: Step ID
        
        Returns:
            Script step or None if not found
        """
        steps = self._scripts.get(script_id)
        
        if not steps:
            return None
        
        for step in steps:
            if step.step_id == step_id:
                return step
        
        return None

    def initialize_script_progress(
        self,
        session_id: str,
        script_id: str = "default",
    ) -> ScriptProgress:
        """
        Initialize script progress for a session.
        
        Args:
            session_id: Session ID
            script_id: Script ID to use
        
        Returns:
            Initialized script progress
        """
        if script_id not in self._scripts:
            logger.warning("Script not found, using default", script_id=script_id)
            script_id = "default"
        
        progress = ScriptProgress(script_id=script_id)
        
        self._session_progress[session_id] = progress
        
        logger.info(
            "Script progress initialized",
            session_id=session_id,
            script_id=script_id,
        )
        
        return progress

    def get_script_progress(
        self,
        session_id: str,
    ) -> Optional[ScriptProgress]:
        """
        Get the script progress for a session.
        
        Args:
            session_id: Session ID
        
        Returns:
            Script progress or None if not found
        """
        return self._session_progress.get(session_id)

    def complete_step(
        self,
        session_id: str,
        step_id: str,
    ) -> bool:
        """
        Mark a step as completed.
        
        Args:
            session_id: Session ID
            step_id: Step ID to complete
        
        Returns:
            True if step was completed successfully
        """
        progress = self._session_progress.get(session_id)
        
        if not progress:
            return False
        
        if step_id not in progress.completed_steps:
            progress.completed_steps.append(step_id)
        
        # Move to next step if current
        if progress.current_step == step_id:
            step = self.get_step(progress.script_id, step_id)
            if step and step.next_steps:
                progress.current_step = step.next_steps[0]
        
        logger.debug("Step completed", session_id=session_id, step_id=step_id)
        
        return True

    def skip_step(
        self,
        session_id: str,
        step_id: str,
    ) -> bool:
        """
        Skip a step in the script.
        
        Args:
            session_id: Session ID
            step_id: Step ID to skip
        
        Returns:
            True if step was skipped successfully
        """
        progress = self._session_progress.get(session_id)
        
        if not progress:
            return False
        
        if step_id not in progress.skipped_steps:
            progress.skipped_steps.append(step_id)
        
        # Move to next step if current
        if progress.current_step == step_id:
            step = self.get_step(progress.script_id, step_id)
            if step and step.next_steps:
                progress.current_step = step.next_steps[0]
        
        logger.debug("Step skipped", session_id=session_id, step_id=step_id)
        
        return True

    def set_current_step(
        self,
        session_id: str,
        step_id: str,
    ) -> bool:
        """
        Set the current step in the script.
        
        Args:
            session_id: Session ID
            step_id: Step ID to set as current
        
        Returns:
            True if current step was set successfully
        """
        progress = self._session_progress.get(session_id)
        
        if not progress:
            return False
        
        # Verify step exists in script
        step = self.get_step(progress.script_id, step_id)
        if not step:
            logger.warning("Step not found in script", step_id=step_id)
            return False
        
        progress.current_step = step_id
        
        logger.debug("Current step set", session_id=session_id, step_id=step_id)
        
        return True

    def get_current_step(self, session_id: str) -> Optional[ScriptStep]:
        """
        Get the current step for a session.
        
        Args:
            session_id: Session ID
        
        Returns:
            Current script step or None if not found
        """
        progress = self._session_progress.get(session_id)
        
        if not progress or not progress.current_step:
            return None
        
        return self.get_step(progress.script_id, progress.current_step)

    def get_next_steps(self, session_id: str) -> List[str]:
        """
        Get the possible next steps from the current step.
        
        Args:
            session_id: Session ID
        
        Returns:
            List of possible next step IDs
        """
        current_step = self.get_current_step(session_id)
        
        if not current_step:
            return []
        
        return current_step.next_steps.copy()

    def is_step_completed(
        self,
        session_id: str,
        step_id: str,
    ) -> bool:
        """
        Check if a step has been completed.
        
        Args:
            session_id: Session ID
            step_id: Step ID to check
        
        Returns:
            True if step is completed
        """
        progress = self._session_progress.get(session_id)
        
        if not progress:
            return False
        
        return step_id in progress.completed_steps

    def is_step_skipped(
        self,
        session_id: str,
        step_id: str,
    ) -> bool:
        """
        Check if a step has been skipped.
        
        Args:
            session_id: Session ID
            step_id: Step ID to check
        
        Returns:
            True if step is skipped
        """
        progress = self._session_progress.get(session_id)
        
        if not progress:
            return False
        
        return step_id in progress.skipped_steps

    def get_completion_percentage(self, session_id: str) -> float:
        """
        Get the percentage of script completion.
        
        Args:
            session_id: Session ID
        
        Returns:
            Completion percentage (0.0 to 1.0)
        """
        progress = self._session_progress.get(session_id)
        
        if not progress:
            return 0.0
        
        script_steps = self._scripts.get(progress.script_id)
        if not script_steps:
            return 0.0
        
        total_steps = len(script_steps)
        if total_steps == 0:
            return 0.0
        
        completed_count = len(progress.completed_steps)
        return completed_count / total_steps

    def is_script_complete(self, session_id: str) -> bool:
        """
        Check if the script is complete.
        
        Args:
            session_id: Session ID
        
        Returns:
            True if script is complete
        """
        progress = self._session_progress.get(session_id)
        
        if not progress:
            return False
        
        script_steps = self._scripts.get(progress.script_id)
        if not script_steps:
            return False
        
        # Script is complete if all steps are completed or skipped
        for step in script_steps:
            if step.step_id not in progress.completed_steps and step.step_id not in progress.skipped_steps:
                return False
        
        return True

    def reset_script_progress(self, session_id: str) -> bool:
        """
        Reset script progress for a session.
        
        Args:
            session_id: Session ID
        
        Returns:
            True if progress was reset successfully
        """
        if session_id in self._session_progress:
            script_id = self._session_progress[session_id].script_id
            self._session_progress[session_id] = ScriptProgress(script_id=script_id)
            logger.debug("Script progress reset", session_id=session_id)
            return True
        
        return False

    def clear_script_progress(self, session_id: str) -> bool:
        """
        Clear script progress for a session.
        
        Args:
            session_id: Session ID
        
        Returns:
            True if progress was cleared successfully
        """
        if session_id in self._session_progress:
            del self._session_progress[session_id]
            logger.debug("Script progress cleared", session_id=session_id)
            return True
        
        return False

    def get_script_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a summary of the script progress.
        
        Args:
            session_id: Session ID
        
        Returns:
            Script summary or None if not found
        """
        progress = self._session_progress.get(session_id)
        
        if not progress:
            return None
        
        script_steps = self._scripts.get(progress.script_id)
        total_steps = len(script_steps) if script_steps else 0
        
        return {
            "script_id": progress.script_id,
            "current_step": progress.current_step,
            "completed_steps": progress.completed_steps,
            "skipped_steps": progress.skipped_steps,
            "total_steps": total_steps,
            "completion_percentage": self.get_completion_percentage(session_id),
            "is_complete": self.is_script_complete(session_id),
        }


# Global script manager instance
_script_manager: Optional[ScriptManager] = None


def get_script_manager() -> ScriptManager:
    """
    Get the global script manager instance.
    
    Returns:
        ScriptManager: The global script manager
    """
    global _script_manager
    if _script_manager is None:
        _script_manager = ScriptManager()
    return _script_manager
