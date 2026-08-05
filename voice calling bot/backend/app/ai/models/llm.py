from typing import Optional, Any
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Chat message for LLM conversation."""

    role: str = Field(..., description="Message role (system, user, assistant)")
    content: str = Field(..., description="Message content")
    name: Optional[str] = Field(default=None, description="Optional name for the message")


class FunctionCall(BaseModel):
    """Function call for tool/function calling."""

    name: str = Field(..., description="Function name to call")
    arguments: dict = Field(..., description="Function arguments")


class ToolDefinition(BaseModel):
    """Tool/function definition for LLM."""

    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    parameters: dict = Field(..., description="Tool parameters schema")


class LLMChatRequest(BaseModel):
    """
    Request model for LLM chat completion.
    
    This is the standardized request format that all LLM providers must accept.
    Business modules should use this model regardless of the underlying provider.
    """

    messages: list[ChatMessage] = Field(..., description="Conversation messages")
    model: Optional[str] = Field(
        default=None,
        description="Optional model override",
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Sampling temperature",
    )
    max_tokens: Optional[int] = Field(
        default=None,
        description="Maximum tokens to generate",
    )
    top_p: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Nucleus sampling parameter",
    )
    top_k: Optional[int] = Field(
        default=None,
        description="Top-k sampling parameter",
    )
    frequency_penalty: float = Field(
        default=0.0,
        ge=-2.0,
        le=2.0,
        description="Frequency penalty",
    )
    presence_penalty: float = Field(
        default=0.0,
        ge=-2.0,
        le=2.0,
        description="Presence penalty",
    )
    stop_sequences: Optional[list[str]] = Field(
        default=None,
        description="Stop sequences",
    )
    tools: Optional[list[ToolDefinition]] = Field(
        default=None,
        description="Available tools for function calling",
    )
    tool_choice: Optional[str] = Field(
        default=None,
        description="Tool choice (auto, none, or specific tool name)",
    )
    enable_streaming: bool = Field(
        default=False,
        description="Whether to enable streaming (for streaming endpoint)",
    )


class LLMChatResponse(BaseModel):
    """
    Response model for LLM chat completion.
    
    This is the standardized response format that all LLM providers must return.
    Business modules should expect this format regardless of the underlying provider.
    """

    message: ChatMessage = Field(..., description="Generated message")
    finish_reason: str = Field(..., description="Reason for completion (stop, length, tool_calls)")
    provider: str = Field(..., description="Provider name that generated the response")
    model_used: Optional[str] = Field(
        default=None,
        description="Model used for generation",
    )
    processing_time: float = Field(
        ...,
        description="Processing time in seconds",
    )
    prompt_tokens: int = Field(..., description="Number of tokens in prompt")
    completion_tokens: int = Field(..., description="Number of tokens generated")
    total_tokens: int = Field(..., description="Total tokens used")
    tool_calls: Optional[list[FunctionCall]] = Field(
        default=None,
        description="Tool calls made by the model",
    )


class LLMCompletionRequest(BaseModel):
    """
    Request model for LLM text completion.
    
    This is the standardized request format for legacy text completion.
    Business modules should prefer LLMChatRequest for new implementations.
    """

    prompt: str = Field(..., description="Text prompt for completion")
    model: Optional[str] = Field(
        default=None,
        description="Optional model override",
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Sampling temperature",
    )
    max_tokens: Optional[int] = Field(
        default=None,
        description="Maximum tokens to generate",
    )
    top_p: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Nucleus sampling parameter",
    )
    frequency_penalty: float = Field(
        default=0.0,
        ge=-2.0,
        le=2.0,
        description="Frequency penalty",
    )
    presence_penalty: float = Field(
        default=0.0,
        ge=-2.0,
        le=2.0,
        description="Presence penalty",
    )
    stop_sequences: Optional[list[str]] = Field(
        default=None,
        description="Stop sequences",
    )
    enable_streaming: bool = Field(
        default=False,
        description="Whether to enable streaming (for streaming endpoint)",
    )


class LLMCompletionResponse(BaseModel):
    """
    Response model for LLM text completion.
    
    This is the standardized response format for legacy text completion.
    Business modules should prefer LLMChatResponse for new implementations.
    """

    text: str = Field(..., description="Generated text")
    finish_reason: str = Field(..., description="Reason for completion")
    provider: str = Field(..., description="Provider name that generated the response")
    model_used: Optional[str] = Field(
        default=None,
        description="Model used for generation",
    )
    processing_time: float = Field(
        ...,
        description="Processing time in seconds",
    )
    prompt_tokens: int = Field(..., description="Number of tokens in prompt")
    completion_tokens: int = Field(..., description="Number of tokens generated")
    total_tokens: int = Field(..., description="Total tokens used")


class LLMStreamingChunk(BaseModel):
    """
    Streaming chunk for real-time LLM generation.
    
    This model represents partial text during streaming generation.
    """

    content: str = Field(..., description="Partial content")
    is_final: bool = Field(
        default=False,
        description="Whether this is the final chunk",
    )
    finish_reason: Optional[str] = Field(
        default=None,
        description="Reason for completion (only in final chunk)",
    )
    chunk_index: int = Field(..., description="Index of this chunk")
