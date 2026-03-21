"""Base de conhecimento acumulada para documentos e textos processados."""

from __future__ import annotations

import time
from typing import Any, Dict, List

from utils.logger import get_logger

logger = get_logger(__name__)


class KnowledgeBase:
    """Armazena conhecimento extraído de documentos e textos livres."""

    def __init__(self):
        self.documents: Dict[str, Dict[str, Any]] = {}
        self.text_entries: List[Dict[str, Any]] = []

    def add_document(self, source: str, knowledge: Dict[str, Any]):
        self.documents[source] = {
            "source": source,
            "knowledge": knowledge,
            "timestamp": time.time(),
        }
        logger.info(f"📚 Documento adicionado à base: {source}")

    def add_text(self, source: str, knowledge: Dict[str, Any], text: str):
        self.text_entries.append(
            {
                "source": source,
                "knowledge": knowledge,
                "text": text,
                "timestamp": time.time(),
            }
        )
        logger.info(f"📝 Texto adicionado à base: {source}")

    def get_size(self) -> int:
        return len(self.documents) + len(self.text_entries)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "documents": self.documents,
            "text_entries": self.text_entries,
            "size": self.get_size(),
        }
