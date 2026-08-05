import json
import base64
import logging
import asyncio
from xml.sax.saxutils import escape as xml_escape
from fastapi import APIRouter, Request, Depends, HTTPException, Response, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.call import Call
from app.services.telephony_service import telephony_provider
from app.services.conversation_service import conversation_service
from app.config.settings import get_settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/twilio/voice")
@router.get("/twilio/voice")
async def twilio_voice_twiml(
    request: Request,
    call_id: str = "default",
    db: Session = Depends(get_db)
):
    """
    Primary TwiML webhook Twilio calls when the phone is answered.
    """
    settings = get_settings()
    base_url = settings.webhook_base_url.rstrip("/")

    # Get conversation session & initial greeting text
    session = conversation_service.get_or_create_session(call_id)
    greeting = f"Hi {session['lead_name']}! This is {session['agent_name']} from Voxera AI. Am I catching you at a bad time?"
    session["history"].append({"role": "assistant", "content": greeting})

    # Persist initial greeting to Call transcript in DB
    try:
        call_record = db.query(Call).filter(Call.id == call_id).first()
        if call_record:
            call_record.transcript = session["history"]
            call_record.status = "in-progress"
            db.commit()
    except Exception as tx_err:
        logger.warning(f"Could not persist initial transcript for {call_id}: {tx_err}")

    gather_action = f"{base_url}/api/v1/webhooks/twilio/gather?call_id={call_id}"

    logger.info(f"TwiML Voice webhook: call_id={call_id}, lead={session['lead_name']}, agent={session['agent_name']}")

    safe_greeting = xml_escape(greeting)
    twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Gather input="speech" action="{gather_action}" method="POST" timeout="8" speechTimeout="3" bargeIn="true">
        <Say voice="Polly.Joanna">{safe_greeting}</Say>
    </Gather>
</Response>'''
    return Response(content=twiml, media_type="text/xml")



@router.post("/twilio/gather")
@router.get("/twilio/gather")
async def twilio_voice_gather(
    request: Request,
    call_id: str = "default",
    db: Session = Depends(get_db)
):
    """
    Handles speech input from customer during live phone call.
    Uses Human Script Engine (Gemini LLM + Knowledge Base Script State Machine).
    Continues call loop infinitely until caller hangs up.
    """
    settings = get_settings()
    base_url = settings.webhook_base_url.rstrip("/")
    gather_action = f"{base_url}/api/v1/webhooks/twilio/gather?call_id={call_id}"

    # Parse SpeechResult from Twilio POST request
    form_data = await request.form()
    speech_result = form_data.get("SpeechResult") or ""
    logger.info(f"Twilio Gather Call {call_id} Speech Received: '{speech_result}'")

    session = conversation_service.get_or_create_session(call_id)

    if speech_result and speech_result.strip():
        session["history"].append({"role": "user", "content": speech_result})

        # Generate next human-like script response
        ai_response_text = await conversation_service.generate_next_script_turn(call_id, speech_result)
        logger.info(f"Call {call_id} AI Response: '{ai_response_text}'")
        session["history"].append({"role": "assistant", "content": ai_response_text})

        # Persist transcript to PostgreSQL so Live Monitor can display it
        try:
            call_record = db.query(Call).filter(Call.id == call_id).first()
            if call_record:
                call_record.transcript = session["history"]
                call_record.status = "in-progress"
                db.commit()
        except Exception as tx_err:
            logger.warning(f"Could not persist transcript for {call_id}: {tx_err}")

        # XML-escape the AI response to prevent TwiML parsing errors
        safe_response = xml_escape(ai_response_text)

        twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Gather input="speech" action="{gather_action}" method="POST" timeout="8" speechTimeout="3" bargeIn="true">
        <Say voice="Polly.Joanna">{safe_response}</Say>
    </Gather>
</Response>'''
        return Response(content=twiml, media_type="text/xml")

    # If no speech detected, keep call alive and prompt gently
    lead = xml_escape(session["lead_name"])
    twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Gather input="speech" action="{gather_action}" method="POST" timeout="8" speechTimeout="3" bargeIn="true">
        <Say voice="Polly.Joanna">Are you still there {lead}? How can I help you today?</Say>
    </Gather>
</Response>'''
    return Response(content=twiml, media_type="text/xml")




@router.post("/twilio/call-status")
@router.get("/twilio/call-status")
async def twilio_call_status(
    request: Request,
    call_id: str = "default",
    db: Session = Depends(get_db)
):
    """Webhook to handle call status changes from Twilio."""
    form_data = await request.form()
    status = form_data.get("CallStatus") or "in-progress"
    logger.info(f"Twilio status callback: call_id={call_id}, status={status}")

    if call_id and call_id != "default":
        if status in ["completed", "failed", "busy", "no-answer", "canceled"]:
            await conversation_service.end_call(call_id)

    return Response(content="<?xml version='1.0'?><Response></Response>", media_type="text/xml")


@router.websocket("/twilio/media/{call_id}")
async def twilio_media_stream(websocket: WebSocket, call_id: str):
    """
    Bidirectional WebSocket endpoint for Twilio Media Streams fallback.
    """
    await websocket.accept()
    logger.info(f"Twilio WebSocket Connected for Call SID {call_id}")
    
    greeting_task = asyncio.create_task(conversation_service.generate_initial_greeting(call_id))
    stream_sid = None
    
    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            
            if msg["event"] == "start":
                stream_sid = msg["start"]["streamSid"]
                logger.info(f"Media Stream Started: {stream_sid}")
                
                initial_audio = await greeting_task
                if initial_audio and stream_sid:
                    chunk_size = 320
                    for i in range(0, len(initial_audio), chunk_size):
                        chunk = initial_audio[i:i + chunk_size]
                        out_payload = base64.b64encode(chunk).decode('utf-8')
                        media_msg = {
                            "event": "media",
                            "streamSid": stream_sid,
                            "media": {
                                "streamSid": stream_sid,
                                "payload": out_payload
                            }
                        }
                        await websocket.send_text(json.dumps(media_msg))
                        await asyncio.sleep(0.035)

            elif msg["event"] == "media":
                audio_payload = msg["media"]["payload"]
                audio_bytes = base64.b64decode(audio_payload)
                
                ai_audio_bytes, should_interrupt = await conversation_service.process_streaming_audio(
                    call_id=call_id, 
                    audio_chunk=audio_bytes
                )
                
                if should_interrupt and stream_sid:
                    clear_msg = {"event": "clear", "streamSid": stream_sid}
                    await websocket.send_text(json.dumps(clear_msg))
                    
                if ai_audio_bytes and stream_sid:
                    chunk_size = 320
                    for i in range(0, len(ai_audio_bytes), chunk_size):
                        chunk = ai_audio_bytes[i:i + chunk_size]
                        out_payload = base64.b64encode(chunk).decode('utf-8')
                        media_msg = {
                            "event": "media",
                            "streamSid": stream_sid,
                            "media": {
                                "streamSid": stream_sid,
                                "payload": out_payload
                            }
                        }
                        await websocket.send_text(json.dumps(media_msg))
                        await asyncio.sleep(0.035)
                    
            elif msg["event"] == "stop":
                break

    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error(f"WebSocket Error on Call {call_id}: {e}")
    finally:
        await conversation_service.end_call(call_id)
