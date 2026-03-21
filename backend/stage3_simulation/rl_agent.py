import numpy as np
import torch
import torch.nn as nn
from typing import List, Optional, Tuple

from stage2_generation.agent_profile import AgentProfile
from utils.logger import get_logger

logger = get_logger(__name__)


class DQNNetwork(nn.Module):
    def __init__(self, state_size: int, action_size: int = 2):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(state_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, action_size),
        )

    def forward(self, x):
        return self.network(x)


class RLAgent:
    def __init__(self, profile: AgentProfile, state_size: int = 150, action_size: int = 2):
        self.profile = profile
        self.state_size = state_size
        self.action_size = action_size
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = DQNNetwork(state_size, action_size).to(self.device)
        self.target_model = DQNNetwork(state_size, action_size).to(self.device)
        self.target_model.load_state_dict(self.model.state_dict())
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        self.memory: List[tuple] = []
        self.memory_size = 10000
        self.epsilon = profile.epsilon
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.9995
        self.gamma = 0.99
        self._last_state: Optional[np.ndarray] = None

    def decide(self, state: np.ndarray) -> Tuple[int, float]:
        self._last_state = state
        if np.random.random() < self.epsilon:
            return int(np.random.randint(0, self.action_size)), 0.5
        with torch.no_grad():
            tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(self.device)
            q_values = self.model(tensor).cpu().numpy()[0]
        action = int(np.argmax(q_values))
        spread = float(np.max(q_values) - np.min(q_values))
        confidence = min(0.95, 0.5 + spread / (abs(float(np.max(q_values))) + 1e-8))
        return action, confidence

    def learn(self, action: int, outcome: str, next_state: Optional[np.ndarray] = None) -> float:
        outcome_int = 0 if outcome == "BANKER" else 1
        reward = 1.0 if action == outcome_int else -0.5
        if action == outcome_int:
            self.profile.acertos += 1
        else:
            self.profile.erros += 1
        if self._last_state is not None and next_state is not None:
            self.memory.append((self._last_state.copy(), action, reward, next_state.copy()))
            if len(self.memory) > self.memory_size:
                self.memory.pop(0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            self.profile.epsilon = self.epsilon
        return reward

    def get_stats(self) -> dict:
        return {"name": self.profile.name, "acertos": self.profile.acertos, "erros": self.profile.erros, "total": self.profile.total_uso, "accuracy": self.profile.accuracy, "epsilon": round(self.epsilon, 3), "memory_size": len(self.memory), "personality": self.profile.personality[:50]}
