"""
Fallback quando LLM local está offline
"""

import json
import random
from typing import Dict, List


class LLMFallback:
    """Respostas de fallback quando LLM está offline"""
    
    @staticmethod
    def extract_entities(text: str) -> Dict:
        """Fallback para extração de entidades"""
        import re
        
        entities = []
        
        # Padrões simples
        patterns = [
            (r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', 'pessoa'),
            (r'\b[A-Z][a-z]+ (Bank|Corp|Inc|Ltd|Group)\b', 'organizacao'),
            (r'\b\d{4}\b', 'evento'),
        ]
        
        for pattern, entity_type in patterns:
            matches = re.findall(pattern, text)
            for match in set(matches[:5]):
                entities.append({
                    'name': match if isinstance(match, str) else match[0],
                    'type': entity_type,
                    'description': f'Entidade detectada automaticamente'
                })
        
        return {'entities': entities}
    
    @staticmethod
    def create_agent(entity_name: str, context: str) -> Dict:
        """Fallback para criação de agente"""
        # Personalidades pré-definidas
        personalities = [
            "INTJ - Arquiteto: Estratégico, inovador, visionário. Traços: analítico, independente, determinado.",
            "ENFP - Ativista: Entusiasmado, criativo, social. Traços: otimista, empático, espontâneo.",
            "ISTJ - Logístico: Prático, detalhista, confiável. Traços: organizado, responsável, conservador.",
            "ENTJ - Comandante: Líder, decisivo, estratégico. Traços: ambicioso, confiante, direto.",
            "INTP - Lógico: Analítico, curioso, teórico. Traços: criativo, independente, cético."
        ]
        
        positions = ['esquerda', 'direita', 'centro', 'neutro']
        
        return {
            'name': entity_name,
            'personality': random.choice(personalities),
            'traits': ['analítico', 'estratégico', 'adaptável'],
            'mbti': random.choice(['INTJ', 'ENFP', 'ISTJ', 'ENTJ', 'INTP']),
            'history': f'Agente baseado em {entity_name}',
            'position': random.choice(positions)
        }
    
    @staticmethod
    def generate_report(stats: Dict) -> str:
        """Fallback para geração de relatório"""
        accuracy = stats.get('accuracy', 0)
        active_agents = stats.get('active_agents', 0)
        total_agents = stats.get('total_agents', 0)
        
        return f"""
## Relatório de Simulação

**Resumo Executivo**
O sistema alcançou {accuracy:.1f}% de precisão com {active_agents} agentes ativos.

**Análise de Performance**
A precisão atual é de {accuracy:.1f}%, baseada em {stats.get('predictions_made', 0)} previsões.

**Análise dos Agentes**
- Agentes ativos: {active_agents}
- Total de agentes criados: {total_agents}

**Recomendações**
- Continue monitorando a evolução dos agentes
- Considere aumentar a população de agentes
- Analise padrões de erro para melhorias

*Relatório gerado em modo fallback (LLM offline)*
"""
    
    @staticmethod
    def chat_response(agent_name: str, question: str, personality: str, accuracy: float) -> str:
        """Fallback para chat"""
        return f"""
Como {agent_name}, com minha personalidade {personality[:50]}... 
Baseado na minha experiência ({accuracy:.1f}% de precisão), 
eu analiso os padrões e faço previsões com base no histórico.

Sua pergunta: "{question}"

Em geral, minha estratégia é identificar streaks e padrões de alternância, 
combinando análise técnica com intuição baseada em experiência.
"""
