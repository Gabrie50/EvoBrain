"""Coletor genérico para API REST."""

from __future__ import annotations

import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests

from data_collector.base import BaseDataCollector, DataPoint
from utils.logger import get_logger

logger = get_logger(__name__)


class RESTAPICollector(BaseDataCollector):
    def __init__(
        self,
        url: str,
        headers: Dict | None = None,
        params: Dict | None = None,
        interval: float = 0.5,
    ):
        self.url = url
        self.headers = headers or {}
        self.params = params or {}
        self.interval = interval
        self.last_id: Optional[str] = None
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def fetch_latest(self) -> Optional[DataPoint]:
        try:
            params = self.params.copy()
            params["_t"] = int(time.time() * 1000)
            response = self.session.get(self.url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict):
                return None
            item_id = data.get("id") or data.get("Id") or str(hash(str(data)))
            action = data.get("result") or data.get("action") or data.get("type", "UNKNOWN")
            value = data.get("value") or data.get("price") or data.get("score", 0)
            if item_id == self.last_id:
                return None
            self.last_id = str(item_id)
            return DataPoint(
                id=str(item_id),
                timestamp=datetime.now(),
                action=str(action).upper(),
                value=float(value) if isinstance(value, (int, float)) else 0,
                raw_data=data,
            )
        except Exception as exc:
            logger.debug(f"Erro na API REST: {exc}")
            return None

    def fetch_history(self, limit: int = 100) -> List[DataPoint]:
        return []

    def validate(self, data: DataPoint) -> bool:
        return data.id is not None and data.action is not None
