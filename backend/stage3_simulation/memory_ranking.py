"""Ranking de memórias por importância emocional e utilidade."""

from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np

from stage2_generation.memory_system import Memory, MemoryType
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class RankedMemory:
    memory: Memory
    emotional_score: float = 0.0
    utility_score: float = 0.0
    social_score: float = 0.0
    recency_score: float = 0.0
    total_score: float = 0.0

    def compute_total(self, weights: Dict[str, float] | None = None):
        weights = weights or {"emotional": 0.3, "utility": 0.3, "social": 0.2, "recency": 0.2}
        self.total_score = (
            weights["emotional"] * self.emotional_score
            + weights["utility"] * self.utility_score
            + weights["social"] * self.social_score
            + weights["recency"] * self.recency_score
        )


class MemoryRanker:
    def __init__(self, decay_rate: float = 0.01):
        self.decay_rate = decay_rate
        self.memory_scores: Dict[str, RankedMemory] = {}
        self.usage_history: Dict[str, List[Tuple[float, bool]]] = defaultdict(list)
        logger.info("🏆 MemoryRanker inicializado")

    def rank_memory(
        self,
        memory: Memory,
        outcome: str | None = None,
        reward: float | None = None,
        social_impact: float = 0,
    ) -> RankedMemory:
        del outcome
        emotional_score = self._compute_emotional_score(reward) if reward is not None else memory.importance.value / 4.0
        utility_score = self._compute_utility_score(memory.id)
        recency_score = self._compute_recency_score(memory.timestamp)
        ranked = RankedMemory(
            memory=memory,
            emotional_score=emotional_score,
            utility_score=utility_score,
            social_score=social_impact,
            recency_score=recency_score,
        )
        ranked.compute_total()
        self.memory_scores[memory.id] = ranked
        return ranked

    def _compute_emotional_score(self, reward: float) -> float:
        return min(1.0, abs(reward) * 2)

    def _compute_utility_score(self, memory_id: str) -> float:
        history = self.usage_history.get(memory_id, [])
        if not history:
            return 0.5
        successes = sum(1 for _, success in history if success)
        success_rate = successes / len(history)
        recent_history = history[-10:]
        recent_successes = sum(1 for _, success in recent_history if success)
        recent_rate = recent_successes / max(1, len(recent_history))
        return 0.3 * success_rate + 0.7 * recent_rate

    def _compute_recency_score(self, timestamp: float) -> float:
        age = time.time() - timestamp
        return float(np.exp(-self.decay_rate * age / 3600))

    def record_usage(self, memory_id: str, success: bool):
        self.usage_history[memory_id].append((time.time(), success))
        if len(self.usage_history[memory_id]) > 100:
            self.usage_history[memory_id] = self.usage_history[memory_id][-100:]

    def get_top_memories(self, agent_id: int | None = None, n: int = 10) -> List[RankedMemory]:
        memories = list(self.memory_scores.values())
        if agent_id is not None:
            memories = [memory for memory in memories if memory.memory.agent_id == agent_id]
        memories.sort(key=lambda item: item.total_score, reverse=True)
        return memories[:n]

    def get_emotional_memories(self, agent_id: int | None = None, n: int = 5) -> List[RankedMemory]:
        memories = list(self.memory_scores.values())
        if agent_id is not None:
            memories = [memory for memory in memories if memory.memory.agent_id == agent_id]
        memories.sort(key=lambda item: item.emotional_score, reverse=True)
        return memories[:n]

    def consolidate_important_memories(self, threshold: float = 0.7):
        important = [memory for memory in self.memory_scores.values() if memory.total_score > threshold]
        for ranked in important:
            if ranked.memory.memory_type == MemoryType.EPISODIC:
                ranked.memory.memory_type = MemoryType.SEMANTIC
                ranked.memory.consolidation_strength = 0.8

    def get_statistics(self) -> dict:
        scores = [memory.total_score for memory in self.memory_scores.values()]
        return {
            "total_memories": len(self.memory_scores),
            "avg_score": float(np.mean(scores)) if scores else 0,
            "max_score": float(np.max(scores)) if scores else 0,
        }
