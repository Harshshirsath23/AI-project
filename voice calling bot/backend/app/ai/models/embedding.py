from typing import Optional
from pydantic import BaseModel, Field


class EmbeddingRequest(BaseModel):
    """
    Request model for text embedding generation.
    
    This is the standardized request format that all embedding providers must accept.
    Business modules should use this model regardless of the underlying provider.
    """

    text: str = Field(..., description="Text to generate embedding for")
    model: Optional[str] = Field(
        default=None,
        description="Optional model override",
    )
    normalize: bool = Field(
        default=True,
        description="Whether to normalize the embedding vector",
    )
    encoding_format: str = Field(
        default="float",
        description="Encoding format (float or base64)",
    )


class EmbeddingResponse(BaseModel):
    """
    Response model for text embedding generation.
    
    This is the standardized response format that all embedding providers must return.
    Business modules should expect this format regardless of the underlying provider.
    """

    embedding: list[float] = Field(..., description="Embedding vector")
    dimension: int = Field(..., description="Dimension of the embedding vector")
    provider: str = Field(..., description="Provider name that generated the response")
    model_used: Optional[str] = Field(
        default=None,
        description="Model used for embedding generation",
    )
    processing_time: float = Field(
        ...,
        description="Processing time in seconds",
    )
    token_count: int = Field(
        ...,
        description="Number of tokens in the input text",
    )
