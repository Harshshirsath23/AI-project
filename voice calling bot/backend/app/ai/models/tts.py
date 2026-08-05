from typing import Optional
from pydantic import BaseModel, Field


class TTSRequest(BaseModel):
    """
    Request model for Text-to-Speech synthesis.
    
    This is the standardized request format that all TTS providers must accept.
    Business modules should use this model regardless of the underlying provider.
    """

    text: str = Field(..., description="Text to synthesize to speech")
    voice_id: str = Field(..., description="Voice ID to use for synthesis")
    language: Optional[str] = Field(
        default="en",
        description="Language code (e.g., 'en', 'hi', 'es')",
    )
    model: Optional[str] = Field(
        default=None,
        description="Optional model override",
    )
    output_format: str = Field(
        default="wav",
        description="Output audio format (wav, mp3, ogg, etc.)",
    )
    sample_rate: int = Field(
        default=24000,
        description="Output sample rate in Hz",
    )
    speed: float = Field(
        default=1.0,
        ge=0.5,
        le=2.0,
        description="Speech speed multiplier",
    )
    pitch: float = Field(
        default=1.0,
        ge=0.5,
        le=2.0,
        description="Pitch multiplier",
    )
    volume: float = Field(
        default=1.0,
        ge=0.0,
        le=2.0,
        description="Volume multiplier",
    )
    enable_ssml: bool = Field(
        default=False,
        description="Whether to parse SSML tags in text",
    )
    enable_pronunciation: bool = Field(
        default=False,
        description="Whether to enable pronunciation hints",
    )


class TTSResponse(BaseModel):
    """
    Response model for Text-to-Speech synthesis.
    
    This is the standardized response format that all TTS providers must return.
    Business modules should expect this format regardless of the underlying provider.
    """

    audio_data: bytes = Field(..., description="Synthesized audio data bytes")
    audio_format: str = Field(..., description="Audio format of the output")
    sample_rate: int = Field(..., description="Sample rate of the audio")
    duration: float = Field(..., description="Audio duration in seconds")
    voice_id: str = Field(..., description="Voice ID used for synthesis")
    language: str = Field(..., description="Language of the synthesized speech")
    provider: str = Field(..., description="Provider name that generated the response")
    model_used: Optional[str] = Field(
        default=None,
        description="Model used for synthesis",
    )
    processing_time: float = Field(
        ...,
        description="Processing time in seconds",
    )
    characters_count: int = Field(
        ...,
        description="Number of characters synthesized",
    )


class TTSStreamingChunk(BaseModel):
    """
    Streaming chunk for real-time TTS synthesis.
    
    This model represents partial audio data during streaming synthesis.
    """

    audio_data: bytes = Field(..., description="Partial audio data bytes")
    chunk_index: int = Field(..., description="Index of this chunk")
    is_final: bool = Field(
        default=False,
        description="Whether this is the final chunk",
    )
    duration: float = Field(..., description="Duration of this chunk in seconds")
