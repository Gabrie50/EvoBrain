"""Evolução baseada em memória e herança de conhecimento."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List

import torch

from stage2_generation.agent_profile import AgentProfile
from stage2_generation.memory_system import MemoryImportance
from stage3_simulation.memory_enhanced_agent import MemoryEnhancedAgent
from stage3_simulation.memory_ranking import MemoryRanker
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class GeneticHeritage:
    parent_id: int
    memory_ids: List[str]
    strategy_weights: Dict[str, float]
    success_rate: float
    generation: int


class EvolutionaryMemory:
    def __init__(self, memory_ranker: MemoryRanker):
        self.memory_ranker = memory_ranker
        self.genetic_pool: List[GeneticHeritage] = []
        self.generation = 0
        logger.info("🧬 EvolutionaryMemory inicializado")

    def select_fittest(self, agents: List[MemoryEnhancedAgent], top_k: int = 10) -> List[MemoryEnhancedAgent]:
        scored_agents = []
        for agent in agents:
            perf_score = agent.profile.accuracy / 100
            top_memories = self.memory_ranker.get_top_memories(agent.profile.id, 5)
            memory_score = sum(memory.total_score for memory in top_memories) / 5 if top_memories else 0
            scored_agents.append((agent, 0.7 * perf_score + 0.3 * memory_score))
        scored_agents.sort(key=lambda item: item[1], reverse=True)
        return [agent for agent, _ in scored_agents[:top_k]]

    def create_offspring(
        self,
        parent1: MemoryEnhancedAgent,
        parent2: MemoryEnhancedAgent,
        mutation_rate: float = 0.1,
    ) -> MemoryEnhancedAgent:
        new_id = max(parent1.profile.id, parent2.profile.id) + 1
        new_name = f"Offspring_{parent1.profile.name[:5]}_{parent2.profile.name[:5]}"
        new_profile = AgentProfile(
            id=new_id,
            name=new_name,
            entity_name=f"Herdeiro de {parent1.profile.entity_name} e {parent2.profile.entity_name}",
            personality=f"Herda de {parent1.profile.personality[:30]} e {parent2.profile.personality[:30]}",
            traits=list(set(parent1.profile.traits + parent2.profile.traits))[:3],
            mbti=random.choice([parent1.profile.mbti, parent2.profile.mbti]),
            history=f"Evoluído da geração {self.generation}",
        )
        offspring = MemoryEnhancedAgent(new_profile, parent1.state_size)
        self._inherit_memories(offspring, parent1, parent2)
        self._crossover_weights(offspring, parent1, parent2)
        if random.random() < mutation_rate:
            self._mutate(offspring)
        self.genetic_pool.append(
            GeneticHeritage(
                parent_id=parent1.profile.id,
                memory_ids=[memory.id for memory in offspring.memory_system.long_term.memories.values()][:10],
                strategy_weights={},
                success_rate=(parent1.profile.accuracy + parent2.profile.accuracy) / 200,
                generation=self.generation,
            )
        )
        logger.info(f"🧬 Novo agente criado: {new_name}")
        return offspring

    def _inherit_memories(self, offspring, parent1, parent2):
        parent1_memories = self.memory_ranker.get_top_memories(parent1.profile.id, 10)
        parent2_memories = self.memory_ranker.get_top_memories(parent2.profile.id, 10)
        combined = sorted(parent1_memories + parent2_memories, key=lambda item: item.total_score, reverse=True)
        for ranked in combined[:20]:
            offspring.memory_system.remember(
                content=ranked.memory.content,
                memory_type=ranked.memory.memory_type,
                importance=MemoryImportance(min(4, int(ranked.total_score * 4) + 1)),
                related_agents=ranked.memory.related_agents,
            )

    def _crossover_weights(self, offspring, parent1, parent2):
        with torch.no_grad():
            for param1, param2, child_param in zip(
                parent1.model.parameters(),
                parent2.model.parameters(),
                offspring.model.parameters(),
            ):
                child_param.data = 0.6 * param1.data + 0.4 * param2.data
        offspring.target_model.load_state_dict(offspring.model.state_dict())

    def _mutate(self, agent, mutation_strength: float = 0.05):
        with torch.no_grad():
            for param in agent.model.parameters():
                param.add_(torch.randn_like(param) * mutation_strength)

    def evolve_generation(
        self,
        agents: List[MemoryEnhancedAgent],
        keep_best: int = 10,
        offspring_count: int = 50,
    ) -> List[MemoryEnhancedAgent]:
        self.generation += 1
        logger.info(f"🧬 EVOLUÇÃO GERAÇÃO {self.generation}")
        fittest = self.select_fittest(agents, keep_best)
        new_population = list(fittest)
        for _ in range(offspring_count):
            parent1 = random.choice(fittest)
            parent2 = random.choice(fittest)
            while parent2 == parent1 and len(fittest) > 1:
                parent2 = random.choice(fittest)
            new_population.append(self.create_offspring(parent1, parent2))
        logger.info(f"   ✅ Geração {self.generation}: {len(fittest)} mantidos, {offspring_count} criados")
        return new_population[: len(agents)]
