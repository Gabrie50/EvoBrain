"""
Calculadora de métricas - estatísticas detalhadas da simulação
"""

import numpy as np
from typing import List, Dict, Any
from collections import deque
from datetime import datetime, timedelta


class MetricsCalculator:
    """Calcula métricas detalhadas da simulação"""
    
    def __init__(self, history_size: int = 1000):
        self.history_size = history_size
        self.predictions_history: deque = deque(maxlen=history_size)
        self.accuracy_history: deque = deque(maxlen=history_size)
    
    def add_prediction(self, prediction: str, result: str, acertou: bool, confidence: float):
        """Adiciona uma previsão ao histórico"""
        self.predictions_history.append({
            'timestamp': datetime.now(),
            'prediction': prediction,
            'result': result,
            'acertou': acertou,
            'confidence': confidence
        })
        
        self.accuracy_history.append(acertou)
    
    def get_accuracy_trend(self, window: int = 100) -> List[float]:
        """Retorna tendência de precisão"""
        if len(self.accuracy_history) < window:
            return list(self.accuracy_history)
        
        trend = []
        for i in range(window, len(self.accuracy_history) + 1, window):
            window_data = list(self.accuracy_history)[i-window:i]
            accuracy = sum(window_data) / len(window_data) * 100
            trend.append(accuracy)
        
        return trend
    
    def get_error_analysis(self) -> Dict[str, Any]:
        """Analisa erros"""
        errors = [p for p in self.predictions_history if not p['acertou']]
        
        if not errors:
            return {'total_errors': 0}
        
        # Análise por confiança
        high_confidence_errors = [e for e in errors if e['confidence'] > 80]
        low_confidence_errors = [e for e in errors if e['confidence'] < 50]
        
        # Análise por padrão
        banker_errors = [e for e in errors if e['prediction'] == 'BANKER']
        player_errors = [e for e in errors if e['prediction'] == 'PLAYER']
        
        return {
            'total_errors': len(errors),
            'high_confidence_errors': len(high_confidence_errors),
            'low_confidence_errors': len(low_confidence_errors),
            'banker_errors': len(banker_errors),
            'player_errors': len(player_errors),
            'error_rate': len(errors) / len(self.predictions_history) * 100 if self.predictions_history else 0
        }
    
    def get_performance_by_time(self) -> Dict[str, float]:
        """Performance por período do dia"""
        if not self.predictions_history:
            return {}
        
        performance = {}
        
        for p in self.predictions_history:
            hour = p['timestamp'].hour
            if hour not in performance:
                performance[hour] = {'correct': 0, 'total': 0}
            
            performance[hour]['total'] += 1
            if p['acertou']:
                performance[hour]['correct'] += 1
        
        return {h: (d['correct'] / d['total'] * 100) for h, d in performance.items()}
    
    def get_summary(self) -> Dict[str, Any]:
        """Resumo das métricas"""
        total = len(self.predictions_history)
        correct = sum(1 for p in self.predictions_history if p['acertou'])
        
        return {
            'total_predictions': total,
            'correct_predictions': correct,
            'accuracy': (correct / total * 100) if total > 0 else 0,
            'average_confidence': np.mean([p['confidence'] for p in self.predictions_history]) if total > 0 else 0,
            'error_analysis': self.get_error_analysis(),
            'accuracy_trend': self.get_accuracy_trend(),
            'performance_by_hour': self.get_performance_by_time()
        }
