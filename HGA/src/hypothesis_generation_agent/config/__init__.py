import os
from dotenv import load_dotenv
from .config_loader import get_config_loader, setup_logging

# Load environment variables from .env file
load_dotenv()

# Setup logging
logger = setup_logging(os.getenv("ENVIRONMENT", "development"))

# Get configuration loader
config_loader = get_config_loader()

# Default LLM configuration
DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "gpt-4o-mini")
DEFAULT_LLM_TEMPERATURE = float(os.getenv("DEFAULT_LLM_TEMPERATURE", "0.7"))

# Agent configuration defaults
DEFAULT_MAX_ITER = int(os.getenv("DEFAULT_MAX_ITER", "25"))
DEFAULT_REASONING = os.getenv("DEFAULT_REASONING", "False").lower() == "true"
DEFAULT_INJECT_DATE = os.getenv("DEFAULT_INJECT_DATE", "True").lower() == "true"
DEFAULT_ALLOW_DELEGATION = os.getenv("DEFAULT_ALLOW_DELEGATION", "False").lower() == "true"

# Export configuration functions
__all__ = [
    "get_config_loader",
    "setup_logging",
    "DEFAULT_LLM_MODEL",
    "DEFAULT_LLM_TEMPERATURE",
    "DEFAULT_MAX_ITER",
    "DEFAULT_REASONING",
    "DEFAULT_INJECT_DATE",
    "DEFAULT_ALLOW_DELEGATION"
]