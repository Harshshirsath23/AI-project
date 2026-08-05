from fastapi import APIRouter

router = APIRouter()

AVAILABLE_VOICES = [
    {
        "id": "gtts-en-us",
        "name": "gTTS - Google TTS (English Free)",
        "engine": "gtts",
        "gender": "female",
        "language": "en-US",
        "sample_url": "",
    },
    {
        "id": "gtts-hi-in",
        "name": "gTTS - Google TTS (Hindi / Hinglish Free)",
        "engine": "gtts",
        "gender": "female",
        "language": "hi-IN",
        "sample_url": "",
    },
    {
        "id": "piper-lessac-en",

        "name": "Piper - Lessac (En-US Female)",
        "engine": "piper",
        "gender": "female",
        "language": "en-US",
        "sample_url": "",
    },
    {
        "id": "piper-ryan-en",
        "name": "Piper - Ryan (En-US Male)",
        "engine": "piper",
        "gender": "male",
        "language": "en-US",
        "sample_url": "",
    },
    {
        "id": "elevenlabs-rachel",
        "name": "ElevenLabs - Rachel (Friendly Sales)",
        "engine": "elevenlabs",
        "gender": "female",
        "language": "en-US",
        "sample_url": "",
    },
    {
        "id": "elevenlabs-adam",
        "name": "ElevenLabs - Adam (Professional Male)",
        "engine": "elevenlabs",
        "gender": "male",
        "language": "en-US",
        "sample_url": "",
    },
    {
        "id": "sarvam-vidya-hi",
        "name": "Sarvam AI - Vidya (Hindi / Hinglish Female)",
        "engine": "sarvam",
        "gender": "female",
        "language": "hi-IN",
        "sample_url": "",
    },
    {
        "id": "sarvam-rahul-hi",
        "name": "Sarvam AI - Rahul (Hindi / Hinglish Male)",
        "engine": "sarvam",
        "gender": "male",
        "language": "hi-IN",
        "sample_url": "",
    },
    {
        "id": "parler-tts-expressive",
        "name": "Parler-TTS - Natural Expressive (Hugging Face)",
        "engine": "huggingface",
        "gender": "female",
        "language": "en-US",
        "sample_url": "",
    },
]


@router.get("")
async def list_available_voices():
    """Get list of available TTS voices for agent voice selection."""
    return AVAILABLE_VOICES
