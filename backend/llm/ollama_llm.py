"""LLM via Ollama."""

from __future__ import annotations

import requests

from llm.base import BaseLLM
from utils.logger import get_logger

logger = get_logger(__name__)


class OllamaLLM(BaseLLM):
    def __init__(self, model: str, host: str = "http://localhost:11434", temperature: float = 0.7, max_tokens: int = 1000, timeout: int = 30):
        self.model = model
        self.host = host
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.session = requests.Session()
        self._connected = False

    def connect(self) -> bool:
        try:
            response = self.session.get(f"{self.host}/api/tags", timeout=5)
            if response.status_code == 200:
                self._connected = True
                logger.info("✅ Conectado ao Ollama")
                return True
        except Exception as exc:
            logger.error(f"Erro ao conectar ao Ollama: {exc}")
        return False

    def is_connected(self) -> bool:
        return self._connected

    def generate(self, prompt: str, temperature: float | None = None, max_tokens: int | None = None) -> str:
        if not self._connected and not self.connect():
            return self._fallback(prompt)
        try:
            response = self.session.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": temperature or self.temperature,
                    "max_tokens": max_tokens or self.max_tokens,
                },
                timeout=self.timeout,
            )
            if response.status_code == 200:
                return response.json().get("response", "")
        except Exception as exc:
            logger.error(f"Erro na geração: {exc}")
        return self._fallback(prompt)

    def _fallback(self, prompt: str) -> str:
        if "extraia" in prompt.lower():
            return '{"entities": []}'
        return "LLM local indisponível"
