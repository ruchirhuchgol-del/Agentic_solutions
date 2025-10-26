"""
Environment settings and configuration.

Provides centralized configuration management for the application.
"""

import os
from typing import Optional
from ..utils.logger import get_logger


class Settings:
    """
    Application settings loaded from environment variables.
    
    Centralized configuration management with environment variable
    override capabilities and runtime configuration access.
    """
    
    def __init__(self):
        """Initialize settings from environment variables."""
        # GitHub settings
        self.github_token: Optional[str] = os.getenv("GITHUB_TOKEN")
        self.github_username: Optional[str] = os.getenv("GITHUB_USERNAME")
        
        # Redis settings
        self.redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
        
        # Application settings
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.debug: bool = os.getenv("DEBUG", "False").lower() == "true"
        
        # API settings
        self.api_host: str = os.getenv("API_HOST", "0.0.0.0")
        self.api_port: int = int(os.getenv("API_PORT", "8000"))
        
        # Rate limiting
        self.rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "1000"))
        self.rate_limit_period: int = int(os.getenv("RATE_LIMIT_PERIOD", "3600"))  # seconds
    
    @property
    def is_production(self) -> bool:
        """
        Check if running in production mode.
        
        Returns:
            True if in production, False otherwise
        """
        return not self.debug and os.getenv("ENVIRONMENT") == "production"
    
    @property
    def is_development(self) -> bool:
        """
        Check if running in development mode.
        
        Returns:
            True if in development, False otherwise
        """
        return self.debug or os.getenv("ENVIRONMENT") == "development"


# Global settings instance
settings = Settings()