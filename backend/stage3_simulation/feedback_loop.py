"""
Feedback loop - aprende com erros e ajusta agentes
"""

import time
from typing import Dict, List, Any
from collections import deque
from utils.logger import get_logger

logger = get_logger(__name__)


class FeedbackLoop:
    """
    Loop de feedback que aprende com erros
    Ajusta pesos dos agentes e identifica padrões de erro
    """
    
    def __init__(self, learning_rate: float = 0.1):
        self.learning_rate = learning_rate
        self.error_history: deque = deque(maxlen=1000)
        self.patterns: Dict[str, int] = {}
        self.corrections_applied = 0
        
        logger.info("🔄 Feedback Loop inicializado")
    
    def process(self, prediction: Dict, real_result: str, acertou: bool):
        """Processa resultado e aprende"""
        if acertou:
            self._reward_agents(prediction)
        else:
            self._penalize_agents(prediction)
            self._analyze_error(prediction, real_result)
    
    def _reward_agents(self, prediction: Dict):
        """Recompensa agentes que acertaram"""
        for vote in prediction.get('agent_votes', []):
            agent_name = vote['name']
            # Aumenta peso do agente
            self._adjust_agent_weight(agent_name, +0.02)
    
    def _penalize_agents(self, prediction: Dict):
        """Penaliza agentes que erraram"""
        for vote in prediction.get('agent_votes', []):
            if vote['prediction'] == prediction['prediction']:
                agent_name = vote['name']
                # Diminui peso do agente
                self._adjust_agent_weight(agent_name, -0.01)
    
    def _adjust_agent_weight(self, agent_name: str, delta: float):
        """Ajusta peso de um agente"""
        # Isso será implementado via referência ao sistema RL
        # Por enquanto, apenas log
        logger.debug(f"   Ajustando peso de {agent_name}: {delta:+.2f}")
    
    def _analyze_error(self, prediction: Dict, real_result: str):
        """Analisa erro para identificar padrões"""
        error_info = {
            'prediction': prediction['prediction'],
            'real': real_result,
            'confidence': prediction['confidence'],
            'timestamp': time.time()
        }
        
        self.error_history.append(error_info)
        
        # Identifica padrões
        pattern = self._identify_pattern(error_info)
        if pattern:
            self.patterns[pattern] = self.patterns.get(pattern, 0) + 1
            logger.info(f"🔍 Padrão identificado: {pattern} (total: {self.patterns[pattern]})")
    
    def _identify_pattern(self, error: Dict) -> str:
        """Identifica padrão de erro"""
        confidence = error['confidence']
        
        if confidence > 80:
            return "erro_alta_confianca"
        elif confidence < 50:
            return "erro_baixa_confianca"
        
        return None
    
    def get_stats(self) -> dict:
        """Retorna estatísticas do feedback loop"""
        return {
            'total_errors': len(self.error_history),
            'patterns': self.patterns,
            'corrections_applied': self.corrections_applied
        }
