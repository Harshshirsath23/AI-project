from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database.connection import get_db
from app.models.agent import Agent, AgentVoiceProfile, AgentConfiguration

router = APIRouter()


class VoiceProfileSchema(BaseModel):
    voice_id: str = "en_US-lessac-medium"
    voice_name: str = "Piper - En-US Female (Lessac)"
    voice_gender: str = "female"
    voice_accent: str = "US"
    pitch: float = 1.0
    speed: float = 1.0


class AgentCreateSchema(BaseModel):
    name: str
    description: Optional[str] = ""
    status: str = "active"
    default_language: str = "en-US"
    llm_provider: str = "gemini"
    stt_provider: str = "faster-whisper"
    tts_provider: str = "gtts"
    system_prompt: Optional[str] = "You are a helpful AI voice assistant."
    greeting_message: Optional[str] = "Hello! How can I help you today?"
    conversation_script: Optional[str] = None
    knowledge_base_id: Optional[str] = None
    voice_profile: Optional[VoiceProfileSchema] = Field(default_factory=VoiceProfileSchema)


@router.get("")
async def list_agents(
    db: Session = Depends(get_db),
    status: Optional[str] = None
):
    """Get list of all AI agents."""
    query = db.query(Agent).filter(Agent.deleted_at.is_(None))
    if status:
        query = query.filter(Agent.status == status)
    agents = query.order_by(Agent.created_at.desc()).all()
    
    result = []
    for agent in agents:
        vp = db.query(AgentVoiceProfile).filter(AgentVoiceProfile.agent_id == agent.id).first()
        result.append({
            "id": str(agent.id),
            "name": agent.name,
            "description": agent.description,
            "status": agent.status,
            "default_language": agent.default_language,
            "llm_provider": agent.llm_provider,
            "stt_provider": agent.stt_provider,
            "tts_provider": agent.tts_provider,
            "system_prompt": agent.system_prompt,
            "greeting_message": agent.greeting_message,
            "conversation_script": agent.conversation_script,
            "knowledge_base_id": agent.knowledge_base_id if hasattr(agent, 'knowledge_base_id') else None,
            "created_at": agent.created_at.isoformat() if agent.created_at else None,
            "voice": vp.voice_name if vp else "Google gTTS Voice",
        })
    return result


@router.post("")
async def create_agent(
    data: AgentCreateSchema,
    db: Session = Depends(get_db)
):
    """Create a new AI Agent."""
    # For dev mode, use default organization UUID
    org_id = "00000000-0000-0000-0000-000000000000"
    
    # Resolve knowledge_base_id safely
    kb_id_to_save = None
    if data.knowledge_base_id:
        from app.models.knowledge_base import KnowledgeBase, KnowledgeDocument
        doc = db.query(KnowledgeDocument).filter(KnowledgeDocument.id == data.knowledge_base_id).first()
        if doc and doc.knowledge_base_id:
            kb_id_to_save = doc.knowledge_base_id
        else:
            kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == data.knowledge_base_id).first()
            if kb:
                kb_id_to_save = kb.id

    agent = Agent(
        organization_id=org_id,
        name=data.name,
        description=data.description,
        status=data.status,
        default_language=data.default_language,
        llm_provider=data.llm_provider,
        stt_provider=data.stt_provider,
        tts_provider=data.tts_provider,
        system_prompt=data.system_prompt,
        greeting_message=data.greeting_message,
        conversation_script=data.conversation_script,
        knowledge_base_id=kb_id_to_save,
    )

    db.add(agent)
    db.commit()
    db.refresh(agent)

    if data.voice_profile:
        vp = AgentVoiceProfile(
            agent_id=agent.id,
            voice_id=data.voice_profile.voice_id,
            voice_name=data.voice_profile.voice_name,
            voice_gender=data.voice_profile.voice_gender,
            voice_accent=data.voice_profile.voice_accent,
            pitch=data.voice_profile.pitch,
            speed=data.voice_profile.speed,
        )
        db.add(vp)
        db.commit()

    return {"status": "success", "agent_id": str(agent.id), "name": agent.name}


class AgentUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    greeting_message: Optional[str] = None
    conversation_script: Optional[str] = None
    knowledge_base_id: Optional[str] = None
    status: Optional[str] = None


@router.put("/{agent_id}")
async def update_agent(agent_id: str, data: AgentUpdateSchema, db: Session = Depends(get_db)):
    """Update an existing AI Agent configuration and assigned Knowledge Base script."""
    agent = db.query(Agent).filter(Agent.id == agent_id, Agent.deleted_at.is_(None)).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
        
    if data.name is not None:
        agent.name = data.name
    if data.description is not None:
        agent.description = data.description
    if data.system_prompt is not None:
        agent.system_prompt = data.system_prompt
    if data.greeting_message is not None:
        agent.greeting_message = data.greeting_message
    if data.conversation_script is not None:
        agent.conversation_script = data.conversation_script
    if data.knowledge_base_id is not None:
        kb_target_id = data.knowledge_base_id
        from app.models.knowledge_base import KnowledgeBase, KnowledgeDocument
        doc = db.query(KnowledgeDocument).filter(KnowledgeDocument.id == kb_target_id).first()
        if doc and doc.knowledge_base_id:
            agent.knowledge_base_id = doc.knowledge_base_id
        else:
            kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_target_id).first()
            if kb:
                agent.knowledge_base_id = kb.id
            else:
                agent.knowledge_base_id = None
    if data.status is not None:
        agent.status = data.status

    db.commit()
    db.refresh(agent)
    return {"status": "success", "agent_id": str(agent.id), "knowledge_base_id": agent.knowledge_base_id}



@router.get("/{agent_id}")
async def get_agent_detail(agent_id: str, db: Session = Depends(get_db)):
    """Get single AI Agent details."""
    agent = db.query(Agent).filter(Agent.id == agent_id, Agent.deleted_at.is_(None)).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
        
    vp = db.query(AgentVoiceProfile).filter(AgentVoiceProfile.agent_id == agent.id).first()
    return {
        "id": str(agent.id),
        "name": agent.name,
        "description": agent.description,
        "status": agent.status,
        "default_language": agent.default_language,
        "llm_provider": agent.llm_provider,
        "stt_provider": agent.stt_provider,
        "tts_provider": agent.tts_provider,
        "system_prompt": agent.system_prompt,
        "greeting_message": agent.greeting_message,
        "conversation_script": agent.conversation_script,
        "knowledge_base_id": agent.knowledge_base_id,
        "voice_profile": {
            "voice_id": vp.voice_id if vp else "default",
            "voice_name": vp.voice_name if vp else "Default Voice",
            "voice_gender": vp.voice_gender if vp else "female",
            "pitch": vp.pitch if vp else 1.0,
            "speed": vp.speed if vp else 1.0,
        } if vp else None
    }



@router.delete("/{agent_id}")
async def delete_agent(agent_id: str, db: Session = Depends(get_db)):
    """Soft delete an AI Agent."""
    from datetime import datetime, UTC
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if agent:
        agent.deleted_at = datetime.now(UTC)
        db.commit()
    return {"status": "success"}

