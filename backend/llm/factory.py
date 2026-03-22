"""Fábrica de LLMs."""

from __future__ import annotations

from typing import Optional

from config import settings
from llm.base import BaseLLM
from llm.llama_cpp_llm import LlamaCppLLM
from llm.ollama_llm import OllamaLLM
from llm.openai_llm import OpenAILLM
from utils.logger import get_logger

logger = get_logger(__name__)


def create_llm() -> Optional[BaseLLM]:
    llm_type = settings.llm.type.lower()
    if llm_type == "ollama":
        logger.info(f"🧠 Usando Ollama: {settings.llm.model}")
        return OllamaLLM(
            model=settings.llm.model,
            host=settings.llm.host,
            temperature=settings.llm.temperature,
            max_tokens=settings.llm.max_tokens,
            timeout=settings.llm.timeout,
        )
    if llm_type == "llama_cpp":
        logger.info(f"🧠 Usando Llama.cpp: {settings.llm.model}")
        return LlamaCppLLM(
            model_path=settings.llm.model,
            temperature=settings.llm.temperature,
            max_tokens=settings.llm.max_tokens,
        )
    if llm_type == "openai":
        logger.info(f"🧠 Usando OpenAI: {settings.llm.model}")
        return OpenAILLM(
            model=settings.llm.model,
            api_key=settings.llm.api_key,
            base_url=settings.llm.host,
            temperature=settings.llm.temperature,
            max_tokens=settings.llm.max_tokens,
        )
    logger.warning(f"⚠️ Tipo de LLM desconhecido: {llm_type}")
    return None
