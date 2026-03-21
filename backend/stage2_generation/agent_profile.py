import time
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class AgentProfile:
    id: int
    name: str
    entity_name: str
    personality: str
    traits: List[str] = field(default_factory=list)
    mbti: str = "INTJ"
    history: str = ""
    memory: List[str] = field(default_factory=list)
    long_term_memory: List[str] = field(default_factory=list)
    relationships: Dict[str, float] = field(default_factory=dict)
    position: str = "neutro"
    ideology: Dict[str, float] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    last_active: float = field(default_factory=time.time)
    generation: int = 0
    acertos: int = 0
    erros: int = 0
    total_uso: int = 0
    epsilon: float = 0.3
    weight: float = 1.0
    specializations: List[str] = field(default_factory=list)
    discovered_patterns: List[str] = field(default_factory=list)

    def update_stats(self, acertou: bool):
        self.last_active = time.time()
        self.total_uso += 1
        if acertou:
            self.acertos += 1
        else:
            self.erros += 1

    @property
    def accuracy(self) -> float:
        return (self.acertos / self.total_uso) * 100 if self.total_uso else 0.0

    @property
    def fitness(self) -> float:
        return min(100.0, self.accuracy + len(self.specializations) * 5)

    def to_dict(self) -> dict:
        return self.__dict__.copy()
