"""
Interface com LLM local (Ollama)
"""

import requests
import json
import time
from typing import Optional, Dict, Any
from utils.logger import get_logger

logger = get_logger(__name__)


class LocalLLM:
    """Cliente para LLM local via Ollama"""
    
    def __init__(self, model: str = "llama3.2", host: str = "http://localhost:11434", timeout: int = 30):
        self.model = model
        self.host = host
        self.timeout = timeout
        self.session = requests.Session()
        self._connected = False
        
        logger.info(f"🧠 LocalLLM inicializado: {model} @ {host}")
    
    def connect(self) -> bool:
        """Testa conexão com Ollama"""
        try:
            response = self.session.get(f"{self.host}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]
                
                if self.model not in model_names:
                    logger.warning(f"Modelo {self.model} não encontrado. Disponível: {model_names}")
                
                self._connected = True
                logger.info(f"✅ Conectado ao Ollama. Modelos: {model_names}")
                return True
            else:
                logger.error(f"Erro ao conectar: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Erro ao conectar ao Ollama: {e}")
            return False
    
    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Gera texto com a LLM"""
        if not self._connected:
            logger.warning("LLM não conectada, tentando reconectar...")
            if not self.connect():
                return self._fallback_response(prompt)
        
        try:
            response = self.session.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                logger.error(f"Erro na geração: {response.status_code}")
                return self._fallback_response(prompt)
                
        except requests.exceptions.Timeout:
            logger.error("Timeout na geração")
            return self._fallback_response(prompt)
        except Exception as e:
            logger.error(f"Erro na geração: {e}")
            return self._fallback_response(prompt)
    
    def _fallback_response(self, prompt: str) -> str:
        """Resposta de fallback quando LLM está offline"""
        if "extraia" in prompt.lower() or "entidades" in prompt.lower():
            return '{"entities": []}'
        elif "personalidade" in prompt.lower() or "perfil" in prompt.lower():
            return '{"name": "Agente", "personality": "Analítico, estratégico", "position": "neutro"}'
        else:
            return "O sistema de LLM local está offline. Verifique se o Ollama está rodando."
    
    def is_connected(self) -> bool:
        """Retorna status da conexão"""
        return self._connected
    
    def list_models(self) -> list:
        """Lista modelos disponíveis"""
        try:
            response = self.session.get(f"{self.host}/api/tags", timeout=5)
            if response.status_code == 200:
                return [m['name'] for m in response.json().get('models', [])]
        except Exception as e:
            logger.error(f"Erro ao listar modelos: {e}")
        
        return []
