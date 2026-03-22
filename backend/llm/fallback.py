"""
Fallback quando LLM está offline
"""

import random


class LLMFallback:
    @staticmethod
    def extract_entities(text: str) -> dict:
        import re

        entities = []
        patterns = [
            (r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", "pessoa"),
            (r"\b[A-Z][a-z]+ (Bank|Corp|Inc)\b", "organizacao"),
        ]
        for pattern, etype in patterns:
            matches = re.findall(pattern, text)
            for match in set(matches[:5]):
                entities.append({"name": match, "type": etype, "description": "Entidade detectada"})
        return {"entities": entities}

    @staticmethod
    def create_agent(entity_name: str, context: str) -> dict:
        del context
        personalities = [
            "INTJ - Arquiteto: Estratégico",
            "ENFP - Ativista: Criativo",
            "ISTJ - Logístico: Prático",
        ]
        return {
            "name": entity_name,
            "personality": random.choice(personalities),
            "traits": ["analítico", "estratégico"],
            "mbti": random.choice(["INTJ", "ENFP", "ISTJ"]),
            "history": f"Agente baseado em {entity_name}",
            "position": "neutro",
        }

    @staticmethod
    def generate_report(stats: dict) -> str:
        return f"""
## Relatório de Simulação
Precisão: {stats.get('accuracy', 0):.1f}%
Agentes ativos: {stats.get('active_agents', 0)}
Total de previsões: {stats.get('predictions_made', 0)}
*Relatório gerado em modo fallback (LLM offline)*
"""
