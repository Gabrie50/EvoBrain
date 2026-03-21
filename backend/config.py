"""
Configuração unificada do EvoBrain.
Carrega variáveis de ambiente e, opcionalmente, YAML do usuário.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List

import yaml
from dotenv import load_dotenv

load_dotenv()


@dataclass
class DomainConfig:
    type: str = "custom"
    name: str = "Domínio Customizado"
    description: str = "Configure suas próprias ações"
    actions: List[Dict[str, Any]] = field(
        default_factory=lambda: [
            {"id": 0, "name": "ACAO_A", "color": "🔴", "emoji": "🔴"},
            {"id": 1, "name": "ACAO_B", "color": "🔵", "emoji": "🔵"},
        ]
    )


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
    type: str = "custom"
    enabled: bool = True
    interval: float = 0.5
    rest_url: str = ""
    rest_method: str = "GET"
    rest_headers: Dict[str, Any] = field(default_factory=dict)
    rest_params: Dict[str, Any] = field(default_factory=dict)
    rest_mapping: Dict[str, Any] = field(default_factory=dict)
    ws_url: str = ""
    ws_headers: Dict[str, Any] = field(default_factory=dict)
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
        self._load_from_yaml()

    def _get_json(self, key: str, default: Any) -> Any:
        raw = os.getenv(key)
        if not raw:
            return default
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return default

    def _load_from_env(self):
        self.domain.type = os.getenv("DOMAIN_TYPE", self.domain.type)
        self.domain.name = os.getenv("DOMAIN_NAME", self.domain.name)
        self.domain.description = os.getenv("DOMAIN_DESCRIPTION", self.domain.description)
        self.domain.actions = self._get_json("DOMAIN_ACTIONS", self.domain.actions)

        self.llm.type = os.getenv("LLM_TYPE", self.llm.type)
        self.llm.model = os.getenv("LLM_MODEL", self.llm.model)
        self.llm.host = os.getenv("LLM_HOST", self.llm.host)
        self.llm.api_key = os.getenv("LLM_API_KEY", self.llm.api_key)
        self.llm.temperature = float(os.getenv("LLM_TEMPERATURE", self.llm.temperature))
        self.llm.max_tokens = int(os.getenv("LLM_MAX_TOKENS", self.llm.max_tokens))
        self.llm.timeout = int(os.getenv("LLM_TIMEOUT", self.llm.timeout))

        self.data_source.type = os.getenv("DATA_SOURCE_TYPE", self.data_source.type)
        self.data_source.enabled = os.getenv("DATA_SOURCE_ENABLED", str(self.data_source.enabled)).lower() == "true"
        self.data_source.interval = float(os.getenv("DATA_SOURCE_INTERVAL", self.data_source.interval))
        self.data_source.rest_url = os.getenv("DATA_SOURCE_REST_URL", self.data_source.rest_url)
        self.data_source.rest_method = os.getenv("DATA_SOURCE_REST_METHOD", self.data_source.rest_method)
        self.data_source.rest_headers = self._get_json("DATA_SOURCE_REST_HEADERS", self.data_source.rest_headers)
        self.data_source.rest_params = self._get_json("DATA_SOURCE_REST_PARAMS", self.data_source.rest_params)
        self.data_source.rest_mapping = self._get_json("DATA_SOURCE_REST_MAPPING", self.data_source.rest_mapping)
        self.data_source.ws_url = os.getenv("DATA_SOURCE_WS_URL", self.data_source.ws_url)
        self.data_source.ws_headers = self._get_json("DATA_SOURCE_WS_HEADERS", self.data_source.ws_headers)

        self.agents.max_agents = int(os.getenv("MAX_AGENTS", self.agents.max_agents))
        self.agents.state_size = int(os.getenv("STATE_SIZE", self.agents.state_size))
        self.agents.creation_delay = float(os.getenv("AGENT_CREATION_DELAY", self.agents.creation_delay))
        self.agents.initial_agents = int(os.getenv("INITIAL_AGENTS", self.agents.initial_agents))

        self.rl.learning_rate = float(os.getenv("LEARNING_RATE", self.rl.learning_rate))
        self.rl.gamma = float(os.getenv("GAMMA", self.rl.gamma))
        self.rl.epsilon_start = float(os.getenv("EPSILON_START", self.rl.epsilon_start))
        self.rl.epsilon_min = float(os.getenv("EPSILON_MIN", self.rl.epsilon_min))
        self.rl.epsilon_decay = float(os.getenv("EPSILON_DECAY", self.rl.epsilon_decay))
        self.rl.batch_size = int(os.getenv("BATCH_SIZE", self.rl.batch_size))
        self.rl.memory_size = int(os.getenv("MEMORY_SIZE", self.rl.memory_size))

        self.replay.capacity = int(os.getenv("REPLAY_BUFFER_SIZE", self.replay.capacity))
        self.replay.alpha = float(os.getenv("REPLAY_ALPHA", self.replay.alpha))
        self.replay.beta = float(os.getenv("REPLAY_BETA", self.replay.beta))

        self.neuroevolution.mutation_rate = float(os.getenv("MUTATION_RATE", self.neuroevolution.mutation_rate))
        self.neuroevolution.elite_percent = float(os.getenv("ELITE_PERCENT", self.neuroevolution.elite_percent))
        self.neuroevolution.crossover_rate = float(os.getenv("CROSSOVER_RATE", self.neuroevolution.crossover_rate))
        self.neuroevolution.population_size = int(os.getenv("POPULATION_SIZE", self.neuroevolution.population_size))

        self.memory.episodic_size = int(os.getenv("EPISODIC_MEMORY_SIZE", self.memory.episodic_size))
        self.memory.long_term_size = int(os.getenv("LONG_TERM_MEMORY_SIZE", self.memory.long_term_size))
        self.memory.decay_rate = float(os.getenv("MEMORY_DECAY_RATE", self.memory.decay_rate))
        self.memory.consolidation_threshold = float(os.getenv("MEMORY_CONSOLIDATION_THRESHOLD", self.memory.consolidation_threshold))

        self.competition.elo_k = int(os.getenv("COMPETITION_ELO_K", self.competition.elo_k))
        self.competition.keep_ratio = float(os.getenv("COMPETITION_KEEP_RATIO", self.competition.keep_ratio))
        self.competition.tournament_rounds = int(os.getenv("TOURNAMENT_ROUNDS", self.competition.tournament_rounds))

        self.continuous_learning.upload_dir = os.getenv("UPLOAD_DIR", self.continuous_learning.upload_dir)
        self.continuous_learning.enabled = os.getenv("CONTINUOUS_LEARNING_ENABLED", str(self.continuous_learning.enabled)).lower() == "true"
        self.continuous_learning.interval = int(os.getenv("CONTINUOUS_LEARNING_INTERVAL", self.continuous_learning.interval))

        self.database.enabled = os.getenv("DATABASE_ENABLED", str(self.database.enabled)).lower() == "true"
        self.database.url = os.getenv("DATABASE_URL", self.database.url)

        self.api.host = os.getenv("API_HOST", self.api.host)
        self.api.port = int(os.getenv("API_PORT", self.api.port))
        self.api.workers = int(os.getenv("API_WORKERS", self.api.workers))
        self.api.cors_origins = self._get_json("API_CORS_ORIGINS", self.api.cors_origins)

        self.frontend.url = os.getenv("FRONTEND_URL", self.frontend.url)
        self.frontend.title = os.getenv("FRONTEND_TITLE", self.frontend.title)
        self.frontend.theme = os.getenv("FRONTEND_THEME", self.frontend.theme)

    def _load_from_yaml(self):
        yaml_path = Path("config/user_config.yml")
        if not yaml_path.exists():
            return
        with yaml_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        self._merge_dict(data)

    def _merge_dict(self, data: Dict[str, Any]):
        for key, value in data.items():
            if not hasattr(self, key):
                continue
            current = getattr(self, key)
            if hasattr(current, "__dataclass_fields__") and isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if hasattr(current, subkey):
                        setattr(current, subkey, subvalue)

    def get_domain_actions(self) -> List[Dict[str, Any]]:
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

    def get_action_emoji(self, action_name: str) -> str:
        for action in self.domain.actions:
            if action["name"] == action_name:
                return action.get("emoji", action.get("color", "⚪"))
        return "⚪"

    def to_dict(self) -> Dict[str, Any]:
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

    def __getattr__(self, name: str) -> Any:
        compatibility_map = {
            "LLM_MODEL": self.llm.model,
            "LLM_HOST": self.llm.host,
            "LLM_TIMEOUT": self.llm.timeout,
            "MAX_AGENTS": self.agents.max_agents,
            "STATE_SIZE": self.agents.state_size,
            "AGENT_CREATION_DELAY": self.agents.creation_delay,
            "LEARNING_RATE": self.rl.learning_rate,
            "GAMMA": self.rl.gamma,
            "EPSILON_START": self.rl.epsilon_start,
            "EPSILON_MIN": self.rl.epsilon_min,
            "EPSILON_DECAY": self.rl.epsilon_decay,
            "BATCH_SIZE": self.rl.batch_size,
            "MEMORY_SIZE": self.rl.memory_size,
            "MUTATION_RATE": self.neuroevolution.mutation_rate,
            "ELITE_PERCENT": self.neuroevolution.elite_percent,
            "CROSSOVER_RATE": self.neuroevolution.crossover_rate,
            "DATABASE_URL": self.database.url,
            "API_HOST": self.api.host,
            "API_PORT": self.api.port,
            "API_WORKERS": self.api.workers,
            "FRONTEND_URL": self.frontend.url,
            "BACBO_API_URL": self.data_source.bacbo_api_url,
            "BACBO_WS_URL": self.data_source.bacbo_ws_url,
            "HISTORY_SIZE": 5000,
        }
        if name in compatibility_map:
            return compatibility_map[name]
        raise AttributeError(name)


settings = Settings()
