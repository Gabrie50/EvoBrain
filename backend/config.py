from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações do sistema."""

    LLM_MODEL: str = "llama3.2"
    LLM_HOST: str = "http://localhost:11434"
    LLM_TIMEOUT: int = 30

    MAX_AGENTS: int = 10000
    STATE_SIZE: int = 150
    AGENT_CREATION_DELAY: float = 0.5

    LEARNING_RATE: float = 0.001
    GAMMA: float = 0.99
    EPSILON_START: float = 0.3
    EPSILON_MIN: float = 0.05
    EPSILON_DECAY: float = 0.9995
    BATCH_SIZE: int = 64
    MEMORY_SIZE: int = 10000

    MUTATION_RATE: float = 0.1
    ELITE_PERCENT: float = 0.2
    CROSSOVER_RATE: float = 0.7

    PREDICTION_INTERVAL: float = 0.5
    HISTORY_SIZE: int = 5000
    FEEDBACK_DELAY: float = 0.1

    DATABASE_URL: Optional[str] = None

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 1

    FRONTEND_URL: str = "http://localhost:3000"

    BACBO_API_URL: str = "https://api-cs.casino.org/svc-evolution-game-events/api/bacbo"
    BACBO_WS_URL: str = "wss://api-cs.casino.org/svc-evolution-game-events/ws/bacbo"
    API_TIMEOUT: int = 5
    API_RETRIES: int = 3

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
