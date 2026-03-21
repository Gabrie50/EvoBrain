import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import numpy as np

from stage2_generation.agent_profile import AgentProfile
from stage3_simulation.neuroevolution import NeuroEvolution
from stage3_simulation.rl_agent import RLAgent
from stage3_simulation.state_extractor import StateExtractor


def test_rl_agent():
    profile = AgentProfile(id=1, name='TestAgent', entity_name='Test', personality='Test')
    agent = RLAgent(profile, state_size=150)
    state = np.random.randn(150).astype(np.float32)
    action, confidence = agent.decide(state)
    assert action in [0, 1]
    assert 0 <= confidence <= 1
    reward = agent.learn(action, 'BANKER', state)
    assert reward in [1.0, -0.5]


def test_neuroevolution():
    neuro = NeuroEvolution(population_size=10)
    class MockAgent:
        def __init__(self, idx):
            self.profile = AgentProfile(idx, f'Agent{idx}', f'Entity{idx}', 'Test')
            self.state_size = 150
            self.action_size = 2
            self.model = RLAgent(self.profile).model
            self.target_model = RLAgent(self.profile).target_model
    neuro.population = [MockAgent(i) for i in range(10)]
    neuro.evolve([50, 60, 70, 55, 65, 45, 80, 40, 75, 85])
    assert neuro.generation == 1
    assert len(neuro.population) == 10


def test_state_extractor():
    extractor = StateExtractor(state_size=150)
    history = [{'resultado': 'BANKER', 'player_score': 5, 'banker_score': 7}, {'resultado': 'PLAYER', 'player_score': 8, 'banker_score': 4}]
    state = extractor.extract(history)
    assert len(state) == 150
    assert isinstance(state, np.ndarray)
