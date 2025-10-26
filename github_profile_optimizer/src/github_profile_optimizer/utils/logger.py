"""
Structured JSON logging.

Provides structured logging capabilities with JSON formatting for better log analysis.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional


class StructuredLogger:
    """
    Logger that outputs structured JSON logs.
    
    Provides structured logging with JSON formatting for improved
    log parsing and analysis capabilities.
    """
    
    def __init__(self, name: str, level: int = logging.INFO):
        """
        Initialize the structured logger.
        
        Args:
            name: Logger name
            level: Logging level
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Create handler if it doesn't exist
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _log(self, level: str, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """
        Log a message with structured data.
        
        Args:
            level: Log level
            message: Log message
            extra_data: Additional structured data
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level,
            "message": message
        }
        
        if extra_data:
            log_entry.update(extra_data)
            
        self.logger.log(getattr(logging, level.upper()), json.dumps(log_entry))
    
    def info(self, message: str, **kwargs):
        """
        Log an info message.
        
        Args:
            message: Log message
            **kwargs: Additional structured data
        """
        self._log("info", message, kwargs)
    
    def error(self, message: str, **kwargs):
        """
        Log an error message.
        
        Args:
            message: Log message
            **kwargs: Additional structured data
        """
        self._log("error", message, kwargs)
    
    def warning(self, message: str, **kwargs):
        """
        Log a warning message.
        
        Args:
            message: Log message
            **kwargs: Additional structured data
        """
        self._log("warning", message, kwargs)
    
    def debug(self, message: str, **kwargs):
        """
        Log a debug message.
        
        Args:
            message: Log message
            **kwargs: Additional structured data
        """
        self._log("debug", message, kwargs)


def get_logger(name: str) -> StructuredLogger:
    """
    Get a structured logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        StructuredLogger instance
    """
    return StructuredLogger(name)