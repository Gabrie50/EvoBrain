"""Base de conhecimento acumulada."""

from __future__ import annotations

import json
import time
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class KnowledgeDocument:
    id: str
    source: str
    content: str
    entities: List[Dict]
    relations: List[Dict]
    timestamp: float
    tags: List[str] = field(default_factory=list)


class KnowledgeBase:
    def __init__(self, storage_path: str = "storage/knowledge"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.documents: Dict[str, KnowledgeDocument] = {}
        self.entity_index: Dict[str, List[str]] = defaultdict(list)
        self.tag_index: Dict[str, List[str]] = defaultdict(list)
        self._load()
        logger.info(f"📚 KnowledgeBase: {len(self.documents)} documentos")

    def add_document(self, source: str, knowledge: Dict) -> str:
        doc_id = f"{source}_{int(time.time())}"
        document = KnowledgeDocument(
            id=doc_id,
            source=source,
            content=knowledge.get("text", ""),
            entities=knowledge.get("entities", []),
            relations=knowledge.get("relations", []),
            timestamp=time.time(),
            tags=self._extract_tags(knowledge),
        )
        self.documents[doc_id] = document
        for entity in document.entities:
            self.entity_index[entity["name"]].append(doc_id)
        for tag in document.tags:
            self.tag_index[tag].append(doc_id)
        self._save_document(doc_id)
        logger.info(f"📄 Documento adicionado: {doc_id}")
        return doc_id

    def add_text(self, source: str, knowledge: Dict, text: str) -> str:
        updated = dict(knowledge)
        updated["text"] = text
        return self.add_document(source, updated)

    def _extract_tags(self, knowledge: Dict) -> List[str]:
        tags = set()
        for entity in knowledge.get("entities", []):
            tags.add(entity.get("type", entity.get("entity_type", "unknown")))
        return list(tags)

    def search_by_entity(self, entity_name: str) -> List[KnowledgeDocument]:
        doc_ids = self.entity_index.get(entity_name, [])
        return [self.documents[doc_id] for doc_id in doc_ids if doc_id in self.documents]

    def search_by_tag(self, tag: str) -> List[KnowledgeDocument]:
        doc_ids = self.tag_index.get(tag, [])
        return [self.documents[doc_id] for doc_id in doc_ids if doc_id in self.documents]

    def get_all_entities(self) -> Dict[str, int]:
        entity_counts: Dict[str, int] = defaultdict(int)
        for document in self.documents.values():
            for entity in document.entities:
                entity_counts[entity["name"]] += 1
        return dict(entity_counts)

    def _save_document(self, doc_id: str):
        document = self.documents[doc_id]
        path = self.storage_path / f"{doc_id}.json"
        with path.open("w", encoding="utf-8") as handle:
            json.dump(
                {
                    "id": document.id,
                    "source": document.source,
                    "content": document.content[:10000],
                    "entities": document.entities,
                    "relations": document.relations,
                    "timestamp": document.timestamp,
                    "tags": document.tags,
                },
                handle,
                indent=2,
                default=str,
            )

    def _load(self):
        for path in self.storage_path.glob("*.json"):
            try:
                with path.open("r", encoding="utf-8") as handle:
                    data = json.load(handle)
                document = KnowledgeDocument(
                    id=data["id"],
                    source=data["source"],
                    content=data["content"],
                    entities=data["entities"],
                    relations=data["relations"],
                    timestamp=data["timestamp"],
                    tags=data.get("tags", []),
                )
                self.documents[document.id] = document
                for entity in document.entities:
                    self.entity_index[entity["name"]].append(document.id)
                for tag in document.tags:
                    self.tag_index[tag].append(document.id)
            except Exception as exc:
                logger.error(f"Erro ao carregar {path}: {exc}")

    def get_statistics(self) -> dict:
        return {
            "total_documents": len(self.documents),
            "total_entities": len(self.entity_index),
            "total_tags": len(self.tag_index),
        }

    def get_size(self) -> int:
        return len(self.documents)
