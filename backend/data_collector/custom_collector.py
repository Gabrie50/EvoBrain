"""Coletor customizado - usuário implementa."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from data_collector.base import BaseDataCollector, DataPoint
from utils.logger import get_logger

logger = get_logger(__name__)


class CustomDataCollector(BaseDataCollector):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.last_id: Optional[str] = None
        logger.warning("⚠️ Coletor customizado ativado! Implemente fetch_latest()")

    def fetch_latest(self) -> Optional[DataPoint]:
        raise NotImplementedError("Implemente fetch_latest() na sua classe CustomDataCollector")

    def fetch_history(self, limit: int = 100) -> List[DataPoint]:
        raise NotImplementedError("Implemente fetch_history()")

    def validate(self, data: DataPoint) -> bool:
        return data.id is not None and data.action is not None
