"""
Pipeline de dados - orquestra a coleta de dados genéricos
"""

import threading
import time
from collections import deque
from typing import Callable, List, Optional

from config import settings
from data_collector.base import DataPoint
from data_collector.factory import create_data_collector
from utils.logger import get_logger

logger = get_logger(__name__)


class DataPipeline:
    def __init__(self, on_new_data: Optional[Callable] = None):
        self.collector = create_data_collector()
        self.on_new_data = on_new_data
        self._running = False
        self._thread = None
        self._last_id: Optional[str] = None
        self._data_buffer: deque = deque(maxlen=10000)
        logger.info("📊 DataPipeline inicializado")

    def start(self):
        if not self.collector:
            logger.error("❌ Nenhum coletor configurado")
            return
        self._running = True
        self._thread = threading.Thread(target=self._collect_loop, daemon=True)
        self._thread.start()
        logger.info(f"✅ Pipeline iniciado com coletor: {type(self.collector).__name__}")

    def _collect_loop(self):
        while self._running:
            try:
                data = self.collector.fetch_latest()
                if data and data.id != self._last_id:
                    self._last_id = data.id
                    self._data_buffer.append(data)
                    if self.on_new_data:
                        self.on_new_data(data)
                time.sleep(settings.data_source.interval)
            except Exception as exc:
                logger.error(f"Erro no loop: {exc}")
                time.sleep(5)

    def get_latest_data(self) -> Optional[DataPoint]:
        return self._data_buffer[-1] if self._data_buffer else None

    def get_history(self, limit: int = 100) -> List[DataPoint]:
        return list(self._data_buffer)[-limit:]

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
