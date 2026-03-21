"""
Interface do agente - ponto de entrada para interação
"""

from typing import Dict, List, Optional
from .chat_engine import ChatEngine
from ..stage2_generation.dynamic_generator import DynamicAgentGenerator
from utils.logger import get_logger

logger = get_logger(__name__)


class AgentInterface:
    """Interface para interação com agentes"""
    
    def __init__(self, generator: DynamicAgentGenerator, chat_engine: ChatEngine):
        self.generator = generator
        self.chat_engine = chat_engine
    
    def ask_agent(self, agent_name: str, question: str) -> Dict:
        """Pergunta para um agente"""
        response = self.chat_engine.chat(agent_name, question)
        
        return {
            'agent': agent_name,
            'question': question,
            'response': response,
            'status': 'success'
        }
    
    def ask_about_prediction(self, agent_name: str, prediction: str, context: List[Dict]) -> Dict:
        """Pergunta sobre uma previsão específica"""
        question = f"Você previu {prediction}. Por que tomou essa decisão? Quais fatores influenciaram sua escolha?"
        
        response = self.chat_engine.chat(agent_name, question)
        
        return {
            'agent': agent_name,
            'prediction': prediction,
            'explanation': response,
            'status': 'success'
        }
    
    def get_agent_insights(self, agent_name: str) -> Dict:
        """Obtém insights sobre um agente"""
        agent = self.generator.get_agent(agent_name)
        if not agent:
            return {'error': f'Agent {agent_name} not found'}
        
        # Pergunta sobre estratégia
        question = "Qual é sua estratégia para prever resultados? Como você analisa os padrões?"
        strategy = self.chat_engine.chat(agent_name, question)
        
        # Pergunta sobre autoavaliação
        question = "Como você avalia sua própria performance? O que você aprendeu com seus erros?"
        self_assessment = self.chat_engine.chat(agent_name, question)
        
        return {
            'name': agent.name,
            'personality': agent.personality,
            'accuracy': agent.accuracy,
            'total_decisions': agent.total_uso,
            'strategy': strategy,
            'self_assessment': self_assessment
        }
    
    def compare_agents(self, agent_names: List[str], question: str) -> Dict:
        """Compara respostas de múltiplos agentes"""
        responses = {}
        
        for name in agent_names:
            if self.generator.get_agent(name):
                responses[name] = self.chat_engine.chat(name, question)
        
        return {
            'question': question,
            'responses': responses
        }
