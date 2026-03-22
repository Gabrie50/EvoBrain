"""Memória vetorial para busca semântica."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np

try:
    from sentence_transformers import SentenceTransformer

    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False

from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class VectorMemory:
    id: str
    content: str
    embedding: np.ndarray
    metadata: dict


class VectorMemoryStore:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = None
        self.memories: List[VectorMemory] = []
        if EMBEDDINGS_AVAILABLE:
            try:
                self.model = SentenceTransformer(model_name)
                logger.info(f"✅ Modelo de embeddings carregado: {model_name}")
            except Exception as exc:
                logger.warning(f"⚠️ Erro ao carregar modelo: {exc}")

    def add(self, memory_id: str, content: str, metadata: dict | None = None) -> bool:
        if not self.model:
            return False
        try:
            embedding = self.model.encode(content, normalize_embeddings=True)
            self.memories.append(
                VectorMemory(id=memory_id, content=content, embedding=embedding, metadata=metadata or {})
            )
            return True
        except Exception as exc:
            logger.error(f"Erro ao adicionar memória vetorial: {exc}")
            return False

    def search(self, query: str, top_k: int = 10) -> List[Tuple[str, float, dict]]:
        if not self.model or not self.memories:
            return []
        try:
            query_embedding = self.model.encode(query, normalize_embeddings=True)
            similarities = [
                (memory.id, float(np.dot(query_embedding, memory.embedding)), memory.metadata)
                for memory in self.memories
            ]
            similarities.sort(key=lambda item: item[1], reverse=True)
            return similarities[:top_k]
        except Exception as exc:
            logger.error(f"Erro na busca vetorial: {exc}")
            return []

    def clear(self):
        self.memories.clear()
