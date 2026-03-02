"""Structured logging utilities"""
import logging
import sys
from datetime import datetime
from typing import Any, Dict

from src.config import config


def setup_logging() -> logging.Logger:
    """Configure structured logging"""
    logger = logging.getLogger("ashoka")
    logger.setLevel(getattr(logging, config.LOG_LEVEL))
    
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger


def log_event(logger: logging.Logger, event_type: str, data: Dict[str, Any]) -> None:
    """Log structured event"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        **data
    }
    logger.info(f"{event_type}: {log_data}")


# Global logger instance
logger = setup_logging()
