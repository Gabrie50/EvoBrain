"""Base para coletores de dados genéricos."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class DataPoint:
    id: str
    timestamp: datetime
    action: str
    value: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    raw_data: Dict[str, Any] = field(default_factory=dict)


class BaseDataCollector(ABC):
    @abstractmethod
    def fetch_latest(self) -> Optional[DataPoint]:
        pass

    @abstractmethod
    def fetch_history(self, limit: int = 100) -> List[DataPoint]:
        pass

    @abstractmethod
    def validate(self, data: DataPoint) -> bool:
        pass
