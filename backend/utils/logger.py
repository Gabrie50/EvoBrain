"""
Configuração de logging
"""

import sys
import logging
from pathlib import Path
from datetime import datetime


def setup_logger(name: str = "evobrain", level: int = logging.INFO) -> logging.Logger:
    """Configura logger com formato bonito"""
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove handlers existentes
    logger.handlers.clear()
    
    # Console handler com cores
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Formato
    class ColoredFormatter(logging.Formatter):
        """Formatter com cores para console"""
        
        COLORS = {
            'DEBUG': '\033[36m',   # Cyan
            'INFO': '\033[32m',    # Green
            'WARNING': '\033[33m', # Yellow
            'ERROR': '\033[31m',   # Red
            'CRITICAL': '\033[35m' # Magenta
        }
        
        def format(self, record):
            color = self.COLORS.get(record.levelname, '')
            reset = '\033[0m'
            
            # Timestamp formatado
            timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
            
            # Nível com cor
            level_colored = f"{color}{record.levelname}{reset}"
            
            # Mensagem
            message = record.getMessage()
            
            # Formato completo
            return f"{timestamp} | {level_colored} | {record.name} | {message}"
    
    console_handler.setFormatter(ColoredFormatter())
    logger.addHandler(console_handler)
    
    # File handler
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    file_handler = logging.FileHandler(
        log_dir / f"evobrain_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    ))
    logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = "evobrain") -> logging.Logger:
    """Retorna logger configurado"""
    return logging.getLogger(name)


# Logger padrão
logger = setup_logger()
