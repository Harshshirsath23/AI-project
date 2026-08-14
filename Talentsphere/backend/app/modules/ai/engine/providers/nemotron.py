import structlog
import json
from typing import Any, Dict, Optional, Type, TypeVar
from pydantic import BaseModel
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage

from app.core.config import settings
from app.modules.ai.engine.providers.base import BaseLLMProvider
from app.core.observability import trace_span

logger = structlog.get_logger(__name__)

T = TypeVar("T", bound=BaseModel)


class NemotronProvider(BaseLLMProvider):
    """
    NVIDIA Nemotron 3 Ultra Provider implementation for TalentSphere.
    
    Supports:
    - High-reasoning structured generation & decision intelligence
    - OpenAI-compatible NVIDIA NIM endpoint integration (https://integrate.api.nvidia.com/v1)
    - Non-blocking async execution
    - LangSmith telemetry tracing
    - Graceful fallback to MockLLM when external credentials or endpoints are unconfigured
    """

    def __init__(
        self,
        model_name: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None
    ):
        self.model_name = model_name or getattr(settings, "NEMOTRON_MODEL", "nvidia/nemotron-3-ultra")
        self.temperature = temperature if temperature is not None else getattr(settings, "NEMOTRON_TEMPERATURE", 0.2)
        self.max_tokens = max_tokens or getattr(settings, "NEMOTRON_MAX_TOKENS", 4096)
        self.timeout = timeout or getattr(settings, "NEMOTRON_TIMEOUT_SECONDS", 30)
        self.max_retries = max_retries or getattr(settings, "NEMOTRON_MAX_RETRIES", 3)
        self.base_url = getattr(settings, "NEMOTRON_BASE_URL", "https://integrate.api.nvidia.com/v1")
        self.api_key = getattr(settings, "NEMOTRON_API_KEY", None)

    def get_model(self) -> BaseChatModel:
        """Instantiate ChatModel instance connected to NVIDIA Nemotron NIM endpoint."""
        if self.api_key and self.api_key.strip():
            try:
                from langchain_openai import ChatOpenAI
                return ChatOpenAI(
                    model=self.model_name,
                    openai_api_key=self.api_key,
                    openai_api_base=self.base_url,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    request_timeout=self.timeout,
                    max_retries=self.max_retries
                )
            except Exception as exc:
                logger.info("Nemotron ChatOpenAI initialization fallback to MockLLM", error=str(exc))

        from app.modules.ai.engine.llm import MockLLM
        return MockLLM(provider_name="NemotronProvider", model_name=self.model_name)

    async def generate_response(
        self,
        system_prompt: str,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate textual reasoning response using NVIDIA Nemotron 3 Ultra."""
        model = self.get_model()
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ]

        async with trace_span(
            name="Nemotron Reasoner Call",
            run_type="llm",
            inputs={"system_prompt": system_prompt, "user_input": user_input[:200]},
            metadata={"model": self.model_name, "provider": "Nemotron"}
        ) as span:
            try:
                res = await model.ainvoke(messages)
                output_text = str(res.content)
                span.end(outputs={"response": output_text[:200]})
                return output_text
            except Exception as exc:
                logger.warning("Nemotron inference call failed, using fallback", error=str(exc))
                from app.modules.ai.engine.llm import MockLLM
                fallback = MockLLM(provider_name="NemotronProvider", model_name=self.model_name)
                res = await fallback.ainvoke(messages)
                output_text = str(res.content)
                span.end(outputs={"response": output_text[:200]}, error=exc)
                return output_text

    async def generate_structured_output(
        self,
        schema: Type[T],
        system_prompt: str,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> T:
        """
        Generate structured output adhering to Pydantic schema using Nemotron 3 Ultra.
        
        Implements multi-tier fallback strategy:
        1. Try Nemotron with structured output
        2. Try Nemotron with JSON mode and manual parsing
        3. Try OpenAI GPT-4 with structured output
        4. Fallback to mock structured generation
        
        Args:
            schema: Pydantic schema for structured output
            system_prompt: System prompt for the LLM
            user_input: User input prompt
            context: Optional context data for fallback generation
            
        Returns:
            Instance of the specified Pydantic schema
        """
        model = self.get_model()
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ]

        async with trace_span(
            name=f"Nemotron Structured Output ({schema.__name__})",
            run_type="llm",
            inputs={"schema": schema.__name__, "user_input": user_input[:200]},
            metadata={"model": self.model_name, "provider": "Nemotron"}
        ) as span:
            from app.modules.ai.engine.llm import MockLLM, LLMService
            
            # Tier 1: Try native structured output
            if hasattr(model, "with_structured_output") and not isinstance(model, MockLLM):
                try:
                    structured_llm = model.with_structured_output(schema)
                    res = await structured_llm.ainvoke(messages)
                    if isinstance(res, schema):
                        logger.info("Nemotron structured output successful", schema=schema.__name__)
                        span.end(outputs=res.model_dump())
                        return res
                except Exception as exc:
                    logger.warning("Nemotron structured output failed, trying JSON mode", error=str(exc))
            
            # Tier 2: Try JSON mode with manual parsing
            if not isinstance(model, MockLLM):
                try:
                    json_schema = schema.model_json_schema()
                    json_prompt = f"{system_prompt}\n\nRespond with valid JSON matching this schema:\n{json.dumps(json_schema)}\n\nUser input: {user_input}"
                    
                    json_messages = [
                        SystemMessage(content=json_prompt),
                        HumanMessage(content=user_input)
                    ]
                    
                    res = await model.ainvoke(json_messages)
                    json_text = str(res.content)
                    
                    # Parse JSON response
                    import json
                    parsed_data = json.loads(json_text)
                    structured_res = schema(**parsed_data)
                    
                    logger.info("Nemotron JSON mode successful", schema=schema.__name__)
                    span.end(outputs=structured_res.model_dump())
                    return structured_res
                    
                except Exception as exc:
                    logger.warning("Nemotron JSON mode failed, trying OpenAI fallback", error=str(exc))
            
            # Tier 3: Try OpenAI fallback
            try:
                from langchain_openai import ChatOpenAI
                openai_key = getattr(settings, "OPENAI_API_KEY", None)
                if openai_key:
                    openai_model = ChatOpenAI(
                        model="gpt-4",
                        temperature=self.temperature,
                        api_key=openai_key
                    )
                    
                    if hasattr(openai_model, "with_structured_output"):
                        structured_llm = openai_model.with_structured_output(schema)
                        res = await structured_llm.ainvoke(messages)
                        if isinstance(res, schema):
                            logger.info("OpenAI fallback successful", schema=schema.__name__)
                            span.end(outputs=res.model_dump())
                            return res
            except Exception as exc:
                logger.warning("OpenAI fallback failed, using mock generation", error=str(exc))

            # Tier 4: Fallback mock generator
            service = LLMService(model_name=self.model_name)
            mock_res = service._generate_mock_structured_output(schema, user_input, context)
            logger.info("Mock structured output used", schema=schema.__name__)
            span.end(outputs=mock_res.model_dump())
            return mock_res
