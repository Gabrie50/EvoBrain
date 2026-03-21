import random
from typing import List, Tuple


class PersonalityFactory:
    MBTI_TYPES = [("INTJ", "Arquiteto", "Estratégico, inovador, visionário"), ("ENTJ", "Comandante", "Líder, decisivo, estratégico"), ("ISTJ", "Logístico", "Prático, detalhista, confiável")]
    TRAITS = {"positivo": ["otimista", "confiante", "resiliente"], "negativo": ["cético", "ansioso", "teimoso"], "neutro": ["analítico", "prático", "cauteloso"]}

    @classmethod
    def generate(cls, seed: str | None = None) -> Tuple[str, List[str], str]:
        if seed is not None:
            random.seed(hash(seed))
        mbti, label, desc = random.choice(cls.MBTI_TYPES)
        traits = [random.choice(cls.TRAITS[key]) for key in ["positivo", "negativo", "neutro"]]
        return mbti, traits, f"{mbti} ({label}) - {desc}. Traços: {', '.join(traits)}"
