#!/usr/bin/env python
"""
Script para avaliar performance do sistema
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import time
from storage.database import db
from utils.logger import logger


def evaluate():
    """Avalia performance do sistema"""
    logger.info("📊 Avaliando performance do sistema...")
    
    # Estatísticas do banco
    stats = db.get_stats()
    
    logger.info(f"""
╔══════════════════════════════════════════════════════════════╗
║                    RELATÓRIO DE AVALIAÇÃO                    ║
╠══════════════════════════════════════════════════════════════╣
║  Total de rodadas:     {stats.get('total_rodadas', 0):>10}                               ║
║  Total de previsões:   {stats.get('total_previsoes', 0):>10}                               ║
║  Acertos:              {stats.get('acertos', 0):>10}                               ║
║  Precisão:             {stats.get('precisao', 0):>9.1f}%                               ║
╚══════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    evaluate()
