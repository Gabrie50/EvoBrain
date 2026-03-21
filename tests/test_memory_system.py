import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import numpy as np

from stage2_generation.memory_system import MemoryImportance, MemorySystem, MemoryType
from stage3_simulation.agent_competition import AgentCompetition
from stage3_simulation.memory_enhanced_agent import MemoryEnhancedAgent
from stage3_simulation.memory_ranking import MemoryRanker
from stage3_simulation.prioritized_replay import Experience, PrioritizedReplayBuffer
from stage2_generation.agent_profile import AgentProfile


def build_agent(agent_id: int, name: str) -> MemoryEnhancedAgent:
    profile = AgentProfile(id=agent_id, name=name, entity_name=name, personality='Analítico')
    return MemoryEnhancedAgent(profile, state_size=150)


def test_memory_system_remember_and_recall():
    memory_system = MemorySystem(agent_id=7)
    memory_system.remember('Vitória recente', MemoryType.EPISODIC, MemoryImportance.HIGH)
    procedural = memory_system.remember('Padrão consolidado', MemoryType.PROCEDURAL, MemoryImportance.CRITICAL)

    recalled = memory_system.recall('Padrão', limit=5)

    assert any(memory.id == procedural.id for memory in recalled)
    assert memory_system.get_summary()['long_term_count'] == 1
    assert memory_system.get_summary()['working_memory_size'] >= 1


def test_prioritized_replay_buffer_sampling_and_update():
    buffer = PrioritizedReplayBuffer(capacity=10)
    for idx in range(4):
        buffer.push(
            Experience(
                state=np.zeros(3),
                action=idx % 2,
                reward=float(idx),
                next_state=np.ones(3),
                done=False,
                td_error=0.1 + idx,
                importance=0.6,
                agent_id=idx,
            )
        )

    experiences, weights, indices = buffer.sample(2)
    buffer.update_priorities(indices, np.array([0.9, 0.4]), np.array([0.7, 0.8]))

    assert len(experiences) == 2
    assert len(weights) == 2
    assert len(indices) == 2
    assert len(buffer.get_most_important(2)) == 2


def test_memory_ranker_and_competition_work_together():
    ranker = MemoryRanker()
    agent1 = build_agent(1, 'AgentOne')
    agent2 = build_agent(2, 'AgentTwo')

    memory = agent1.memory_system.remember('Aprendi uma boa estratégia', MemoryType.EPISODIC, MemoryImportance.HIGH)
    ranked = ranker.rank_memory(memory, reward=1.0, social_impact=0.2)
    ranker.record_usage(memory.id, True)
    ranker.consolidate_important_memories(threshold=0.2)

    competition = AgentCompetition(ranker)
    winner, score1, score2 = competition.compete(agent1, agent2, test_episodes=5)

    assert ranked.total_score > 0
    assert winner in [agent1, agent2]
    assert 0 <= score1 <= 1
    assert 0 <= score2 <= 1
    assert competition.get_statistics()['total_matches'] == 0
