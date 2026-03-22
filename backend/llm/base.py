"""Base para LLMs."""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseLLM(ABC):
    @abstractmethod
    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        pass

    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        pass
