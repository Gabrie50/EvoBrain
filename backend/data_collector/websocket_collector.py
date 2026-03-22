"""Coletor genérico para WebSocket."""

from __future__ import annotations

import json
import threading
import time
from datetime import datetime
from typing import Callable, Dict, List, Optional

from data_collector.base import BaseDataCollector, DataPoint
from utils.logger import get_logger

logger = get_logger(__name__)

try:
    import websocket

    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False


class WebSocketCollector(BaseDataCollector):
    def __init__(self, url: str, headers: Dict | None = None, on_message_callback: Callable | None = None):
        self.url = url
        self.headers = headers or {}
        self.on_message_callback = on_message_callback
        self.last_data: Optional[DataPoint] = None
        self._running = False
        self._thread: Optional[threading.Thread] = None
        if not WEBSOCKET_AVAILABLE:
            logger.warning("WebSocket não disponível. Instale: pip install websocket-client")

    def start(self):
        if not WEBSOCKET_AVAILABLE:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        while self._running:
            try:
                ws = websocket.WebSocketApp(
                    self.url,
                    header=[f"{key}: {value}" for key, value in self.headers.items()],
                    on_open=self._on_open,
                    on_message=self._on_message,
                    on_error=self._on_error,
                )
                ws.run_forever()
            except Exception as exc:
                logger.error(f"Erro no WebSocket: {exc}")
                time.sleep(5)

    def _on_open(self, ws):
        del ws
        logger.info("✅ WebSocket conectado")

    def _on_message(self, ws, message):
        del ws
        try:
            data = json.loads(message)
            item_id = data.get("id") or str(hash(str(data)))
            action = data.get("result") or data.get("action") or data.get("type", "UNKNOWN")
            value = data.get("value") or data.get("price") or data.get("score", 0)
            self.last_data = DataPoint(
                id=str(item_id),
                timestamp=datetime.now(),
                action=str(action).upper(),
                value=float(value) if isinstance(value, (int, float)) else 0,
                raw_data=data,
            )
            if self.on_message_callback:
                self.on_message_callback(self.last_data)
        except json.JSONDecodeError:
            pass

    def _on_error(self, ws, error):
        del ws
        logger.error(f"Erro WebSocket: {error}")

    def fetch_latest(self) -> Optional[DataPoint]:
        return self.last_data

    def fetch_history(self, limit: int = 100) -> List[DataPoint]:
        return []

    def validate(self, data: DataPoint) -> bool:
        return data.id is not None and data.action is not None

    def stop(self):
        self._running = False
