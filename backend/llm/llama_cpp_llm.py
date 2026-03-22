"""LLM via Llama.cpp."""

from __future__ import annotations

from llm.base import BaseLLM
from utils.logger import get_logger

logger = get_logger(__name__)

try:
    from llama_cpp import Llama

    LLAMA_CPP_AVAILABLE = True
except ImportError:
    LLAMA_CPP_AVAILABLE = False


class LlamaCppLLM(BaseLLM):
    def __init__(self, model_path: str, temperature: float = 0.7, max_tokens: int = 1000, n_ctx: int = 2048, n_threads: int = 4):
        self.model_path = model_path
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.n_ctx = n_ctx
        self.n_threads = n_threads
        self.model = None
        self._connected = False

    def connect(self) -> bool:
        if not LLAMA_CPP_AVAILABLE:
            logger.error("Llama.cpp não instalado. Instale com: pip install llama-cpp-python")
            return False
        try:
            self.model = Llama(model_path=self.model_path, n_ctx=self.n_ctx, n_threads=self.n_threads)
            self._connected = True
            logger.info(f"✅ Modelo Llama.cpp carregado: {self.model_path}")
            return True
        except Exception as exc:
            logger.error(f"Erro ao carregar modelo: {exc}")
            return False

    def is_connected(self) -> bool:
        return self._connected and self.model is not None

    def generate(self, prompt: str, temperature: float | None = None, max_tokens: int | None = None) -> str:
        if not self._connected and not self.connect():
            return self._fallback(prompt)
        try:
            output = self.model(
                prompt,
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature or self.temperature,
                echo=False,
            )
            return output["choices"][0]["text"]
        except Exception as exc:
            logger.error(f"Erro na geração: {exc}")
        return self._fallback(prompt)

    def _fallback(self, prompt: str) -> str:
        del prompt
        return "Llama.cpp indisponível"
