"""
Cliente da API do Bac Bo - coleta dados em tempo real
"""

import time
import requests
import json
from typing import Optional, Dict, List
from datetime import datetime, timezone

from utils.logger import get_logger

logger = get_logger(__name__)


class BacBoDataAPI:
    """Cliente para a API do Bac Bo"""
    
    def __init__(self):
        self.api_url = "https://api-cs.casino.org/svc-evolution-game-events/api/bacbo"
        self.latest_url = f"{self.api_url}/latest"
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Cache-Control': 'no-cache'
        }
        
        self.last_id: Optional[str] = None
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        logger.info("📡 BacBoDataAPI inicializado")
    
    def fetch_latest(self) -> Optional[Dict]:
        """Busca a rodada mais recente"""
        try:
            response = self.session.get(self.latest_url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            rodada_id = data.get('id')
            
            if rodada_id == self.last_id:
                return None
            
            self.last_id = rodada_id
            
            # Extrai dados
            game_data = data.get('data', {})
            result = game_data.get('result', {})
            
            player_dice = result.get('playerDice', {})
            banker_dice = result.get('bankerDice', {})
            
            player_score = player_dice.get('first', 0) + player_dice.get('second', 0)
            banker_score = banker_dice.get('first', 0) + banker_dice.get('second', 0)
            
            outcome = result.get('outcome', '')
            if outcome == 'PlayerWon':
                resultado = 'PLAYER'
            elif outcome == 'BankerWon':
                resultado = 'BANKER'
            else:
                resultado = 'TIE'
            
            return {
                'id': rodada_id,
                'timestamp': datetime.now(timezone.utc),
                'player_score': player_score,
                'banker_score': banker_score,
                'resultado': resultado,
                'raw_data': data
            }
            
        except requests.exceptions.Timeout:
            logger.debug("Timeout na API")
            return None
        except requests.exceptions.RequestException as e:
            logger.debug(f"Erro na API: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro ao processar resposta: {e}")
            return None
    
    def fetch_history(self, page: int = 0, size: int = 100) -> List[Dict]:
        """Busca histórico de rodadas"""
        try:
            params = {
                'page': page,
                'size': size,
                'sort': 'data.settledAt,desc',
                '_t': int(time.time() * 1000)
            }
            
            response = self.session.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            rodadas = []
            
            for item in data:
                game_data = item.get('data', {})
                result = game_data.get('result', {})
                
                player_dice = result.get('playerDice', {})
                banker_dice = result.get('bankerDice', {})
                
                player_score = player_dice.get('first', 0) + player_dice.get('second', 0)
                banker_score = banker_dice.get('first', 0) + banker_dice.get('second', 0)
                
                outcome = result.get('outcome', '')
                if outcome == 'PlayerWon':
                    resultado = 'PLAYER'
                elif outcome == 'BankerWon':
                    resultado = 'BANKER'
                else:
                    resultado = 'TIE'
                
                settled_at = game_data.get('settledAt', '')
                try:
                    timestamp = datetime.fromisoformat(settled_at.replace('Z', '+00:00'))
                except:
                    timestamp = datetime.now(timezone.utc)
                
                rodadas.append({
                    'id': game_data.get('id'),
                    'timestamp': timestamp,
                    'player_score': player_score,
                    'banker_score': banker_score,
                    'resultado': resultado
                })
            
            return rodadas
            
        except Exception as e:
            logger.error(f"Erro ao buscar histórico: {e}")
            return []
