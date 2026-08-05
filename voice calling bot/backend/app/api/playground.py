import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Optional

from app.database.connection import get_db
from app.models.agent import Agent
from app.services.ai_providers import ai_provider_service

router = APIRouter()


class ChatMessageSchema(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class PlaygroundChatRequest(BaseModel):
    agent_id: Optional[str] = None
    message: str
    voice_id: str = "gtts-en-us"
    llm_provider: str = "gemini"
    conversation_history: List[ChatMessageSchema] = []
    temperature: float = 0.7


@router.post("/chat")
async def playground_chat(data: PlaygroundChatRequest, db: Session = Depends(get_db)):
    """
    Playground chat endpoint - sends user message to real LLM (Gemini).
    Returns AI response text, latency, and token estimate.
    """
    start_time = time.time()

    # Load agent system prompt from DB if agent_id given
    system_prompt = "You are a helpful and friendly AI voice assistant. Keep responses under 2-3 short sentences."
    greeting_message = "Hi there! How can I help you today?"

    if data.agent_id and data.agent_id != "custom":
        try:
            agent = db.query(Agent).filter(Agent.id == data.agent_id).first()
            if agent:
                system_prompt = agent.system_prompt or system_prompt
                greeting_message = agent.greeting_message or greeting_message
        except Exception:
            pass

    # Build history as list of dicts
    history = [{"role": m.role, "content": m.content} for m in data.conversation_history]

    # Call real Gemini LLM with temperature from request
    response_text = await ai_provider_service.generate_response(
        system_prompt=system_prompt,
        script="",
        conversation_history=history,
        user_input=data.message,
        provider=data.llm_provider,
        temperature=data.temperature
    )


    elapsed_ms = int((time.time() - start_time) * 1000)
    # Rough estimate: ~1.3 tokens per word
    tokens_used = int(len(data.message.split()) * 1.3) + int(len(response_text.split()) * 1.3)
    cost_estimate = round(tokens_used * 0.000002, 5)  # ~$0.002 per 1K tokens

    return {
        "response": response_text,
        "latency_ms": elapsed_ms,
        "tokens": tokens_used,
        "cost": cost_estimate,
        "provider": data.llm_provider,
        "voice_id": data.voice_id,
    }


@router.get("/config")
async def get_playground_config():
    """Returns available real LLM and TTS providers for the playground."""
    return {
        "llm_providers": [
            {"id": "gemini", "name": "Gemini 2.5 Flash", "description": "Google Gemini - Fast & Free tier available"},
            {"id": "huggingface", "name": "Nemotron (HuggingFace)", "description": "NVIDIA Nemotron via HuggingFace API"},
        ],
        "tts_engines": [
            {"id": "gtts-en-us", "name": "gTTS - English (Free)", "engine": "gtts", "language": "en-US"},
            {"id": "gtts-hi-in", "name": "gTTS - Hindi / Hinglish (Free)", "engine": "gtts", "language": "hi-IN"},
        ]
    }
