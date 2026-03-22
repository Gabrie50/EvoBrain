"""
Validações de dados
"""

import re
from typing import Dict


def validate_rodada(data: Dict) -> bool:
    required = ["id", "resultado", "player_score", "banker_score"]
    for field in required:
        if field not in data:
            return False
    if data["resultado"] not in ["BANKER", "PLAYER", "TIE"]:
        return False
    if not isinstance(data["player_score"], int) or not isinstance(data["banker_score"], int):
        return False
    return True


def validate_previsao(data: Dict) -> bool:
    if "previsao" not in data or "confianca" not in data:
        return False
    if data["previsao"] not in ["BANKER", "PLAYER"]:
        return False
    if not isinstance(data["confianca"], (int, float)) or data["confianca"] < 0 or data["confianca"] > 100:
        return False
    return True


def sanitize_text(text: str, max_length: int = 10000) -> str:
    text = re.sub(r'[^\w\s.,!?;:()\-\[\]\'"áàãâéèêíìîóòõôúùûçÁÀÃÂÉÈÊÍÌÎÓÒÕÔÚÙÛÇ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    if len(text) > max_length:
        text = text[:max_length] + "..."
    return text.strip()
