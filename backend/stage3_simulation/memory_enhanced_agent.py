"""Agente RL com memória aprimorada."""

from __future__ import annotations

import time
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn

from config import settings
from stage2_generation.agent_profile import AgentProfile
from stage2_generation.memory_system import MemoryImportance, MemorySystem, MemoryType
from stage3_simulation.rl_agent import DQNNetwork, RLAgent
from utils.logger import get_logger

logger = get_logger(__name__)


class MemoryAugmentedNetwork(nn.Module):
    def __init__(self, state_size: int, memory_size: int = 128, action_size: int = 2):
        super().__init__()
        self.state_encoder = nn.Sequential(nn.Linear(state_size, 256), nn.ReLU(), nn.Dropout(0.2))
        self.memory_encoder = nn.Sequential(nn.Linear(memory_size, 128), nn.ReLU())
        self.combined = nn.Sequential(
            nn.Linear(256 + 128, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, action_size),
        )

    def forward(self, state, memory_embedding):
        state_features = self.state_encoder(state)
        memory_features = self.memory_encoder(memory_embedding)
        return self.combined(torch.cat([state_features, memory_features], dim=1))


class MemoryEnhancedAgent(RLAgent):
    def __init__(self, profile: AgentProfile, state_size: int = 150):
        super().__init__(profile, state_size)
        self.memory_system = MemorySystem(profile.id)
        self.memory_embedding_size = 128
        self.model = MemoryAugmentedNetwork(state_size, self.memory_embedding_size, self.action_size).to(self.device)
        self.target_model = MemoryAugmentedNetwork(state_size, self.memory_embedding_size, self.action_size).to(self.device)
        self.target_model.load_state_dict(self.model.state_dict())
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=settings.rl.learning_rate)
        self.decision_history: List[Dict] = []
        self.name_to_action = {action["name"]: action["id"] for action in settings.get_domain_actions()}
        logger.info(f"🧠 Agente com memória criado: {profile.name}")

    def _encode_memories(self, memories: List) -> torch.Tensor:
        if not memories:
            return torch.zeros(1, self.memory_embedding_size).to(self.device)

        import hashlib

        embedding = np.zeros(self.memory_embedding_size, dtype=np.float32)
        for index, memory in enumerate(memories[:5]):
            hash_val = int(hashlib.md5(memory.content.encode("utf-8")).hexdigest()[:8], 16)
            embedding[index % self.memory_embedding_size] = (hash_val % 100) / 100
        return torch.FloatTensor(embedding).unsqueeze(0).to(self.device)

    def decide(self, state: np.ndarray, context: Optional[Dict] = None) -> Tuple[int, float]:
        self.profile.total_uso += 1
        self._last_state = state
        query = context.get("query", "") if context else ""
        memories = self.memory_system.recall(query, limit=5)
        memory_embedding = self._encode_memories(memories)

        if np.random.random() < self.epsilon:
            action = int(np.random.randint(0, self.action_size))
            confidence = 0.5
        else:
            with torch.no_grad():
                state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
                q_values = self.model(state_tensor, memory_embedding).cpu().numpy()[0]
                action = int(np.argmax(q_values))
                confidence = min(
                    0.95,
                    0.5 + (float(np.max(q_values)) - float(np.min(q_values))) / (abs(float(np.max(q_values))) + 1e-8),
                )

        self._last_action = action
        self.decision_history.append(
            {
                "state": state,
                "action": action,
                "confidence": confidence,
                "timestamp": time.time(),
                "memories_used": len(memories),
            }
        )
        return action, confidence

    def learn(self, action: int, outcome: str, next_state: Optional[np.ndarray] = None) -> float:
        outcome_action = self.name_to_action.get(outcome, -1)
        if outcome_action == action:
            self.profile.acertos += 1
            reward = 1.0
        else:
            self.profile.erros += 1
            reward = -0.5

        if abs(reward) > 0.5:
            self.memory_system.remember(
                f"Quando {outcome} ocorreu, minha decisão foi {'certa' if reward > 0 else 'errada'}",
                MemoryType.PROCEDURAL,
                MemoryImportance.HIGH if reward > 0 else MemoryImportance.MEDIUM,
            )

        if self._last_state is not None and next_state is not None:
            next_memories = self.memory_system.recall(outcome, limit=5)
            next_memory_embedding = self._encode_memories(next_memories)
            current_memory_embedding = self._encode_memories(self.memory_system.recall("", limit=5))
            self._store_experience(
                self._last_state,
                action,
                reward,
                next_state,
                current_memory_embedding,
                next_memory_embedding,
            )

        if len(self.memory) >= settings.rl.batch_size:
            self._train_batch()
        if self.epsilon > settings.rl.epsilon_min:
            self.epsilon *= settings.rl.epsilon_decay
            self.profile.epsilon = self.epsilon
        return reward

    def _store_experience(self, state, action, reward, next_state, mem_embed, next_mem_embed):
        self.memory.append(
            (
                state.copy(),
                action,
                reward,
                next_state.copy(),
                mem_embed.cpu().numpy(),
                next_mem_embed.cpu().numpy(),
            )
        )
        if len(self.memory) > self.memory_size:
            self.memory.pop(0)

    def _train_batch(self, batch_size: Optional[int] = None):
        batch_size = batch_size or settings.rl.batch_size
        if len(self.memory) < batch_size:
            return

        batch = np.random.choice(len(self.memory), batch_size, replace=False)
        states, actions, rewards, next_states, mem_embeds, next_mem_embeds = [], [], [], [], [], []
        for index in batch:
            state, action, reward, next_state, mem_embed, next_mem_embed = self.memory[index]
            states.append(state)
            actions.append(action)
            rewards.append(reward)
            next_states.append(next_state)
            mem_embeds.append(mem_embed)
            next_mem_embeds.append(next_mem_embed)

        states = torch.FloatTensor(np.array(states)).to(self.device)
        actions = torch.LongTensor(actions).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        next_states = torch.FloatTensor(np.array(next_states)).to(self.device)
        mem_embeds = torch.FloatTensor(np.array(mem_embeds)).squeeze(1).to(self.device)
        next_mem_embeds = torch.FloatTensor(np.array(next_mem_embeds)).squeeze(1).to(self.device)

        current_q = self.model(states, mem_embeds).gather(1, actions.unsqueeze(1))
        with torch.no_grad():
            next_q = self.target_model(next_states, next_mem_embeds).max(1)[0]
            target_q = rewards + settings.rl.gamma * next_q

        loss = nn.MSELoss()(current_q.squeeze(), target_q)
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
        self.optimizer.step()

        for target_param, param in zip(self.target_model.parameters(), self.model.parameters()):
            target_param.data.copy_(0.001 * param.data + 0.999 * target_param.data)

    def get_memory_summary(self) -> Dict:
        return self.memory_system.get_summary()

    def get_stats(self) -> dict:
        stats = super().get_stats()
        stats.update({"memory": self.memory_system.get_summary(), "type": "MEMORY_ENHANCED"})
        return stats
