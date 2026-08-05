from typing import Optional, Dict, Any
from dataclasses import dataclass, field

from app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class PersonalityDefinition:
    """Definition of an agent personality."""

    id: str
    name: str
    description: str
    traits: Dict[str, Any] = field(default_factory=dict)
    system_prompt_template: Optional[str] = None
    response_style: str = "professional"
    metadata: Dict[str, Any] = field(default_factory=dict)


class PersonalityManager:
    """
    Manager for agent personalities.
    
    This manager handles personality definitions and their application to
    conversations. Personalities influence how the AI agent responds,
    including tone, style, and behavior patterns.
    
    Supported personalities include:
    - Professional
    - Friendly
    - Sales
    - Technical
    - Support
    - Empathetic
    - Corporate
    
    The personality manager provides the framework for personality application.
    Actual LLM integration will use these personalities to influence prompt generation.
    """

    def __init__(self):
        """Initialize the personality manager."""
        self._personalities: Dict[str, PersonalityDefinition] = {}
        self._session_personalities: Dict[str, str] = {}

        # Initialize default personalities
        self._initialize_default_personalities()

    def _initialize_default_personalities(self) -> None:
        """Initialize default personality definitions."""
        default_personalities = [
            PersonalityDefinition(
                id="professional",
                name="Professional",
                description="Professional and formal communication style",
                traits={
                    "tone": "formal",
                    "politeness": "high",
                    "verbosity": "moderate",
                    "empathy": "moderate",
                },
                response_style="professional",
            ),
            PersonalityDefinition(
                id="friendly",
                name="Friendly",
                description="Warm and approachable communication style",
                traits={
                    "tone": "casual",
                    "politeness": "high",
                    "verbosity": "moderate",
                    "empathy": "high",
                },
                response_style="friendly",
            ),
            PersonalityDefinition(
                id="sales",
                name="Sales",
                description="Persuasive and goal-oriented communication style",
                traits={
                    "tone": "enthusiastic",
                    "politeness": "high",
                    "verbosity": "high",
                    "empathy": "moderate",
                    "persuasion": "high",
                },
                response_style="sales",
            ),
            PersonalityDefinition(
                id="technical",
                name="Technical",
                description="Precise and detail-oriented communication style",
                traits={
                    "tone": "neutral",
                    "politeness": "moderate",
                    "verbosity": "high",
                    "empathy": "low",
                    "precision": "high",
                },
                response_style="technical",
            ),
            PersonalityDefinition(
                id="support",
                name="Support",
                description="Helpful and patient communication style",
                traits={
                    "tone": "patient",
                    "politeness": "high",
                    "verbosity": "moderate",
                    "empathy": "high",
                    "helpfulness": "high",
                },
                response_style="support",
            ),
            PersonalityDefinition(
                id="empathetic",
                name="Empathetic",
                description="Understanding and emotionally intelligent communication style",
                traits={
                    "tone": "warm",
                    "politeness": "high",
                    "verbosity": "moderate",
                    "empathy": "very_high",
                },
                response_style="empathetic",
            ),
            PersonalityDefinition(
                id="corporate",
                name="Corporate",
                description="Business-focused and formal communication style",
                traits={
                    "tone": "formal",
                    "politeness": "high",
                    "verbosity": "moderate",
                    "empathy": "low",
                    "business_focus": "high",
                },
                response_style="corporate",
            ),
        ]

        for personality in default_personalities:
            self._personalities[personality.id] = personality

        logger.info("Default personalities initialized", count=len(default_personalities))

    def register_personality(self, personality: PersonalityDefinition) -> None:
        """
        Register a new personality definition.
        
        Args:
            personality: Personality definition to register
        """
        self._personalities[personality.id] = personality
        logger.info("Personality registered", personality_id=personality.id, name=personality.name)

    def get_personality(self, personality_id: str) -> Optional[PersonalityDefinition]:
        """
        Get a personality definition by ID.
        
        Args:
            personality_id: Personality ID
        
        Returns:
            Personality definition or None if not found
        """
        return self._personalities.get(personality_id)

    def list_personalities(self) -> list[PersonalityDefinition]:
        """
        List all registered personalities.
        
        Returns:
            List of personality definitions
        """
        return list(self._personalities.values())

    def assign_personality(
        self,
        session_id: str,
        personality_id: str,
    ) -> bool:
        """
        Assign a personality to a session.
        
        Args:
            session_id: Session ID
            personality_id: Personality ID
        
        Returns:
            True if personality was assigned successfully
        """
        if personality_id not in self._personalities:
            logger.warning("Personality not found", personality_id=personality_id)
            return False
        
        self._session_personalities[session_id] = personality_id
        
        logger.info(
            "Personality assigned",
            session_id=session_id,
            personality_id=personality_id,
        )
        
        return True

    def get_session_personality(
        self,
        session_id: str,
    ) -> Optional[PersonalityDefinition]:
        """
        Get the personality assigned to a session.
        
        Args:
            session_id: Session ID
        
        Returns:
            Personality definition or None if not assigned
        """
        personality_id = self._session_personalities.get(session_id)
        
        if not personality_id:
            return None
        
        return self._personalities.get(personality_id)

    def remove_session_personality(self, session_id: str) -> bool:
        """
        Remove the personality assignment from a session.
        
        Args:
            session_id: Session ID
        
        Returns:
            True if personality was removed successfully
        """
        if session_id in self._session_personalities:
            del self._session_personalities[session_id]
            logger.debug("Session personality removed", session_id=session_id)
            return True
        
        return False

    def get_personality_traits(
        self,
        personality_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Get the traits for a personality.
        
        Args:
            personality_id: Personality ID
        
        Returns:
            Personality traits or None if not found
        """
        personality = self._personalities.get(personality_id)
        
        if not personality:
            return None
        
        return personality.traits.copy()

    def get_session_traits(self, session_id: str) -> Dict[str, Any]:
        """
        Get the traits for a session's assigned personality.
        
        Args:
            session_id: Session ID
        
        Returns:
            Personality traits or empty dict if not assigned
        """
        personality = self.get_session_personality(session_id)
        
        if not personality:
            return {}
        
        return personality.traits.copy()

    def get_system_prompt_template(
        self,
        personality_id: str,
    ) -> Optional[str]:
        """
        Get the system prompt template for a personality.
        
        Args:
            personality_id: Personality ID
        
        Returns:
            System prompt template or None if not found
        """
        personality = self._personalities.get(personality_id)
        
        if not personality:
            return None
        
        return personality.system_prompt_template

    def get_session_system_prompt_template(
        self,
        session_id: str,
    ) -> Optional[str]:
        """
        Get the system prompt template for a session's assigned personality.
        
        Args:
            session_id: Session ID
        
        Returns:
            System prompt template or None if not assigned
        """
        personality = self.get_session_personality(session_id)
        
        if not personality:
            return None
        
        return personality.system_prompt_template

    def get_response_style(
        self,
        personality_id: str,
    ) -> Optional[str]:
        """
        Get the response style for a personality.
        
        Args:
            personality_id: Personality ID
        
        Returns:
            Response style or None if not found
        """
        personality = self._personalities.get(personality_id)
        
        if not personality:
            return None
        
        return personality.response_style

    def get_session_response_style(self, session_id: str) -> Optional[str]:
        """
        Get the response style for a session's assigned personality.
        
        Args:
            session_id: Session ID
        
        Returns:
            Response style or None if not assigned
        """
        personality = self.get_session_personality(session_id)
        
        if not personality:
            return None
        
        return personality.response_style

    def update_personality(
        self,
        personality_id: str,
        traits: Optional[Dict[str, Any]] = None,
        system_prompt_template: Optional[str] = None,
        response_style: Optional[str] = None,
    ) -> bool:
        """
        Update an existing personality definition.
        
        Args:
            personality_id: Personality ID
            traits: Updated traits
            system_prompt_template: Updated system prompt template
            response_style: Updated response style
        
        Returns:
            True if personality was updated successfully
        """
        personality = self._personalities.get(personality_id)
        
        if not personality:
            return False
        
        if traits is not None:
            personality.traits.update(traits)
        
        if system_prompt_template is not None:
            personality.system_prompt_template = system_prompt_template
        
        if response_style is not None:
            personality.response_style = response_style
        
        logger.info("Personality updated", personality_id=personality_id)
        
        return True

    def delete_personality(self, personality_id: str) -> bool:
        """
        Delete a personality definition.
        
        Args:
            personality_id: Personality ID
        
        Returns:
            True if personality was deleted successfully
        """
        if personality_id in self._personalities:
            del self._personalities[personality_id]
            logger.info("Personality deleted", personality_id=personality_id)
            return True
        
        return False

    def clear_session_assignment(self, session_id: str) -> None:
        """
        Clear personality assignment for a session.
        
        Args:
            session_id: Session ID
        """
        if session_id in self._session_personalities:
            del self._session_personalities[session_id]
            logger.debug("Session personality cleared", session_id=session_id)


# Global personality manager instance
_personality_manager: Optional[PersonalityManager] = None


def get_personality_manager() -> PersonalityManager:
    """
    Get the global personality manager instance.
    
    Returns:
        PersonalityManager: The global personality manager
    """
    global _personality_manager
    if _personality_manager is None:
        _personality_manager = PersonalityManager()
    return _personality_manager
