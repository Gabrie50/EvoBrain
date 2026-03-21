"""
Cliente WebSocket para dados em tempo real
"""

import json
import threading
import time
from typing import Optional, Callable, Dict
from dataclasses import dataclass

try:
    import websocket
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False

from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class WebSocketMessage:
    """Mensagem recebida do WebSocket"""
    type: str
    data: Dict
    raw: str


class WebSocketClient:
    """Cliente WebSocket para dados em tempo real"""
    
    def __init__(self, url: str, on_message: Optional[Callable] = None):
        self.url = url
        self.on_message_callback = on_message
        self.ws = None
        self._running = False
        self._thread: Optional[threading.Thread] = None
        
        if not WEBSOCKET_AVAILABLE:
            logger.warning("WebSocket não disponível. Instale: pip install websocket-client")
    
    def connect(self):
        """Conecta ao WebSocket"""
        if not WEBSOCKET_AVAILABLE:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
    
    def _run(self):
        """Executa o WebSocket em thread separada"""
        while self._running:
            try:
                self.ws = websocket.WebSocketApp(
                    self.url,
                    on_open=self._on_open,
                    on_message=self._on_message,
                    on_error=self._on_error,
                    on_close=self._on_close
                )
                self.ws.run_forever()
            except Exception as e:
                logger.error(f"Erro no WebSocket: {e}")
                time.sleep(5)
    
    def _on_open(self, ws):
        """Callback de abertura"""
        logger.info("✅ WebSocket conectado")
    
    def _on_message(self, ws, message):
        """Callback de mensagem"""
        try:
            data = json.loads(message)
            msg = WebSocketMessage(
                type=data.get('type', 'unknown'),
                data=data,
                raw=message
            )
            
            if self.on_message_callback:
                self.on_message_callback(msg)
                
        except json.JSONDecodeError:
            logger.debug(f"Mensagem não-JSON: {message[:100]}")
    
    def _on_error(self, ws, error):
        """Callback de erro"""
        logger.error(f"Erro WebSocket: {error}")
    
    def _on_close(self, ws, close_status_code, close_msg):
        """Callback de fechamento"""
        logger.info("WebSocket desconectado")
    
    def stop(self):
        """Para o cliente"""
        self._running = False
        if self.ws:
            self.ws.close()
