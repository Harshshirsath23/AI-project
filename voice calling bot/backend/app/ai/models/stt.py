from typing import Optional
from pydantic import BaseModel, Field


class STTRequest(BaseModel):
    """
    Request model for Speech-to-Text transcription.
    
    This is the standardized request format that all STT providers must accept.
    Business modules should use this model regardless of the underlying provider.
    """

    audio_data: bytes = Field(..., description="Raw audio data bytes")
    audio_format: str = Field(
        default="wav",
        description="Audio format (wav, mp3, ogg, etc.)",
    )
    sample_rate: int = Field(
        default=16000,
        description="Audio sample rate in Hz",
    )
    language: Optional[str] = Field(
        default="en",
        description="Language code (e.g., 'en', 'hi', 'es')",
    )
    model: Optional[str] = Field(
        default=None,
        description="Optional model override",
    )
    enable_timestamps: bool = Field(
        default=False,
        description="Whether to include word-level timestamps",
    )
    enable_diarization: bool = Field(
        default=False,
        description="Whether to enable speaker diarization",
    )
    num_speakers: Optional[int] = Field(
        default=None,
        description="Number of speakers for diarization",
    )
    vocabulary: Optional[list[str]] = Field(
        default=None,
        description="Optional vocabulary list for better recognition",
    )
    profanity_filter: bool = Field(
        default=False,
        description="Whether to filter profanity",
    )


class WordTimestamp(BaseModel):
    """Word-level timestamp for transcription."""

    word: str
    start_time: float = Field(..., description="Start time in seconds")
    end_time: float = Field(..., description="End time in seconds")
    confidence: float = Field(..., ge=0.0, le=1.0)


class SpeakerSegment(BaseModel):
    """Speaker segment for diarization."""

    speaker_id: str
    start_time: float = Field(..., description="Start time in seconds")
    end_time: float = Field(..., description="End time in seconds")
    text: str


class STTResponse(BaseModel):
    """
    Response model for Speech-to-Text transcription.
    
    This is the standardized response format that all STT providers must return.
    Business modules should expect this format regardless of the underlying provider.
    """

    text: str = Field(..., description="Transcribed text")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall confidence score")
    language: str = Field(..., description="Detected language")
    duration: float = Field(..., description="Audio duration in seconds")
    word_timestamps: Optional[list[WordTimestamp]] = Field(
        default=None,
        description="Word-level timestamps if enabled",
    )
    speaker_segments: Optional[list[SpeakerSegment]] = Field(
        default=None,
        description="Speaker segments if diarization enabled",
    )
    provider: str = Field(..., description="Provider name that generated the response")
    model_used: Optional[str] = Field(
        default=None,
        description="Model used for transcription",
    )
    processing_time: float = Field(
        ...,
        description="Processing time in seconds",
    )


class STTStreamingChunk(BaseModel):
    """
    Streaming chunk for real-time STT transcription.
    
    This model represents partial transcription results during streaming.
    """

    text: str = Field(..., description="Partial transcribed text")
    is_final: bool = Field(
        default=False,
        description="Whether this chunk is final (no more updates expected)",
    )
    start_time: Optional[float] = Field(
        default=None,
        description="Start time of this chunk in seconds",
    )
    end_time: Optional[float] = Field(
        default=None,
        description="End time of this chunk in seconds",
    )
    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Confidence score for this chunk",
    )
