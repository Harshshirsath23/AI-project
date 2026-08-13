"""WebSocket connection and room subscriptions manager."""

import json
from typing import Dict, List, Set, Optional
from fastapi import WebSocket
from app.core.logging import get_logger

logger = get_logger(__name__)


class ConnectionManager:
    """Manages WebSocket client connections and room-based pub/sub broadcasting."""

    def __init__(self):
        # Active connections: websocket -> user_id
        self.active_connections: Dict[WebSocket, Optional[str]] = {}
        # Room subscriptions: room_id -> set of websockets
        self.rooms: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: Optional[str] = None):
        """Accept new WebSocket connection."""
        await websocket.accept()
        self.active_connections[websocket] = user_id
        logger.info("WebSocket connection accepted", user_id=user_id)

    def disconnect(self, websocket: WebSocket):
        """Disconnect WebSocket client and remove from rooms."""
        if websocket in self.active_connections:
            del self.active_connections[websocket]

        # Remove from all rooms
        for room_id, clients in list(self.rooms.items()):
            clients.discard(websocket)
            if not clients:
                del self.rooms[room_id]

        logger.info("WebSocket disconnected")

    def subscribe(self, websocket: WebSocket, room_id: str):
        """Subscribe connection to a room (e.g., 'call:123', 'org:456')."""
        if room_id not in self.rooms:
            self.rooms[room_id] = set()
        self.rooms[room_id].add(websocket)
        logger.info("Subscribed to room", room_id=room_id)

    def unsubscribe(self, websocket: WebSocket, room_id: str):
        """Unsubscribe connection from a room."""
        if room_id in self.rooms:
            self.rooms[room_id].discard(websocket)
            if not self.rooms[room_id]:
                del self.rooms[room_id]

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send direct JSON message to a specific connection."""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error("Failed to send WS message", error=str(e))
            self.disconnect(websocket)

    async def broadcast_to_room(self, room_id: str, message: dict):
        """Broadcast message to all subscribers in a room."""
        if room_id not in self.rooms:
            return

        dead_connections: List[WebSocket] = []
        for connection in list(self.rooms[room_id]):
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error("Error broadcasting to room client", room_id=room_id, error=str(e))
                dead_connections.append(connection)

        for dead in dead_connections:
            self.disconnect(dead)


# Global singleton instance
ws_manager = ConnectionManager()
