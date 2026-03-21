"""
Motor de chat - permite conversar com agentes usando LLM local
"""

import json
from typing import Dict, Optional, List

from ..stage2_generation.dynamic_generator import DynamicAgentGenerator
from ..llm.local_llm import LocalLLM
from utils.logger import get_logger

logger = get_logger(__name__)


class ChatEngine:
    """Motor de chat para interação com agentes"""
    
    def __init__(self, generator: DynamicAgentGenerator, llm: LocalLLM):
        self.generator = generator
        self.llm = llm
        self.conversation_history: Dict[str, List[Dict]] = {}
    
    def chat(self, agent_name: str, question: str) -> str:
        """Conversa com um agente"""
        agent = self.generator.get_agent(agent_name)
        if not agent:
            return f"Agente '{agent_name}' não encontrado. Agentes disponíveis: {', '.join(self.generator.agents.keys())[:100]}"
        
        # Recupera histórico da conversa
        if agent_name not in self.conversation_history:
            self.conversation_history[agent_name] = []
        
        history = self.conversation_history[agent_name]
        
        # Constrói prompt com contexto do agente
        prompt = self._build_agent_prompt(agent, question, history)
        
        # Gera resposta
        response = self.llm.generate(prompt)
        
        # Atualiza histórico
        history.append({'role': 'user', 'content': question})
        history.append({'role': 'assistant', 'content': response})
        
        # Limita histórico
        if len(history) > 20:
            self.conversation_history[agent_name] = history[-20:]
        
        return response
    
    def chat_with_agent_by_id(self, agent_id: int, question: str) -> str:
        """Conversa com agente por ID"""
        for name, agent in self.generator.agents.items():
            if agent.id == agent_id:
                return self.chat(name, question)
        
        return f"Agente com ID {agent_id} não encontrado"
    
    def list_agents(self) -> List[Dict]:
        """Lista todos os agentes disponíveis para chat"""
        return [
            {
                'name': agent.name,
                'id': agent.id,
                'personality': agent.personality[:100],
                'accuracy': agent.accuracy,
                'total_uses': agent.total_uso
            }
            for agent in self.generator.get_all_agents()
        ]
    
    def _build_agent_prompt(self, agent, question: str, history: List[Dict]) -> str:
        """Constrói prompt para o agente"""
        # Contexto do agente
        context = f"""
Você é {agent.name}, um agente com a seguinte personalidade:
- Personalidade: {agent.personality}
- Histórico: {agent.history[:500]}
- Posicionamento: {agent.position}

Você tem participado de uma simulação de previsão de Bac Bo com os seguintes resultados:
- Total de decisões: {agent.total_uso}
- Acertos: {agent.acertos}
- Precisão: {agent.accuracy:.1f}%

Seus traços principais: {', '.join(agent.traits[:3]) if agent.traits else 'analítico, estratégico'}
"""
        
        # Histórico da conversa
        history_text = ""
        for msg in history[-5:]:
            role = "Usuário" if msg['role'] == 'user' else "Você"
            history_text += f"{role}: {msg['content']}\n"
        
        # Prompt final
        prompt = f"""
{context}

Histórico da conversa:
{history_text}

Usuário pergunta: {question}

Responda como {agent.name}, mantendo sua personalidade. Seja conciso, mas explique seu raciocínio.
"""
        
        return prompt
    
    def reset_conversation(self, agent_name: str):
        """Reseta histórico de conversa com um agente"""
        if agent_name in self.conversation_history:
            del self.conversation_history[agent_name]
            logger.info(f"🔄 Conversa com {agent_name} resetada")
