"""
Configuração de logging
"""

import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logger(name: str = "evobrain", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()

    class ColoredFormatter(logging.Formatter):
        COLORS = {"DEBUG": "\033[36m", "INFO": "\033[32m", "WARNING": "\033[33m", "ERROR": "\033[31m", "CRITICAL": "\033[35m"}

        def format(self, record):
            color = self.COLORS.get(record.levelname, "")
            reset = "\033[0m"
            timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
            level_colored = f"{color}{record.levelname}{reset}"
            return f"{timestamp} | {level_colored} | {record.name} | {record.getMessage()}"

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColoredFormatter())
    logger.addHandler(console_handler)

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(log_dir / f"evobrain_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
    logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "evobrain") -> logging.Logger:
    return logging.getLogger(name)


logger = setup_logger()
