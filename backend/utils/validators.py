"""
Validações de dados
"""

import re
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone


def validate_rodada(data: Dict) -> bool:
    """Valida dados de uma rodada"""
    required_fields = ['id', 'resultado', 'player_score', 'banker_score']
    
    for field in required_fields:
        if field not in data:
            return False
    
    if data['resultado'] not in ['BANKER', 'PLAYER', 'TIE']:
        return False
    
    if not isinstance(data['player_score'], int) or not isinstance(data['banker_score'], int):
        return False
    
    if data['player_score'] < 0 or data['player_score'] > 12:
        return False
    
    if data['banker_score'] < 0 or data['banker_score'] > 12:
        return False
    
    return True


def validate_previsao(data: Dict) -> bool:
    """Valida dados de uma previsão"""
    required_fields = ['previsao', 'confianca']
    
    for field in required_fields:
        if field not in data:
            return False
    
    if data['previsao'] not in ['BANKER', 'PLAYER']:
        return False
    
    if not isinstance(data['confianca'], (int, float)):
        return False
    
    if data['confianca'] < 0 or data['confianca'] > 100:
        return False
    
    return True


def validate_agent_profile(data: Dict) -> bool:
    """Valida perfil de agente"""
    required_fields = ['name', 'personality']
    
    for field in required_fields:
        if field not in data:
            return False
    
    if not isinstance(data['name'], str) or len(data['name']) > 100:
        return False
    
    return True


def sanitize_text(text: str, max_length: int = 10000) -> str:
    """Sanitiza texto para uso com LLM"""
    # Remove caracteres especiais problemáticos
    text = re.sub(r'[^\w\s.,!?;:()\-\[\]\'"áàãâéèêíìîóòõôúùûçÁÀÃÂÉÈÊÍÌÎÓÒÕÔÚÙÛÇ]', ' ', text)
    
    # Remove múltiplos espaços
    text = re.sub(r'\s+', ' ', text)
    
    # Trunca
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    return text.strip()


def validate_state(state: List[float], expected_size: int) -> bool:
    """Valida estado para rede neural"""
    if len(state) != expected_size:
        return False
    
    for value in state:
        if not isinstance(value, (int, float)):
            return False
    
    return True
