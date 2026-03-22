"""Prioritized Replay Buffer com priorização baseada em erro TD e importância."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np

from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Experience:
    state: np.ndarray
    action: int
    reward: float
    next_state: np.ndarray
    done: bool
    td_error: float = 0.0
    importance: float = 0.5
    timestamp: float = field(default_factory=time.time)
    agent_id: int = 0


class PrioritizedReplayBuffer:
    def __init__(self, capacity: int = 100000, alpha: float = 0.6, beta: float = 0.4):
        self.capacity = capacity
        self.alpha = alpha
        self.beta = beta
        self.buffer: List[Experience] = []
        self.priorities = np.zeros(capacity, dtype=np.float32)
        self.position = 0
        self.size = 0
        logger.info(f"📀 PrioritizedReplayBuffer: capacity={capacity}")

    def push(self, experience: Experience):
        priority = (abs(experience.td_error) + 1e-6) ** self.alpha
        priority *= 0.5 + experience.importance
        if self.size < self.capacity:
            self.buffer.append(experience)
        else:
            self.buffer[self.position] = experience
        self.priorities[self.position] = priority
        self.position = (self.position + 1) % self.capacity
        self.size = min(self.size + 1, self.capacity)

    def sample(self, batch_size: int) -> Tuple[List[Experience], np.ndarray, np.ndarray]:
        if self.size < batch_size:
            return self.buffer[: self.size], np.ones(self.size), np.arange(self.size)

        probs = self.priorities[: self.size] ** self.alpha
        probs /= probs.sum()
        indices = np.random.choice(self.size, batch_size, p=probs)
        weights = (self.size * probs[indices]) ** (-self.beta)
        weights /= weights.max()
        experiences = [self.buffer[idx] for idx in indices]
        return experiences, weights, indices

    def update_priorities(self, indices: np.ndarray, td_errors: np.ndarray, importances: np.ndarray | None = None):
        for offset, (idx, td_error) in enumerate(zip(indices, td_errors)):
            priority = (abs(td_error) + 1e-6) ** self.alpha
            if importances is not None:
                importance_value = importances[offset] if offset < len(importances) else importances[-1]
                priority *= 0.5 + importance_value
            self.priorities[idx] = priority

    def get_most_important(self, n: int = 10) -> List[Experience]:
        if self.size == 0:
            return []
        scores = [
            (index, self.priorities[index] * (0.5 + self.buffer[index].importance))
            for index in range(self.size)
        ]
        scores.sort(key=lambda item: item[1], reverse=True)
        return [self.buffer[index] for index, _ in scores[:n]]

    def get_by_agent(self, agent_id: int, limit: int = 100) -> List[Experience]:
        return [experience for experience in self.buffer[: self.size] if experience.agent_id == agent_id][-limit:]

    def clear(self):
        self.buffer.clear()
        self.priorities.fill(0)
        self.size = 0
        self.position = 0
