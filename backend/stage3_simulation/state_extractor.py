"""
Extrator de estado - converte histórico em vetor para rede neural
"""

import numpy as np
from typing import List, Dict


class StateExtractor:
    """Extrai estado do histórico para entrada da rede neural"""
    
    def __init__(self, state_size: int = 150):
        self.state_size = state_size
    
    def extract(self, history: List[Dict]) -> np.ndarray:
        """Extrai estado do histórico"""
        state = []
        
        for r in history:
            # Resultado (one-hot)
            if r['resultado'] == 'BANKER':
                state.extend([1, 0, 0])
            elif r['resultado'] == 'PLAYER':
                state.extend([0, 1, 0])
            else:  # TIE
                state.extend([0, 0, 1])
            
            # Scores
            state.append(r.get('player_score', 0) / 12)
            state.append(r.get('banker_score', 0) / 12)
        
        # Pad para tamanho fixo
        while len(state) < self.state_size:
            state.append(0)
        
        # Trunca se necessário
        if len(state) > self.state_size:
            state = state[:self.state_size]
        
        return np.array(state, dtype=np.float32)
    
    def extract_features(self, history: List[Dict]) -> np.ndarray:
        """Extrai features adicionais para análise"""
        if len(history) < 10:
            return np.zeros(10)
        
        results = [r['resultado'] for r in history[-50:]]
        
        features = []
        
        # Streak atual
        streak = 0
        for r in reversed(results):
            if r != 'TIE':
                streak += 1
            else:
                break
        features.append(streak / 20)
        
        # Proporção BANKER/PLAYER
        banker = results.count('BANKER')
        player = results.count('PLAYER')
        total = banker + player
        if total > 0:
            features.append(banker / total)
            features.append(player / total)
        else:
            features.extend([0.5, 0.5])
        
        # Alternância
        alternations = 0
        for i in range(1, len(results)):
            if results[i] != 'TIE' and results[i-1] != 'TIE' and results[i] != results[i-1]:
                alternations += 1
        features.append(alternations / max(1, len(results)))
        
        # TIE rate
        tie_rate = results.count('TIE') / len(results)
        features.append(tie_rate)
        
        return np.array(features, dtype=np.float32)
