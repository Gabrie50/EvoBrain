#!/usr/bin/env python
"""
Script para treinar o sistema com dados históricos
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import time
from pathlib import Path
from typing import List, Dict

from stage3_simulation.rl_agent import RLAgent
from stage3_simulation.neuroevolution import NeuroEvolution
from stage2_generation.agent_profile import AgentProfile
from data_collector.bacbo_api import BacBoDataAPI
from storage.database import db
from utils.logger import logger


def train_with_historical_data(limit: int = 1000):
    """Treina com dados históricos do banco"""
    logger.info(f"🧠 Treinando com {limit} rodadas históricas...")
    
    # Carrega dados históricos
    rodadas = db.get_ultimas_rodadas(limit)
    
    if not rodadas:
        logger.error("Nenhum dado histórico encontrado")
        return
    
    logger.info(f"📊 Carregadas {len(rodadas)} rodadas")
    
    # Cria agente simples para treino
    profile = AgentProfile(
        id=0,
        name="Trainer",
        entity_name="Trainer",
        personality="Analítico, estratégico"
    )
    
    agent = RLAgent(profile, state_size=150)
    
    # Treina com os dados
    correct = 0
    total = 0
    
    for i in range(30, len(rodadas)):
        historico = rodadas[:i]
        resultado = rodadas[i]['resultado']
        
        # Extrai estado
        state = agent._extract_state(historico[-30:])
        
        # Decide
        action, _ = agent.decide(state)
        
        # Verifica
        outcome_int = 0 if resultado == 'BANKER' else 1
        if action == outcome_int:
            correct += 1
        total += 1
        
        # Aprende
        agent.learn(action, resultado)
        
        if total % 100 == 0:
            logger.info(f"   Progresso: {total}/{len(rodadas)-30} | Precisão: {correct/total*100:.1f}%")
    
    logger.info(f"✅ Treino concluído! Precisão final: {correct/total*100:.1f}%")


if __name__ == "__main__":
    train_with_historical_data()
