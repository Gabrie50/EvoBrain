"""Grafo de conhecimento - Armazena entidades e relações."""

from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class GraphNode:
    name: str
    entity_type: str
    description: str
    properties: Dict[str, Any] = field(default_factory=dict)
    neighbors: List[str] = field(default_factory=list)


@dataclass
class GraphEdge:
    source: str
    target: str
    relation_type: str
    description: str = ""


class KnowledgeGraph:
    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: List[GraphEdge] = []
        self._adjacency: Dict[str, List[str]] = defaultdict(list)

    def add_entity(self, name: str, entity_type: str, description: str = "", properties: Optional[Dict[str, Any]] = None) -> None:
        if name not in self.nodes:
            self.nodes[name] = GraphNode(name=name, entity_type=entity_type, description=description, properties=properties or {})

    def add_relation(self, source: str, target: str, relation_type: str, description: str = "") -> None:
        if source not in self.nodes:
            self.add_entity(source, "unknown", f"Relacionado a {target}")
        if target not in self.nodes:
            self.add_entity(target, "unknown", f"Relacionado a {source}")
        edge = GraphEdge(source, target, relation_type, description)
        self.edges.append(edge)
        self._adjacency[source].append(target)
        self._adjacency[target].append(source)
        self.nodes[source].neighbors.append(target)
        self.nodes[target].neighbors.append(source)

    def get_entity(self, name: str) -> Optional[GraphNode]:
        return self.nodes.get(name)

    def get_relations(self, entity: str) -> List[GraphEdge]:
        return [edge for edge in self.edges if edge.source == entity or edge.target == entity]

    def get_neighbors(self, entity: str) -> List[str]:
        return self._adjacency.get(entity, [])

    def find_path(self, source: str, target: str) -> Optional[List[str]]:
        if source not in self.nodes or target not in self.nodes:
            return None
        queue = deque([(source, [source])])
        visited = {source}
        while queue:
            current, path = queue.popleft()
            if current == target:
                return path
            for neighbor in self._adjacency.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

    def get_central_entities(self, top_n: int = 10) -> List[tuple]:
        degrees = [(name, len(self._adjacency[name])) for name in self.nodes]
        return sorted(degrees, key=lambda item: item[1], reverse=True)[:top_n]

    def get_entity_types(self) -> Dict[str, int]:
        result: Dict[str, int] = defaultdict(int)
        for node in self.nodes.values():
            result[node.entity_type] += 1
        return dict(result)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": [
                {"name": node.name, "type": node.entity_type, "description": node.description, "neighbors": node.neighbors}
                for node in self.nodes.values()
            ],
            "edges": [
                {"source": edge.source, "target": edge.target, "type": edge.relation_type, "description": edge.description}
                for edge in self.edges
            ],
            "stats": {
                "total_nodes": len(self.nodes),
                "total_edges": len(self.edges),
                "entity_types": self.get_entity_types(),
                "central_entities": self.get_central_entities(5),
            },
        }
