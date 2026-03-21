"""
Templates de prompts para a LLM
"""

EXTRACTION_PROMPT = """
Extraia todas as entidades importantes do texto abaixo.

Entidades podem ser:
- Pessoas (nome, cargo, afiliação)
- Organizações (empresas, governos, instituições)
- Eventos (datas, acontecimentos)
- Conceitos (ideias, teorias, padrões)
- Locais (países, cidades, regiões)

Retorne em formato JSON:
{
    "entities": [
        {
            "name": "nome da entidade",
            "type": "pessoa/organizacao/evento/conceito/local",
            "description": "descrição curta",
            "aliases": ["outros nomes"]
        }
    ]
}

Texto:
{text}
"""

AGENT_CREATION_PROMPT = """
Crie um perfil detalhado para um agente baseado na entidade: {entity_name}

Contexto adicional: {context}

Retorne em JSON com os seguintes campos:
{{
    "name": "nome do agente",
    "personality": "descrição da personalidade (incluindo MBTI e 3 traços principais)",
    "traits": ["traço1", "traço2", "traço3"],
    "mbti": "MBTI (ex: INTJ, ENFP, etc)",
    "history": "breve histórico do agente",
    "position": "posicionamento (esquerda/direita/centro/neutro)"
}}
"""

REPORT_PROMPT = """
Você é um analista de dados especializado em sistemas de previsão.
Gere um relatório profissional com base nas estatísticas abaixo.

## ESTATÍSTICAS DA SIMULAÇÃO

- Precisão: {accuracy:.1f}%
- Agentes ativos: {active_agents}
- Total de agentes criados: {total_agents}
- Previsões feitas: {predictions_made}
- Geração atual: {generation}
- Melhor fitness: {best_fitness:.2f}%

## FORMATO DO RELATÓRIO

1. **Resumo Executivo** (2-3 frases)
2. **Análise de Performance**
3. **Análise dos Agentes**
4. **Recomendações**
5. **Próximos Passos**

Seja objetivo e use linguagem profissional.
"""

CHAT_PROMPT = """
Você é {agent_name}, um agente com a seguinte personalidade:
- Personalidade: {personality}
- Histórico: {history}
- Posicionamento: {position}

Você tem participado de uma simulação de previsão com os seguintes resultados:
- Total de decisões: {total_uses}
- Acertos: {correct}
- Precisão: {accuracy:.1f}%

Histórico da conversa:
{history_text}

Usuário pergunta: {question}

Responda como {agent_name}, mantendo sua personalidade. Seja conciso, mas explique seu raciocínio.
"""
