"""
Pipeline de dados - orquestra a coleta de dados
"""

import threading
import time
from typing import Optional, Callable, List
from collections import deque

from .bacbo_api import BacBoDataAPI
from .websocket_client import WebSocketClient
from utils.logger import get_logger

logger = get_logger(__name__)


class DataPipeline:
    """Pipeline de dados com fallback automático"""
    
    def __init__(self, on_new_data: Optional[Callable] = None):
        self.api = BacBoDataAPI()
        self.ws_client = None
        self.on_new_data = on_new_data
        
        self._running = False
        self._threads = []
        self._last_id: Optional[str] = None
        self._fallback_mode = False
        
        logger.info("📊 DataPipeline inicializado")
    
    def start(self):
        """Inicia o pipeline"""
        self._running = True
        
        # Thread da API
        api_thread = threading.Thread(target=self._api_loop, daemon=True)
        api_thread.start()
        self._threads.append(api_thread)
        
        # Thread WebSocket (se disponível)
        try:
            self.ws_client = WebSocketClient(
                "wss://api-cs.casino.org/svc-evolution-game-events/ws/bacbo",
                on_message=self._on_ws_message
            )
            self.ws_client.connect()
            logger.info("✅ Pipeline de dados iniciado (API + WebSocket)")
        except Exception as e:
            logger.warning(f"WebSocket não iniciado: {e}")
            logger.info("✅ Pipeline de dados iniciado (somente API)")
    
    def stop(self):
        """Para o pipeline"""
        self._running = False
        if self.ws_client:
            self.ws_client.stop()
        
        for thread in self._threads:
            thread.join(timeout=2)
        
        logger.info("Pipeline de dados parado")
    
    def _api_loop(self):
        """Loop da API para coleta periódica"""
        while self._running:
            try:
                data = self.api.fetch_latest()
                if data and data['id'] != self._last_id:
                    self._last_id = data['id']
                    self._process_data(data, 'api')
                
                time.sleep(0.5)  # Intervalo da API
                
            except Exception as e:
                logger.error(f"Erro no loop da API: {e}")
                time.sleep(5)
    
    def _on_ws_message(self, message):
        """Callback do WebSocket"""
        try:
            if 'data' in message.data and 'result' in message.data['data']:
                game_data = message.data['data']
                result = game_data['result']
                
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
                
                data = {
                    'id': game_data.get('id'),
                    'timestamp': time.time(),
                    'player_score': player_score,
                    'banker_score': banker_score,
                    'resultado': resultado,
                    'source': 'websocket'
                }
                
                self._process_data(data, 'websocket')
                
        except Exception as e:
            logger.error(f"Erro ao processar mensagem WS: {e}")
    
    def _process_data(self, data: dict, source: str):
        """Processa dados recebidos"""
        data['source'] = source
        
        if self.on_new_data:
            self.on_new_data(data)
        else:
            logger.debug(f"📡 Dados recebidos ({source}): {data['resultado']}")
