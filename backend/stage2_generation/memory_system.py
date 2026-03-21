"""Sistema de memória para agentes."""

from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

import numpy as np

from config import settings


class MemoryType(Enum):
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"
    SOCIAL = "social"
    EMOTIONAL = "emotional"


class MemoryImportance(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Memory:
    id: str
    content: str
    memory_type: MemoryType
    importance: MemoryImportance
    timestamp: float
    agent_id: int
    related_agents: List[int] = field(default_factory=list)
    embedding: Optional[np.ndarray] = None
    access_count: int = 0
    last_accessed: float = 0
    consolidation_strength: float = 0.5

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "content": self.content,
            "memory_type": self.memory_type.value,
            "importance": self.importance.value,
            "timestamp": self.timestamp,
            "agent_id": self.agent_id,
            "related_agents": self.related_agents,
            "access_count": self.access_count,
            "last_accessed": self.last_accessed,
            "consolidation_strength": self.consolidation_strength,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Memory":
        return cls(
            id=data["id"],
            content=data["content"],
            memory_type=MemoryType(data["memory_type"]),
            importance=MemoryImportance(data["importance"]),
            timestamp=data["timestamp"],
            agent_id=data["agent_id"],
            related_agents=data.get("related_agents", []),
            access_count=data.get("access_count", 0),
            last_accessed=data.get("last_accessed", 0),
            consolidation_strength=data.get("consolidation_strength", 0.5),
        )


class EpisodicMemory:
    def __init__(self, capacity: int | None = None):
        self.capacity = capacity or settings.memory.episodic_size
        self.memories: deque[Memory] = deque(maxlen=self.capacity)

    def add(self, memory: Memory):
        self.memories.append(memory)

    def get_recent(self, n: int = 10) -> List[Memory]:
        return list(self.memories)[-n:]

    def get_all(self) -> List[Memory]:
        return list(self.memories)

    def clear(self):
        self.memories.clear()


class LongTermMemory:
    def __init__(self, capacity: int | None = None, decay_rate: float | None = None):
        self.capacity = capacity or settings.memory.long_term_size
        self.decay_rate = decay_rate or settings.memory.decay_rate
        self.memories: Dict[str, Memory] = {}

    def add(self, memory: Memory):
        if len(self.memories) >= self.capacity:
            self._forget_weakest()
        self.memories[memory.id] = memory

    def get(self, memory_id: str) -> Optional[Memory]:
        memory = self.memories.get(memory_id)
        if memory is not None:
            memory.access_count += 1
            memory.last_accessed = time.time()
        return memory

    def search_by_content(self, query: str, limit: int = 10) -> List[Memory]:
        query_lower = query.lower()
        results = [memory for memory in self.memories.values() if query_lower in memory.content.lower()]
        results.sort(key=lambda item: (item.importance.value, item.access_count), reverse=True)
        return results[:limit]

    def search_by_time(self, start_time: float, end_time: float) -> List[Memory]:
        return [memory for memory in self.memories.values() if start_time <= memory.timestamp <= end_time]

    def consolidate(self):
        now = time.time()
        for memory in self.memories.values():
            if memory.access_count > 10:
                memory.consolidation_strength = min(1.0, memory.consolidation_strength + 0.05)
            if memory.last_accessed and now - memory.last_accessed > 86400:
                memory.consolidation_strength *= 1 - self.decay_rate

    def _forget_weakest(self):
        if not self.memories:
            return
        weakest = min(self.memories.values(), key=lambda item: item.consolidation_strength)
        del self.memories[weakest.id]


class SocialMemory:
    def __init__(self):
        self.relationships: Dict[Tuple[int, int], float] = {}
        self.interaction_history: Dict[Tuple[int, int], List[Dict]] = {}

    def update_relationship(self, agent_a: int, agent_b: int, delta: float):
        key = (min(agent_a, agent_b), max(agent_a, agent_b))
        current = self.relationships.get(key, 0.5)
        self.relationships[key] = max(0.0, min(1.0, current + delta))

    def get_affinity(self, agent_a: int, agent_b: int) -> float:
        key = (min(agent_a, agent_b), max(agent_a, agent_b))
        return self.relationships.get(key, 0.5)

    def add_interaction(self, agent_a: int, agent_b: int, interaction_type: str, content: str):
        key = (min(agent_a, agent_b), max(agent_a, agent_b))
        self.interaction_history.setdefault(key, []).append(
            {
                "timestamp": time.time(),
                "type": interaction_type,
                "content": content,
            }
        )
        affinity_delta = {
            "agreement": 0.1,
            "disagreement": -0.05,
            "collaboration": 0.15,
            "conflict": -0.1,
            "help": 0.2,
        }.get(interaction_type, 0.02)
        self.update_relationship(agent_a, agent_b, affinity_delta)

    def get_interaction_summary(self, agent_a: int, agent_b: int) -> Dict:
        key = (min(agent_a, agent_b), max(agent_a, agent_b))
        interactions = self.interaction_history.get(key, [])
        return {
            "affinity": self.get_affinity(agent_a, agent_b),
            "total_interactions": len(interactions),
            "recent_interactions": interactions[-5:] if interactions else [],
        }


class WorkingMemory:
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.items: List[Dict] = []

    def add(self, item: Dict):
        self.items.append(item)
        if len(self.items) > self.capacity:
            self.items.pop(0)

    def get_context(self) -> Dict:
        return {
            "current_items": self.items,
            "size": len(self.items),
            "recent": self.items[-3:] if self.items else [],
        }

    def clear(self):
        self.items.clear()


class MemorySystem:
    def __init__(self, agent_id: int):
        self.agent_id = agent_id
        self.episodic = EpisodicMemory()
        self.long_term = LongTermMemory()
        self.social = SocialMemory()
        self.working = WorkingMemory()
        self._memory_counter = 0

    def _generate_memory_id(self) -> str:
        self._memory_counter += 1
        return f"mem_{self.agent_id}_{self._memory_counter}_{int(time.time())}"

    def remember(
        self,
        content: str,
        memory_type: MemoryType = MemoryType.EPISODIC,
        importance: MemoryImportance = MemoryImportance.MEDIUM,
        related_agents: Optional[List[int]] = None,
    ):
        memory = Memory(
            id=self._generate_memory_id(),
            content=content,
            memory_type=memory_type,
            importance=importance,
            timestamp=time.time(),
            agent_id=self.agent_id,
            related_agents=related_agents or [],
        )
        if memory_type == MemoryType.EPISODIC:
            self.episodic.add(memory)
        else:
            self.long_term.add(memory)
        return memory

    def recall(self, query: str | None = None, limit: int = 10) -> List[Memory]:
        memories: List[Memory] = []
        memories.extend(self.episodic.get_recent(5))
        if query:
            memories.extend(self.long_term.search_by_content(query, limit))

        unique: List[Memory] = []
        seen = set()
        for memory in memories:
            if memory.id not in seen:
                seen.add(memory.id)
                unique.append(memory)

        unique.sort(key=lambda item: (item.importance.value, item.access_count), reverse=True)
        for memory in unique[: self.working.capacity]:
            self.working.add(
                {
                    "id": memory.id,
                    "content": memory.content,
                    "type": memory.memory_type.value,
                    "importance": memory.importance.value,
                }
            )
        return unique[:limit]

    def consolidate(self):
        self.long_term.consolidate()

    def get_summary(self) -> Dict:
        return {
            "agent_id": self.agent_id,
            "episodic_count": len(self.episodic.memories),
            "long_term_count": len(self.long_term.memories),
            "working_memory_size": len(self.working.items),
            "social_relationships": len(self.social.relationships),
        }
