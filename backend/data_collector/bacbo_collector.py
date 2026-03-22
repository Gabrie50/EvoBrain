"""Coletor específico para Bac Bo."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

import requests

from config import settings
from data_collector.base import BaseDataCollector, DataPoint
from utils.logger import get_logger

logger = get_logger(__name__)


class BacBoCollector(BaseDataCollector):
    def __init__(self):
        self.api_url = settings.data_source.bacbo_api_url
        self.latest_url = f"{self.api_url}/latest"
        self.headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
        self.last_id: Optional[str] = None
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def fetch_latest(self) -> Optional[DataPoint]:
        try:
            response = self.session.get(self.latest_url, timeout=5)
            response.raise_for_status()
            data = response.json()
            rodada_id = data.get("id")
            if rodada_id == self.last_id:
                return None
            self.last_id = rodada_id
            result = data.get("data", {}).get("result", {})
            player_dice = result.get("playerDice", {})
            banker_dice = result.get("bankerDice", {})
            player_score = player_dice.get("first", 0) + player_dice.get("second", 0)
            banker_score = banker_dice.get("first", 0) + banker_dice.get("second", 0)
            outcome = result.get("outcome", "")
            if outcome == "PlayerWon":
                action = "PLAYER"
            elif outcome == "BankerWon":
                action = "BANKER"
            else:
                action = "TIE"
            return DataPoint(
                id=rodada_id,
                timestamp=datetime.now(timezone.utc),
                action=action,
                value=player_score + banker_score,
                metadata={"player_score": player_score, "banker_score": banker_score},
                raw_data=data,
            )
        except Exception as exc:
            logger.debug(f"Erro na API Bac Bo: {exc}")
            return None

    def fetch_history(self, limit: int = 100) -> List[DataPoint]:
        return []

    def validate(self, data: DataPoint) -> bool:
        return data.id is not None and data.action in ["BANKER", "PLAYER", "TIE"]
