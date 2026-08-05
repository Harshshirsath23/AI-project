import logging
from typing import List, Dict, Any, Tuple, Optional
from app.services.ai_providers import ai_provider_service
from app.services.audio_utils import calculate_audio_energy

logger = logging.getLogger(__name__)

# Energy threshold for Voice Activity Detection (VAD) interruption
VAD_INTERRUPT_THRESHOLD = 1500.0


class ConversationService:
    """Manages the lifecycle, memory, and LLM orchestration of a live call session."""

    def __init__(self):
        self.active_sessions: Dict[str, Dict[str, Any]] = {}

    def get_or_create_session(self, call_id: str) -> Dict[str, Any]:
        if call_id not in self.active_sessions:
            import uuid
            system_prompt = "You are Sarah, a friendly and energetic Sales SDR for Voxera."
            greeting = "Hi! This is Sarah from Voxera AI. Am I catching you at a bad time?"
            agent_name = "Sarah"
            lead_name = "there"
            script_text = ""

            # Query database to load real Agent, Lead, and Knowledge Base Script
            try:
                from app.database.connection import SessionLocal
                from app.models.call import Call
                from app.models.agent import Agent
                from app.models.lead import Lead
                from app.models.knowledge_base import KnowledgeDocument

                with SessionLocal() as db:
                    call = None
                    if call_id and call_id != "default":
                        try:
                            call_uuid = uuid.UUID(call_id)
                            call = db.query(Call).filter(Call.id == call_uuid).first()
                        except Exception:
                            pass
                    if not call:
                        call = db.query(Call).order_by(Call.created_at.desc()).first()




                    if call:
                        target_agent_id = call.agent_id
                        if target_agent_id:
                            agent = db.query(Agent).filter(Agent.id == target_agent_id).first()
                        else:
                            agent = db.query(Agent).first()

                        if agent:
                            system_prompt = agent.system_prompt or system_prompt
                            greeting = agent.greeting_message or greeting
                            agent_name = agent.name
                            if agent.conversation_script:
                                script_text = agent.conversation_script

                        # Look up lead by lead_id first, fallback to to_number
                        lead = None
                        if hasattr(call, 'lead_id') and call.lead_id:
                            lead = db.query(Lead).filter(Lead.id == call.lead_id).first()
                        if not lead:
                            lead = db.query(Lead).filter(Lead.phone_number == call.to_number).order_by(Lead.updated_at.desc(), Lead.created_at.desc()).first()
                        if lead and lead.name:
                            lead_name = lead.name


                    # Load script from Agent's assigned Knowledge Base documents in DB
                    kb_id = agent.knowledge_base_id if (agent and hasattr(agent, 'knowledge_base_id') and agent.knowledge_base_id) else None
                    if kb_id:
                        try:
                            kb_uuid = uuid.UUID(str(kb_id))
                            kb_docs = db.query(KnowledgeDocument).filter(
                                (KnowledgeDocument.id == kb_uuid) | (KnowledgeDocument.knowledge_base_id == kb_uuid)
                            ).order_by(KnowledgeDocument.created_at.desc()).all()
                        except Exception:
                            kb_docs = db.query(KnowledgeDocument).filter(
                                (KnowledgeDocument.id == str(kb_id)) | (KnowledgeDocument.knowledge_base_id == str(kb_id))
                            ).order_by(KnowledgeDocument.created_at.desc()).all()
                    else:
                        kb_docs = db.query(KnowledgeDocument).order_by(KnowledgeDocument.created_at.desc()).all()

                    doc_scripts = [d.meta_data.strip() for d in kb_docs if d.meta_data and d.meta_data.strip()]
                    if doc_scripts:
                        script_text += "\n\n" + "\n---\n".join(doc_scripts)

                    
                    logger.info(f"Loaded Call SID {call_id}: Agent={agent_name}, Lead={lead_name}, KB_ID={kb_id}, Script length={len(script_text)}")


            except Exception as e:
                logger.warning(f"Could not load DB session for Call SID {call_id}: {e}")

            self.active_sessions[call_id] = {
                "history": [],
                "stage_index": 0,
                "is_speaking": False,
                "audio_buffer": bytearray(),
                "silence_counter": 0,
                "system_prompt": system_prompt,
                "greeting": greeting,
                "agent_name": agent_name,
                "lead_name": lead_name,
                "script_text": script_text,
            }
        return self.active_sessions[call_id]

    def search_knowledge_base(self, user_text: str) -> str:
        """
        RAG Knowledge Base Lookup:
        Queries uploaded KnowledgeDocument extracted text scripts from PostgreSQL.
        """
        try:
            from app.database.connection import SessionLocal
            from app.models.knowledge_base import KnowledgeDocument

            with SessionLocal() as db:
                kb_docs = db.query(KnowledgeDocument).all()
                extracted_texts = []
                for doc in kb_docs:
                    if doc.meta_data:
                        extracted_texts.append(f"--- Script Document: {doc.title} ---\n{doc.meta_data}")

                if extracted_texts:
                    return "\n\n".join(extracted_texts)
        except Exception as e:
            logger.warning(f"RAG Knowledge Base lookup skipped: {e}")

        return ""

    async def process_streaming_audio(
        self, 
        call_id: str, 
        audio_chunk: bytes
    ) -> Tuple[Optional[bytes], bool]:
        """
        Processes an incoming streaming mu-law audio chunk from Twilio.
        Returns (audio_to_send_back, should_interrupt).
        """
        session = self.get_or_create_session(call_id)
        
        # 1. Voice Activity Detection (VAD) & Barge-in Interruption
        audio_energy = calculate_audio_energy(audio_chunk)
        should_interrupt = False

        # Only trigger barge-in if NOT during initial greeting setup
        if session["is_speaking"] and not session.get("is_initial_greeting", False) and audio_energy > VAD_INTERRUPT_THRESHOLD:
            should_interrupt = True
            session["is_speaking"] = False
            logger.info(f"Barge-in / Interruption detected for Call SID {call_id} (Energy: {audio_energy:.1f})")


        # Accumulate audio buffer
        session["audio_buffer"].extend(audio_chunk)

        # Process complete audio turn (~1 second of 8kHz mu-law audio = 8000 bytes)
        if len(session["audio_buffer"]) >= 8000:
            buffer_data = bytes(session["audio_buffer"])
            session["audio_buffer"].clear()

            user_text = await ai_provider_service.transcribe_audio(buffer_data)

            if user_text and user_text.strip():
                logger.info(f"Call {call_id} User Said: '{user_text}'")
                session["history"].append({"role": "user", "content": user_text})
                
                # Perform RAG lookup for script grounding
                kb_script = self.search_knowledge_base(user_text)

                ai_response_text = await ai_provider_service.generate_response(
                    system_prompt=session["system_prompt"],
                    script=f"{kb_script}\nTarget customer name is {session['lead_name']}.",
                    conversation_history=session["history"],
                    user_input=user_text
                )
                
                logger.info(f"Call {call_id} Agent Response: '{ai_response_text}'")
                session["history"].append({"role": "assistant", "content": ai_response_text})
                session["is_speaking"] = True
                
                ai_audio_bytes = await ai_provider_service.generate_speech(ai_response_text)
                return ai_audio_bytes, should_interrupt

        return None, should_interrupt

    async def generate_next_script_turn(self, call_id: str, user_speech: str) -> str:
        """
        Dynamic Agent Knowledge Base Script Engine:
        Executes conversation using the exact script document assigned to the agent in PostgreSQL.
        Parses uploaded KB documents dynamically into turn-by-turn conversation steps.
        """
        session = self.get_or_create_session(call_id)
        session["stage_index"] += 1
        stage = session["stage_index"]
        lead = session["lead_name"]
        agent_name = session["agent_name"]

        # 1. Fetch assigned Knowledge Base script text
        assigned_script = session.get("script_text", "").strip()
        kb_rag_snippet = self.search_knowledge_base(user_speech)
        full_context = f"{assigned_script}\n\nRelevant QA Snippet: {kb_rag_snippet}".strip()

        # 2. Query Gemini LLM with assigned script context
        system_instructions = (
            f"{session['system_prompt']}\n\n"
            f"ASSIGNED CONVERSATION SCRIPT & KNOWLEDGE BASE:\n{full_context}\n\n"
            f"Target customer name: {lead}\n"
            f"Instructions: You are an intelligent AI sales agent on a live phone call with {lead}. "
            f"1. IF THE CUSTOMER ASKS A QUESTION: Answer their question accurately using the Knowledge Base above. "
            f"2. THEN: Seamlessly transition to the next step of your call script. "
            f"3. CONVERSATION STYLE: Keep responses warm, natural, human-like, and strictly under 2-3 short spoken sentences."
        )


        ai_response = await ai_provider_service.generate_response(
            system_prompt=system_instructions,
            script=full_context,
            conversation_history=session["history"],
            user_input=user_speech
        )

        if ai_response and ai_response.strip():
            return ai_response.strip()

        # 3. Dynamic Script Fallback: Parse uploaded script text lines dynamically
        if assigned_script:
            # Clean and split script into non-empty sentences/lines
            lines = [
                line.strip() for line in assigned_script.replace("\r", "\n").split("\n")
                if line.strip() and not line.strip().startswith("#") and len(line.strip()) > 5
            ]
            if lines:
                # Select current line from assigned script based on conversation stage
                line_idx = min(stage - 1, len(lines) - 1)
                script_line = lines[line_idx]
                # Replace placeholders if present
                script_line = (
                    script_line
                    .replace("{Candidate Name}", lead)
                    .replace("[Candidate Name]", lead)
                    .replace("{name}", lead)
                    .replace("[name]", lead)
                    .replace("{Your Name}", agent_name)
                    .replace("[Your Name]", agent_name)
                    .replace("{Recruitment Company Name}", "Voxera Recruitment")
                    .replace("[Recruitment Company Name]", "Voxera Recruitment")
                    .replace("{Client Name}", "Innovate AI Labs")
                    .replace("[Client Name]", "Innovate AI Labs")
                    .replace("{Location}", "Mumbai / Hybrid")
                    .replace("[Location]", "Mumbai / Hybrid")
                )
                return script_line


        # Default fallback if KB has no document text
        return f"Thank you so much for chatting with me today, {lead}. Have a wonderful day!"


        """Generates initial greeting audio for the start of the call."""
        session = self.get_or_create_session(call_id)
        greeting = agent_greeting or session["greeting"]
        
        # Personalize if lead name is known
        if session["lead_name"] and session["lead_name"] != "there":
            greeting = f"Hi {session['lead_name']}! This is {session['agent_name']} from Voxera AI. Am I catching you at a bad time?"

        logger.info(f"Initial Call Greeting for {call_id}: '{greeting}'")
        session["history"].append({"role": "assistant", "content": greeting})
        session["is_speaking"] = True
        session["is_initial_greeting"] = True
        audio_bytes = await ai_provider_service.generate_speech(greeting)
        return audio_bytes

    async def end_call(self, call_id: str):
        """Clean up session memory and persist transcript & recording logs to DB when call ends."""
        if call_id in self.active_sessions:
            session = self.active_sessions[call_id]
            logger.info(f"Ending conversation session for Call SID {call_id}")

            # Save transcript & call history to PostgreSQL
            try:
                import json
                from app.database.connection import SessionLocal
                from app.models.call import Call

                with SessionLocal() as db:
                    call = db.query(Call).filter(Call.id == call_id).first()
                    if call:
                        call.status = "completed"
                        call.transcript = json.dumps(session["history"])
                        db.commit()
                        logger.info(f"Persisted transcript ({len(session['history'])} turns) to DB for Call {call_id}")
            except Exception as e:
                logger.error(f"Error persisting call transcript to DB: {e}")

            del self.active_sessions[call_id]


conversation_service = ConversationService()


