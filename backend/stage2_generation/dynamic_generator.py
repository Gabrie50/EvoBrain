import json
import threading
import time
from collections import deque
from typing import Deque, Dict, Optional, Tuple

from llm.local_llm import LocalLLM
from stage2_generation.agent_profile import AgentProfile
from utils.logger import get_logger

logger = get_logger(__name__)


class DynamicAgentGenerator:
    def __init__(self, llm: LocalLLM, max_agents: int = 10000, creation_delay: float = 0.5):
        self.llm = llm
        self.max_agents = max_agents
        self.creation_delay = creation_delay
        self.agents: Dict[str, AgentProfile] = {}
        self.agent_counter = 0
        self.pending_generation: Deque[Tuple[str, str, int]] = deque()
        self.generation_thread: Optional[threading.Thread] = None
        self._stop_generation = False

    def start_generation_thread(self):
        if self.generation_thread and self.generation_thread.is_alive():
            return
        self.generation_thread = threading.Thread(target=self._generation_worker, daemon=True)
        self.generation_thread.start()

    def request_agent(self, entity_name: str, context: str = "", priority: int = 1) -> Optional[str]:
        if entity_name in self.agents:
            self.agents[entity_name].last_active = time.time()
            return entity_name
        if len(self.agents) >= self.max_agents:
            logger.warning("Limite de agentes atingido")
            return None
        self.pending_generation.append((entity_name, context, priority))
        return entity_name

    def _generation_worker(self):
        while not self._stop_generation:
            if not self.pending_generation:
                time.sleep(0.05)
                continue
            items = sorted(self.pending_generation, key=lambda item: item[2], reverse=True)
            self.pending_generation = deque(items)
            entity_name, context, _ = self.pending_generation.popleft()
            self._create_agent(entity_name, context)
            time.sleep(self.creation_delay)

    def _create_agent(self, entity_name: str, context: str) -> AgentProfile:
        response = self.llm.generate(self._build_creation_prompt(entity_name, context))
        profile_data = self._parse_profile_response(response, entity_name)
        agent = AgentProfile(
            id=self.agent_counter,
            name=profile_data.get("name", entity_name),
            entity_name=entity_name,
            personality=profile_data.get("personality", "INTJ, analítico, cauteloso"),
            traits=profile_data.get("traits", ["analítico"]),
            mbti=profile_data.get("mbti", "INTJ"),
            history=profile_data.get("history", f"Agente baseado em {entity_name}"),
            position=profile_data.get("position", "neutro"),
            ideology=profile_data.get("ideology", {}),
        )
        self.agents[entity_name] = agent
        self.agent_counter += 1
        return agent

    def _build_creation_prompt(self, entity_name: str, context: str) -> str:
        return f"Crie um perfil de agente em JSON para {entity_name}. Contexto: {context[:500]}"

    def _parse_profile_response(self, response: str, default_name: str) -> dict:
        try:
            import re
            match = re.search(r"\{.*\}", response, re.DOTALL)
            if match:
                return json.loads(match.group())
        except json.JSONDecodeError:
            pass
        return {"name": default_name, "personality": "ISTJ, prático, conservador, analítico", "traits": ["prático", "conservador", "analítico"], "mbti": "ISTJ", "history": f"Agente baseado em {default_name}", "position": "neutro", "ideology": {}}

    def get_agent(self, name: str) -> Optional[AgentProfile]:
        return self.agents.get(name)

    def get_all_agents(self):
        return list(self.agents.values())

    def get_stats(self) -> dict:
        now = time.time()
        recent = [agent for agent in self.agents.values() if now - agent.created_at < 60]
        return {"total_agents": len(self.agents), "pending": len(self.pending_generation), "max_agents": self.max_agents, "created_last_minute": len(recent), "total_ever": len(self.agents), "active_agents": len([agent for agent in self.agents.values() if agent.total_uso > 0])}

    def stop(self):
        self._stop_generation = True
        if self.generation_thread:
            self.generation_thread.join(timeout=2)
