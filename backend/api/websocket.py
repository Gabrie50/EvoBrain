"""WebSocket para comunicação em tempo real com o frontend."""

import json
import time
from typing import Set

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        stale = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as exc:
                logger.error(f"Erro ao enviar mensagem: {exc}")
                stale.append(connection)
        for connection in stale:
            self.disconnect(connection)


manager = ConnectionManager()


@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
            except json.JSONDecodeError:
                await manager.send_personal_message({"type": "error", "message": "Invalid JSON"}, websocket)
                continue
            if msg.get('type') == 'ping':
                await manager.send_personal_message({"type": "pong", "timestamp": time.time()}, websocket)
            elif msg.get('type') == 'subscribe':
                await manager.send_personal_message({"type": "subscribed", "topic": msg.get('topic')}, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def broadcast_prediction(prediction: dict):
    await manager.broadcast({"type": "prediction", "data": prediction, "timestamp": time.time()})


async def broadcast_stats(stats: dict):
    await manager.broadcast({"type": "stats", "data": stats, "timestamp": time.time()})
