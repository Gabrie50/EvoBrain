"""LLM via OpenAI API."""

from __future__ import annotations

from llm.base import BaseLLM
from utils.logger import get_logger

logger = get_logger(__name__)

try:
    from openai import OpenAI

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class OpenAILLM(BaseLLM):
    def __init__(self, model: str, api_key: str, base_url: str = "https://api.openai.com/v1", temperature: float = 0.7, max_tokens: int = 1000):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = None
        self._connected = False

    def connect(self) -> bool:
        if not OPENAI_AVAILABLE:
            logger.error("OpenAI não instalado. Instale com: pip install openai")
            return False
        try:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            self._connected = True
            logger.info("✅ Conectado à OpenAI API")
            return True
        except Exception as exc:
            logger.error(f"Erro ao conectar à OpenAI: {exc}")
            return False

    def is_connected(self) -> bool:
        return self._connected and self.client is not None

    def generate(self, prompt: str, temperature: float | None = None, max_tokens: int | None = None) -> str:
        if not self._connected and not self.connect():
            return self._fallback(prompt)
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
            )
            return response.choices[0].message.content
        except Exception as exc:
            logger.error(f"Erro na geração: {exc}")
        return self._fallback(prompt)

    def _fallback(self, prompt: str) -> str:
        del prompt
        return "OpenAI API indisponível"
