"""
Detector de padrões - identifica padrões recorrentes no jogo
"""

import re
from typing import List, Dict, Optional, Tuple
from collections import deque
from utils.logger import get_logger

logger = get_logger(__name__)


class PatternDetector:
    """
    Detecta padrões recorrentes nos resultados
    Ex: padrão 7:2, streaks, alternâncias, etc
    """
    
    def __init__(self):
        self.pattern_history: deque = deque(maxlen=500)
        self.detected_patterns: Dict[str, int] = {}
        
        logger.info("🔍 Pattern Detector inicializado")
    
    def analyze(self, history: List[Dict]) -> Dict:
        """Analisa histórico em busca de padrões"""
        if len(history) < 10:
            return {'patterns': [], 'new_patterns': []}
        
        results = [r['resultado'] for r in history]
        
        patterns = []
        
        # 1. Padrão 7:2 (duplo TIE seguido de sequência)
        pattern_72 = self._detect_pattern_72(results)
        if pattern_72:
            patterns.append(pattern_72)
        
        # 2. Streaks longas
        streak = self._detect_streak(results)
        if streak and streak['length'] >= 3:
            patterns.append(streak)
        
        # 3. Alternância rápida
        alternation = self._detect_alternation(results)
        if alternation:
            patterns.append(alternation)
        
        # 4. Sequência de TIES
        tie_sequence = self._detect_tie_sequence(results)
        if tie_sequence:
            patterns.append(tie_sequence)
        
        # 5. Padrões de reversão
        reversal = self._detect_reversal(results)
        if reversal:
            patterns.append(reversal)
        
        # Atualiza histórico
        for p in patterns:
            self.pattern_history.append(p)
            self.detected_patterns[p['name']] = self.detected_patterns.get(p['name'], 0) + 1
        
        # Identifica novos padrões (que estão aparecendo mais que o normal)
        new_patterns = []
        for p in patterns:
            if self.detected_patterns.get(p['name'], 0) < 3:
                new_patterns.append(p)
        
        return {
            'patterns': patterns,
            'new_patterns': new_patterns,
            'stats': self.get_stats()
        }
    
    def _detect_pattern_72(self, results: List[str]) -> Optional[Dict]:
        """Detecta padrão 7:2 (duplo TIE + sequência dominante)"""
        # Procura duplo TIE
        for i in range(len(results) - 10):
            if results[i] == 'TIE' and results[i+1] == 'TIE':
                # Pega próximos 9 resultados não-TIE
                non_ties = []
                for j in range(i+2, len(results)):
                    if results[j] != 'TIE':
                        non_ties.append(results[j])
                        if len(non_ties) >= 9:
                            break
                
                if len(non_ties) >= 9:
                    banker = non_ties.count('BANKER')
                    player = non_ties.count('PLAYER')
                    
                    if banker >= 7:
                        return {
                            'name': '7:2_BANKER',
                            'description': f'Duplo TIE seguido de {banker}:{player} BANKER',
                            'confidence': min(75, 60 + (banker/9)*100),
                            'prediction': 'BANKER'
                        }
                    elif player >= 7:
                        return {
                            'name': '7:2_PLAYER',
                            'description': f'Duplo TIE seguido de {banker}:{player} PLAYER',
                            'confidence': min(75, 60 + (player/9)*100),
                            'prediction': 'PLAYER'
                        }
        
        return None
    
    def _detect_streak(self, results: List[str]) -> Optional[Dict]:
        """Detecta streak longa"""
        streak = 1
        for i in range(len(results)-1, max(0, len(results)-20), -1):
            if results[i] != 'TIE' and results[i] == results[i-1]:
                streak += 1
            else:
                break
        
        if streak >= 3:
            return {
                'name': f'streak_{streak}',
                'description': f'{streak} resultados consecutivos de {results[-1] if results else "?"}',
                'confidence': min(50 + streak * 5, 80),
                'prediction': results[-1] if results else None
            }
        
        return None
    
    def _detect_alternation(self, results: List[str]) -> Optional[Dict]:
        """Detecta alternância rápida"""
        alternations = 0
        for i in range(1, min(10, len(results))):
            if results[-i] != 'TIE' and results[-i-1] != 'TIE' and results[-i] != results[-i-1]:
                alternations += 1
        
        if alternations >= 3:
            return {
                'name': 'alternation_fast',
                'description': f'Alternância rápida: {alternations} em 10 rodadas',
                'confidence': min(60 + alternations * 5, 75),
                'prediction': None
            }
        
        return None
    
    def _detect_tie_sequence(self, results: List[str]) -> Optional[Dict]:
        """Detecta sequência de TIES"""
        ties = 0
        for r in reversed(results[-10:]):
            if r == 'TIE':
                ties += 1
            else:
                break
        
        if ties >= 2:
            return {
                'name': f'tie_sequence_{ties}',
                'description': f'{ties} TIES consecutivos',
                'confidence': 50 + ties * 10,
                'prediction': None
            }
        
        return None
    
    def _detect_reversal(self, results: List[str]) -> Optional[Dict]:
        """Detecta padrão de reversão"""
        if len(results) < 20:
            return None
        
        first_10 = results[:10]
        last_10 = results[-10:]
        
        banker_first = first_10.count('BANKER')
        banker_last = last_10.count('BANKER')
        
        if banker_first >= 6 and banker_last <= 3:
            return {
                'name': 'reversal_banker_to_player',
                'description': f'Reversão: {banker_first} BANKER nos primeiros 10 → {banker_last} nos últimos 10',
                'confidence': 70,
                'prediction': 'PLAYER'
            }
        elif banker_first <= 3 and banker_last >= 6:
            return {
                'name': 'reversal_player_to_banker',
                'description': f'Reversão: {banker_first} BANKER nos primeiros 10 → {banker_last} nos últimos 10',
                'confidence': 70,
                'prediction': 'BANKER'
            }
        
        return None
    
    def get_stats(self) -> dict:
        """Retorna estatísticas de detecção"""
        return {
            'total_detections': sum(self.detected_patterns.values()),
            'patterns': self.detected_patterns,
            'recent': list(self.pattern_history)[-10:]
        }
    
    def get_prediction(self, history: List[Dict]) -> Optional[Dict]:
        """Retorna previsão baseada em padrões detectados"""
        analysis = self.analyze(history)
        
        for pattern in analysis['patterns']:
            if pattern.get('prediction') and pattern.get('confidence', 0) > 60:
                return {
                    'prediction': pattern['prediction'],
                    'confidence': pattern['confidence'],
                    'pattern': pattern['name']
                }
        
        return None
