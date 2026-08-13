"""WebSocket route handlers for live call streaming and dashboard monitoring."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from typing import Optional
from app.websockets.connection_manager import ws_manager
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.websocket("/ws/calls/{call_id}")
async def call_live_stream_endpoint(
    websocket: WebSocket,
    call_id: str,
    token: Optional[str] = Query(None),
):
    """Real-time WebSocket endpoint for watching live audio call transcripts and state events."""
    await ws_manager.connect(websocket)
    room_id = f"call:{call_id}"
    ws_manager.subscribe(websocket, room_id)

    try:
        from app.services.conversation_service import conversation_service
        session = conversation_service.active_sessions.get(call_id)
        current_transcript = session.get("history", []) if session else []

        # If not in active sessions, check DB
        if not current_transcript:
            from app.database.connection import SessionLocal
            from app.models.call import Call
            import uuid
            try:
                with SessionLocal() as db:
                    c = None
                    try:
                        c = db.query(Call).filter(Call.id == uuid.UUID(call_id)).first()
                    except Exception:
                        c = db.query(Call).filter(Call.provider_call_id == call_id).first()
                    if c and c.transcript:
                        current_transcript = c.transcript if isinstance(c.transcript, list) else []
            except Exception:
                pass

        # Send initial connection confirmation with complete transcript history
        await ws_manager.send_personal_message(
            {
                "event": "connected",
                "call_id": call_id,
                "transcript": current_transcript,
                "state": "speaking" if session and session.get("is_speaking") else "listening",
                "message": f"Subscribed to live feed for call {call_id}",
            },
            websocket,
        )

        while True:
            # Keep-alive receive loop & client command handler
            data = await websocket.receive_json()
            command = data.get("action")

            if command == "ping":
                await ws_manager.send_personal_message({"event": "pong"}, websocket)
            elif command == "mute":
                logger.info("Mute command received via WS", call_id=call_id)
            elif command == "end_call":
                logger.info("End call command received via WS", call_id=call_id)
                await conversation_service.end_call(call_id)
                await ws_manager.broadcast_to_room(
                    room_id,
                    {"event": "call_ended", "call_id": call_id, "state": "ended"},
                )
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        logger.info("Call monitoring WS disconnected", call_id=call_id)
    except Exception as e:
        logger.error("Error in call WS endpoint", call_id=call_id, error=str(e))
        ws_manager.disconnect(websocket)


@router.websocket("/ws/monitoring/org/{organization_id}")
async def org_monitoring_endpoint(
    websocket: WebSocket,
    organization_id: str,
):
    """Organization-wide real-time dashboard feed for active agent status and metrics."""
    await ws_manager.connect(websocket)
    room_id = f"org:{organization_id}"
    ws_manager.subscribe(websocket, room_id)

    try:
        await ws_manager.send_personal_message(
            {
                "event": "connected",
                "organization_id": organization_id,
                "message": "Subscribed to organization live monitoring feed",
            },
            websocket,
        )

        while True:
            data = await websocket.receive_json()
            if data.get("action") == "ping":
                await ws_manager.send_personal_message({"event": "pong"}, websocket)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        logger.error("Error in org monitoring WS endpoint", organization_id=organization_id, error=str(e))
        ws_manager.disconnect(websocket)
