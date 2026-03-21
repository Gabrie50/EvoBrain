import os
import sys
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from stage2_generation.agent_profile import AgentProfile
from stage2_generation.dynamic_generator import DynamicAgentGenerator


class MockLLM:
    def generate(self, prompt: str) -> str:
        return '{"name": "Agente Teste", "personality": "INTJ, analítico", "traits": ["analítico"], "mbti": "INTJ", "history": "Histórico de teste", "position": "neutro"}'


def test_agent_profile():
    profile = AgentProfile(id=1, name='Agente Teste', entity_name='Teste', personality='INTJ')
    assert profile.id == 1
    assert profile.accuracy == 0
    profile.update_stats(True)
    assert profile.acertos == 1
    assert profile.total_uso == 1


def test_dynamic_generator():
    generator = DynamicAgentGenerator(MockLLM(), max_agents=100)
    generator.start_generation_thread()
    generator.request_agent('Entidade Teste', 'Contexto de teste')
    time.sleep(0.7)
    assert generator.get_agent('Entidade Teste') is not None
    assert len(generator.get_all_agents()) >= 1
    generator.stop()
