"""Extrator de conhecimento com GraphRAG e LLM local."""

import json
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List

from llm.local_llm import LocalLLM
from stage1_extraction.knowledge_graph import KnowledgeGraph
from stage1_extraction.pdf_reader import PDFReader
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Entity:
    name: str
    entity_type: str
    description: str
    aliases: List[str] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Relation:
    source: str
    target: str
    relation_type: str
    description: str = ""


class GraphExtractor:
    def __init__(self, llm: LocalLLM):
        self.llm = llm
        self.pdf_reader = PDFReader()
        self.knowledge_graph = KnowledgeGraph()

    def extract_from_pdf(self, pdf_content: bytes, filename: str) -> Dict[str, Any]:
        text = self.pdf_reader.extract_text(pdf_content)
        entities = self._extract_entities(text)
        relations = self._extract_relations(text, entities)
        for entity in entities:
            self.knowledge_graph.add_entity(entity.name, entity.entity_type, entity.description, entity.properties)
        for relation in relations:
            self.knowledge_graph.add_relation(relation.source, relation.target, relation.relation_type, relation.description)
        summary = self._generate_summary(text, entities, relations)
        return {
            "filename": filename,
            "text_length": len(text),
            "entities": [vars(item) for item in entities],
            "relations": [vars(item) for item in relations],
            "summary": summary,
            "graph": self.knowledge_graph.to_dict(),
        }

    def extract_from_text(self, text: str) -> Dict[str, Any]:
        entities = self._extract_entities(text)
        relations = self._extract_relations(text, entities)
        return {"text_length": len(text), "entities": [vars(item) for item in entities], "relations": [vars(item) for item in relations]}

    def _extract_entities(self, text: str) -> List[Entity]:
        prompt = f"Extraia entidades do texto e retorne JSON.\nTexto:\n{text[:3000]}"
        response = self.llm.generate(prompt)
        try:
            data = json.loads(response)
        except json.JSONDecodeError:
            return self._extract_entities_fallback(text)
        result = []
        for item in data.get("entities", []):
            result.append(Entity(name=item["name"], entity_type=item.get("type", "conceito"), description=item.get("description", ""), aliases=item.get("aliases", []), properties=item.get("properties", {})))
        return result

    def _extract_entities_fallback(self, text: str) -> List[Entity]:
        import re

        entities: List[Entity] = []
        patterns = [
            (r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", "pessoa"),
            (r"\b[A-Z][a-z]+ (Bank|Corp|Inc|Ltd|Group)\b", "organizacao"),
            (r"\b\d{4}\b", "evento"),
        ]
        for pattern, entity_type in patterns:
            matches = re.findall(pattern, text)
            seen = set()
            for match in matches:
                name = match if isinstance(match, str) else match[0]
                if name in seen:
                    continue
                seen.add(name)
                entities.append(Entity(name=name, entity_type=entity_type, description="Entidade detectada automaticamente"))
                if len(seen) >= 5:
                    break
        return entities

    def _extract_relations(self, text: str, entities: List[Entity]) -> List[Relation]:
        if len(entities) < 2:
            return []
        prompt = f"Identifique relações entre: {', '.join(entity.name for entity in entities[:20])}. Retorne JSON."
        response = self.llm.generate(prompt)
        try:
            data = json.loads(response)
        except json.JSONDecodeError:
            return []
        return [Relation(source=item["source"], target=item["target"], relation_type=item.get("type", "relacionado"), description=item.get("description", "")) for item in data.get("relations", [])]

    def _generate_summary(self, text: str, entities: List[Entity], relations: List[Relation]) -> str:
        names = ", ".join(entity.name for entity in entities[:10])
        return self.llm.generate(f"Resuma o documento em 3 frases. Entidades: {names}. Texto: {text[:1500]}")
