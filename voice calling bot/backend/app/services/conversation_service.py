import logging
from typing import List, Dict, Any, Tuple, Optional
from app.services.ai_providers import ai_provider_service
from app.services.audio_utils import calculate_audio_energy
from app.ai.validators import ResponseValidator
from app.services.escalation_service import escalation_service
from app.services.context_manager import context_manager
from app.core.circuit_breaker import llm_circuit_breaker
from app.ai.guardrails import guardrail_engine
from app.security.audit_logger import AuditLogger

logger = logging.getLogger(__name__)

# Energy threshold for Voice Activity Detection (VAD) interruption
VAD_INTERRUPT_THRESHOLD = 1500.0


class ConversationService:
    """Manages the lifecycle, memory, advanced guardrails, and LLM orchestration of a live call session."""

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
                        if hasattr(call, "lead_id") and call.lead_id:
                            lead = db.query(Lead).filter(Lead.id == call.lead_id).first()
                        if not lead:
                            lead = (
                                db.query(Lead)
                                .filter(Lead.phone_number == call.to_number)
                                .order_by(Lead.updated_at.desc(), Lead.created_at.desc())
                                .first()
                            )
                        if lead and lead.name:
                            lead_name = lead.name

                    # Load script from Agent's assigned Knowledge Base documents in DB
                    kb_id = (
                        agent.knowledge_base_id
                        if (agent and hasattr(agent, "knowledge_base_id") and agent.knowledge_base_id)
                        else None
                    )
                    if kb_id:
                        try:
                            kb_uuid = uuid.UUID(str(kb_id))
                            kb_docs = (
                                db.query(KnowledgeDocument)
                                .filter(
                                    (KnowledgeDocument.id == kb_uuid)
                                    | (KnowledgeDocument.knowledge_base_id == kb_uuid)
                                )
                                .order_by(KnowledgeDocument.created_at.desc())
                                .all()
                            )
                        except Exception:
                            kb_docs = (
                                db.query(KnowledgeDocument)
                                .filter(
                                    (KnowledgeDocument.id == str(kb_id))
                                    | (KnowledgeDocument.knowledge_base_id == str(kb_id))
                                )
                                .order_by(KnowledgeDocument.created_at.desc())
                                .all()
                            )
                    else:
                        kb_docs = db.query(KnowledgeDocument).order_by(KnowledgeDocument.created_at.desc()).all()

                    doc_scripts = [d.meta_data.strip() for d in kb_docs if d.meta_data and d.meta_data.strip()]
                    if doc_scripts:
                        script_text += "\n\n" + "\n---\n".join(doc_scripts)

                    logger.info(
                        f"Loaded Call SID {call_id}: Agent={agent_name}, Lead={lead_name}, KB_ID={kb_id}, Script length={len(script_text)}"
                    )

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
        """RAG Knowledge Base Lookup."""
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
        audio_chunk: bytes,
    ) -> Tuple[Optional[bytes], bool]:
        """Processes an incoming streaming mu-law audio chunk from Twilio."""
        session = self.get_or_create_session(call_id)

        # 1. Voice Activity Detection (VAD) & Barge-in Interruption
        audio_energy = calculate_audio_energy(audio_chunk)
        should_interrupt = False

        if session["is_speaking"] and not session.get("is_initial_greeting", False) and audio_energy > VAD_INTERRUPT_THRESHOLD:
            should_interrupt = True
            session["is_speaking"] = False
            logger.info(f"Barge-in / Interruption detected for Call SID {call_id} (Energy: {audio_energy:.1f})")

        session["audio_buffer"].extend(audio_chunk)

        # Process complete audio turn (~1 second of 8kHz mu-law audio = 8000 bytes)
        if len(session["audio_buffer"]) >= 8000:
            buffer_data = bytes(session["audio_buffer"])
            session["audio_buffer"].clear()

            user_text = await ai_provider_service.transcribe_audio(buffer_data)

            if user_text and user_text.strip():
                logger.info(f"Call {call_id} User Said: '{user_text}'")

                # Evaluate Guardrails on User Speech
                is_safe, sanitized_speech, violation_reason = guardrail_engine.evaluate_input(user_text)
                if not is_safe:
                    AuditLogger.log_guardrail_violation(call_id, "input_guardrail", violation_reason or "Unsafe input")
                    ai_response_text = sanitized_speech
                else:
                    # Check escalation triggers
                    is_escalated, _ = escalation_service.check_escalation_triggers(sanitized_speech)
                    if is_escalated:
                        ai_response_text = await escalation_service.trigger_call_escalation(call_id, session["lead_name"])
                    else:
                        session["history"].append({"role": "user", "content": sanitized_speech})
                        kb_script = self.search_knowledge_base(sanitized_speech)

                        compressed_history = context_manager.get_compressed_history(session["history"])

                        raw_response = await ai_provider_service.generate_response(
                            system_prompt=session["system_prompt"],
                            script=f"{kb_script}\nTarget customer name is {session['lead_name']}.",
                            conversation_history=compressed_history,
                            user_input=sanitized_speech,
                        )
                        # Evaluate Guardrails on LLM Response Output
                        is_out_safe, clean_output, out_reason = guardrail_engine.evaluate_output(raw_response, kb_script)
                        if not is_out_safe:
                            AuditLogger.log_guardrail_violation(call_id, "output_guardrail", out_reason or "Unsafe output")
                            ai_response_text = clean_output
                        else:
                            ai_response_text = ResponseValidator.validate_and_format(clean_output)

                logger.info(f"Call {call_id} Agent Response: '{ai_response_text}'")
                session["history"].append({"role": "assistant", "content": ai_response_text})
                session["is_speaking"] = True

                ai_audio_bytes = await ai_provider_service.generate_speech(ai_response_text)
                return ai_audio_bytes, should_interrupt

        return None, should_interrupt

    async def generate_next_script_turn(self, call_id: str, user_speech: str) -> str:
        """Dynamic Agent Knowledge Base Script Engine with Advanced Guardrails, Escalation & PII Tokenization."""
        session = self.get_or_create_session(call_id)
        session["stage_index"] += 1
        stage = session["stage_index"]
        lead = session["lead_name"]
        agent_name = session["agent_name"]

        # 1. Advanced Guardrails Inspection on Incoming Speech
        is_safe_input, sanitized_speech, violation_reason = guardrail_engine.evaluate_input(user_speech)
        if not is_safe_input:
            AuditLogger.log_guardrail_violation(call_id, "prompt_injection_or_toxicity", violation_reason or "Unsafe input")
            return sanitized_speech

        # 2. Check escalation triggers
        is_escalated, reason = escalation_service.check_escalation_triggers(sanitized_speech)
        if is_escalated:
            return await escalation_service.trigger_call_escalation(call_id, lead)

        # 3. Fetch assigned Knowledge Base script text
        assigned_script = session.get("script_text", "").strip()
        kb_rag_snippet = self.search_knowledge_base(sanitized_speech)
        full_context = f"{assigned_script}\n\nRelevant QA Snippet: {kb_rag_snippet}".strip()

        # 4. Context compression for sliding window history
        compressed_history = context_manager.get_compressed_history(session["history"])

        # 5. System Instructions
        system_instructions = (
            f"{session['system_prompt']}\n\n"
            f"ASSIGNED CONVERSATION SCRIPT & KNOWLEDGE BASE:\n{full_context}\n\n"
            f"Target customer name: {lead}\n"
            f"Instructions: You are an intelligent AI sales agent on a live phone call with {lead}. "
            f"1. IF THE CUSTOMER ASKS A QUESTION: Answer accurately using the Knowledge Base above. "
            f"2. THEN: Seamlessly transition to the next step of your call script. "
            f"3. CONVERSATION STYLE: Warm, natural, human-like, strictly under 2-3 short sentences."
        )

        async def _generate_llm_call():
            return await ai_provider_service.generate_response(
                system_prompt=system_instructions,
                script=full_context,
                conversation_history=compressed_history,
                user_input=sanitized_speech,
            )

        async def _fallback_script_call():
            if assigned_script:
                lines = [
                    line.strip()
                    for line in assigned_script.replace("\r", "\n").split("\n")
                    if line.strip() and not line.strip().startswith("#") and len(line.strip()) > 5
                ]
                if lines:
                    line_idx = min(stage - 1, len(lines) - 1)
                    return (
                        lines[line_idx]
                        .replace("{name}", lead)
                        .replace("[name]", lead)
                        .replace("{Your Name}", agent_name)
                    )
            return f"Thank you for taking my call today, {lead}. Let's stay in touch!"

        # Execute LLM call via Circuit Breaker
        raw_response = await llm_circuit_breaker.call_async(
            func=_generate_llm_call,
            fallback_func=_fallback_script_call,
        )

        # 6. Advanced Guardrails Inspection on Outgoing LLM Text
        is_safe_out, clean_out, out_reason = guardrail_engine.evaluate_output(raw_response or "", full_context)
        if not is_safe_out:
            AuditLogger.log_guardrail_violation(call_id, "output_guardrail", out_reason or "Unsafe output")
            return clean_out

        # Format length & redact PII
        formatted_response = ResponseValidator.validate_and_format(clean_out)
        return formatted_response or f"Thank you for chatting with me today, {lead}!"

    async def end_call(self, call_id: str):
        """Clean up session memory and persist transcript logs to DB when call ends."""
        session = self.active_sessions.get(call_id)
        logger.info(f"Ending conversation session for Call SID {call_id}")

        try:
            import uuid
            from datetime import datetime, UTC
            from app.database.connection import SessionLocal
            from app.models.call import Call

            with SessionLocal() as db:
                call = None
                if call_id and call_id != "default":
                    try:
                        call = db.query(Call).filter(Call.id == uuid.UUID(call_id)).first()
                    except Exception:
                        call = db.query(Call).filter(Call.provider_call_id == call_id).first()

                if not call:
                    call = db.query(Call).order_by(Call.created_at.desc()).first()

                if call:
                    call.status = "completed"
                    if not call.ended_at:
                        call.ended_at = datetime.now(UTC)
                    if call.started_at:
                        try:
                            started = call.started_at.replace(tzinfo=UTC) if call.started_at.tzinfo is None else call.started_at
                            call.duration_seconds = int((call.ended_at - started).total_seconds())
                        except Exception:
                            pass

                    transcript_history = session["history"] if session and "history" in session else call.transcript
                    if session and "history" in session:
                        call.transcript = session["history"]

                    # Perform AI automated post-call summary & sentiment analysis
                    if transcript_history:
                        try:
                            analysis = await ai_provider_service.analyze_call_transcript(transcript_history)
                            call.summary = analysis.get("summary")
                            call.sentiment = analysis.get("sentiment")
                            logger.info(f"AI Call Analysis [{call.id}]: sentiment='{call.sentiment}', summary='{call.summary}'")
                        except Exception as ai_err:
                            logger.warning(f"Failed to perform AI post-call analysis: {ai_err}")

                    db.commit()
                    logger.info(f"Persisted transcript and analysis to DB for Call {call.id}")
        except Exception as e:
            logger.error(f"Error persisting call transcript to DB: {e}")
        finally:
            self.active_sessions.pop(call_id, None)


conversation_service = ConversationService()
