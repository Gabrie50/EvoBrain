"""
Configuração unificada do EvoBrain
Carrega de variáveis de ambiente
"""

import json
import os
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List

from dotenv import load_dotenv

load_dotenv()


@dataclass
class DomainConfig:
    type: str = "bacbo"
    name: str = "Bac Bo"
    description: str = "Jogo de dados Bac Bo"
    actions: List[Dict] = field(default_factory=lambda: [
        {"id": 0, "name": "BANKER", "color": "🔴", "emoji": "🔴"},
        {"id": 1, "name": "PLAYER", "color": "🔵", "emoji": "🔵"},
        {"id": 2, "name": "TIE", "color": "🟡", "emoji": "🟡"},
    ])


@dataclass
class LLMConfig:
    type: str = "ollama"
    model: str = "llama3.2"
    host: str = "http://localhost:11434"
    api_key: str = ""
    temperature: float = 0.7
    max_tokens: int = 1000
    timeout: int = 30


@dataclass
class DataSourceConfig:
    type: str = "bacbo"
    enabled: bool = True
    interval: float = 0.5
    rest_url: str = ""
    rest_method: str = "GET"
    rest_headers: Dict = field(default_factory=dict)
    rest_params: Dict = field(default_factory=dict)
    ws_url: str = ""
    ws_headers: Dict = field(default_factory=dict)
    bacbo_api_url: str = "https://api-cs.casino.org/svc-evolution-game-events/api/bacbo"
    bacbo_ws_url: str = "wss://api-cs.casino.org/svc-evolution-game-events/ws/bacbo"


@dataclass
class AgentsConfig:
    max_agents: int = 10000
    state_size: int = 150
    creation_delay: float = 0.5
    initial_agents: int = 100


@dataclass
class RLConfig:
    learning_rate: float = 0.001
    gamma: float = 0.99
    epsilon_start: float = 0.3
    epsilon_min: float = 0.05
    epsilon_decay: float = 0.9995
    batch_size: int = 64
    memory_size: int = 10000


@dataclass
class ReplayConfig:
    capacity: int = 100000
    alpha: float = 0.6
    beta: float = 0.4


@dataclass
class NeuroevolutionConfig:
    mutation_rate: float = 0.1
    elite_percent: float = 0.2
    crossover_rate: float = 0.7
    population_size: int = 1000


@dataclass
class MemoryConfig:
    episodic_size: int = 100
    long_term_size: int = 10000
    decay_rate: float = 0.01
    consolidation_threshold: float = 0.7


@dataclass
class CompetitionConfig:
    elo_k: int = 32
    keep_ratio: float = 0.3
    tournament_rounds: int = 3


@dataclass
class ContinuousLearningConfig:
    enabled: bool = True
    upload_dir: str = "uploads"
    interval: int = 5


@dataclass
class DatabaseConfig:
    enabled: bool = False
    url: str = ""


@dataclass
class APIConfig:
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    cors_origins: List[str] = field(default_factory=lambda: ["http://localhost:3000"])


@dataclass
class FrontendConfig:
    url: str = "http://localhost:3000"
    title: str = "EvoBrain"
    theme: str = "dark"


class Settings:
    def __init__(self):
        self.domain = DomainConfig()
        self.llm = LLMConfig()
        self.data_source = DataSourceConfig()
        self.agents = AgentsConfig()
        self.rl = RLConfig()
        self.replay = ReplayConfig()
        self.neuroevolution = NeuroevolutionConfig()
        self.memory = MemoryConfig()
        self.competition = CompetitionConfig()
        self.continuous_learning = ContinuousLearningConfig()
        self.database = DatabaseConfig()
        self.api = APIConfig()
        self.frontend = FrontendConfig()
        self._load_from_env()

    def _load_from_env(self):
        if os.getenv("DOMAIN_TYPE"):
            self.domain.type = os.getenv("DOMAIN_TYPE")
        if os.getenv("DOMAIN_NAME"):
            self.domain.name = os.getenv("DOMAIN_NAME")
        if os.getenv("DOMAIN_DESCRIPTION"):
            self.domain.description = os.getenv("DOMAIN_DESCRIPTION")
        if os.getenv("DOMAIN_ACTIONS"):
            try:
                self.domain.actions = json.loads(os.getenv("DOMAIN_ACTIONS"))
            except Exception:
                pass
        if os.getenv("LLM_TYPE"):
            self.llm.type = os.getenv("LLM_TYPE")
        if os.getenv("LLM_MODEL"):
            self.llm.model = os.getenv("LLM_MODEL")
        if os.getenv("LLM_HOST"):
            self.llm.host = os.getenv("LLM_HOST")
        if os.getenv("LLM_API_KEY"):
            self.llm.api_key = os.getenv("LLM_API_KEY")
        if os.getenv("LLM_TEMPERATURE"):
            self.llm.temperature = float(os.getenv("LLM_TEMPERATURE"))
        if os.getenv("LLM_MAX_TOKENS"):
            self.llm.max_tokens = int(os.getenv("LLM_MAX_TOKENS"))
        if os.getenv("LLM_TIMEOUT"):
            self.llm.timeout = int(os.getenv("LLM_TIMEOUT"))
        if os.getenv("DATA_SOURCE_TYPE"):
            self.data_source.type = os.getenv("DATA_SOURCE_TYPE")
        if os.getenv("DATA_SOURCE_INTERVAL"):
            self.data_source.interval = float(os.getenv("DATA_SOURCE_INTERVAL"))
        if os.getenv("DATA_SOURCE_REST_URL"):
            self.data_source.rest_url = os.getenv("DATA_SOURCE_REST_URL")
        if os.getenv("DATA_SOURCE_WS_URL"):
            self.data_source.ws_url = os.getenv("DATA_SOURCE_WS_URL")
        if os.getenv("MAX_AGENTS"):
            self.agents.max_agents = int(os.getenv("MAX_AGENTS"))
        if os.getenv("STATE_SIZE"):
            self.agents.state_size = int(os.getenv("STATE_SIZE"))
        if os.getenv("LEARNING_RATE"):
            self.rl.learning_rate = float(os.getenv("LEARNING_RATE"))
        if os.getenv("MUTATION_RATE"):
            self.neuroevolution.mutation_rate = float(os.getenv("MUTATION_RATE"))
        if os.getenv("API_PORT"):
            self.api.port = int(os.getenv("API_PORT"))
        if os.getenv("DATABASE_ENABLED"):
            self.database.enabled = os.getenv("DATABASE_ENABLED", "false").lower() == "true"
        if os.getenv("DATABASE_URL"):
            self.database.url = os.getenv("DATABASE_URL")

    def get_domain_actions(self) -> List[Dict]:
        return self.domain.actions

    def get_action_name(self, action_id: int) -> str:
        for action in self.domain.actions:
            if action["id"] == action_id:
                return action["name"]
        return f"UNKNOWN_{action_id}"

    def get_action_id(self, action_name: str) -> int:
        for action in self.domain.actions:
            if action["name"] == action_name:
                return action["id"]
        return -1

    def to_dict(self) -> dict:
        return {
            "domain": asdict(self.domain),
            "llm": asdict(self.llm),
            "data_source": asdict(self.data_source),
            "agents": asdict(self.agents),
            "rl": asdict(self.rl),
            "replay": asdict(self.replay),
            "neuroevolution": asdict(self.neuroevolution),
            "memory": asdict(self.memory),
            "competition": asdict(self.competition),
            "continuous_learning": asdict(self.continuous_learning),
            "database": asdict(self.database),
            "api": asdict(self.api),
            "frontend": asdict(self.frontend),
        }


settings = Settings()
