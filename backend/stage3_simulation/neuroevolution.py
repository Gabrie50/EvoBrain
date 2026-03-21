from collections import deque
from typing import List, Optional

import numpy as np
import torch

from stage2_generation.agent_profile import AgentProfile
from stage3_simulation.rl_agent import RLAgent
from utils.logger import get_logger

logger = get_logger(__name__)


class NeuroEvolution:
    def __init__(self, population_size: int = 1000, mutation_rate: float = 0.1, elite_percent: float = 0.2):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.elite_percent = elite_percent
        self.population: List[RLAgent] = []
        self.generation = 0
        self.best_agent: Optional[RLAgent] = None
        self.best_fitness = 0.0
        self.fitness_history = deque(maxlen=100)

    def evolve(self, fitness: List[float]):
        if len(self.population) < 2:
            return
        indices = np.argsort(fitness)[::-1]
        best_idx = int(indices[0])
        self.best_fitness = max(self.best_fitness, float(fitness[best_idx]))
        self.best_agent = self.population[best_idx]
        self.fitness_history.append(float(fitness[best_idx]))
        elite_size = max(1, int(len(self.population) * self.elite_percent))
        elite = [self.population[int(i)] for i in indices[:elite_size]]
        new_population = elite.copy()
        while len(new_population) < len(self.population):
            parent1 = np.random.choice(elite)
            parent2 = np.random.choice(elite)
            new_population.append(self._crossover(parent1, parent2))
        self.population = new_population[: len(self.population)]
        self.generation += 1

    def _crossover(self, parent1: RLAgent, parent2: RLAgent) -> RLAgent:
        child = RLAgent(parent1.profile, parent1.state_size, parent1.action_size)
        with torch.no_grad():
            for p1, p2, cp in zip(parent1.model.parameters(), parent2.model.parameters(), child.model.parameters()):
                cp.data = 0.6 * p1.data + 0.4 * p2.data
        child.target_model.load_state_dict(child.model.state_dict())
        return child

    def get_stats(self) -> dict:
        return {"generation": self.generation, "population_size": len(self.population), "best_fitness": round(self.best_fitness, 2), "fitness_history": list(self.fitness_history)[-10:], "mutation_rate": self.mutation_rate, "elite_percent": self.elite_percent}
