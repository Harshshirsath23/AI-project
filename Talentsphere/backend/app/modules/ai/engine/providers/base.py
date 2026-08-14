from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type, TypeVar
from pydantic import BaseModel
from langchain_core.language_models.chat_models import BaseChatModel

T = TypeVar("T", bound=BaseModel)


class BaseLLMProvider(ABC):
    """Abstract Base LLM Provider class for TalentSphere AI Architecture."""

    @abstractmethod
    def get_model() -> BaseChatModel:
        """Instantiate and return ChatModel instance."""
        pass

    @abstractmethod
    async def generate_response(
        self,
        system_prompt: str,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate textual response from LLM."""
        pass

    @abstractmethod
    async def generate_structured_output(
        self,
        schema: Type[T],
        system_prompt: str,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> T:
        """Generate structured response adhering to Pydantic schema."""
        pass
