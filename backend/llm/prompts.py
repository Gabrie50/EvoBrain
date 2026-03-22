"""
Templates de prompts para LLM
"""

EXTRACTION_PROMPT = """
Extraia todas as entidades importantes do texto abaixo.
Entidades podem ser: pessoas, organizações, eventos, conceitos, locais.
Retorne em JSON: {{"entities": [{{"name": "...", "type": "...", "description": "..."}}]}}
Texto: {text}
"""

AGENT_CREATION_PROMPT = """
Crie um perfil para um agente baseado em: {entity_name}
Contexto: {context}
Retorne JSON: {{"name": "...", "personality": "...", "traits": [...], "mbti": "...", "history": "...", "position": "..."}}
"""

REPORT_PROMPT = """
Gere um relatório profissional com base nas estatísticas:
- Precisão: {accuracy:.1f}%
- Agentes ativos: {active_agents}
- Total de agentes: {total_agents}
- Previsões: {predictions_made}
- Geração: {generation}
Inclua: resumo executivo, análise de performance, recomendações.
"""

CHAT_PROMPT = """
Você é {agent_name}, com personalidade: {personality}
Histórico: {history}
Precisão: {accuracy:.1f}%
Usuário: {question}
Responda mantendo sua personalidade.
"""
