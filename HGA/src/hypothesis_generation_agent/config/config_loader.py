# src/hypothesis_generation_agent/config/config_loader.py
import os
import yaml
import logging
import logging.config
from typing import Dict, Any, Optional

class ConfigLoader:
    """Loads and manages configuration for the HGA system."""
    
    def __init__(self, config_dir: str = None):
        """Initialize the configuration loader."""
        if config_dir is None:
            # Default to the config directory relative to this file
            self.config_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            self.config_dir = config_dir
        
        self.llm_config = None
        self.logging_config = None
        self.agents_config = None
        self.tasks_config = None
        
        # Load all configurations
        self._load_configs()
    
    def _load_configs(self):
        """Load all configuration files."""
        # Load LLM configuration
        llm_config_path = os.path.join(self.config_dir, "llm_config.yaml")
        with open(llm_config_path, "r") as f:
            self.llm_config = yaml.safe_load(f)
        
        # Load logging configuration
        logging_config_path = os.path.join(self.config_dir, "logging_config.yaml")
        with open(logging_config_path, "r") as f:
            self.logging_config = yaml.safe_load(f)
        
        # Load agents configuration
        agents_config_path = os.path.join(self.config_dir, "agents.yaml")
        with open(agents_config_path, "r") as f:
            self.agents_config = yaml.safe_load(f)
        
        # Load tasks configuration
        tasks_config_path = os.path.join(self.config_dir, "tasks.yaml")
        with open(tasks_config_path, "r") as f:
            self.tasks_config = yaml.safe_load(f)
    
    def get_llm_config(self, model_name: str = None) -> Dict[str, Any]:
        """Get LLM configuration for a specific model or default."""
        if model_name is None:
            model_name = "default"
        
        # Check if it's a predefined model
        if model_name in self.llm_config.get("models", {}):
            return self.llm_config["models"][model_name]
        
        # Return default configuration
        return self.llm_config.get("default", {})
    
    def get_agent_llm_config(self, agent_name: str) -> Dict[str, Any]:
        """Get LLM configuration for a specific agent."""
        agent_configs = self.llm_config.get("agent_configs", {})
        
        if agent_name in agent_configs:
            model_name = agent_configs[agent_name].get("use_model", "default")
            return self.get_llm_config(model_name)
        
        # Return default configuration
        return self.get_llm_config("default")
    
    def setup_logging(self, environment: str = "development"):
        """Setup logging configuration for the specified environment."""
        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(os.path.dirname(self.config_dir), "..", "..", "logs")
        os.makedirs(logs_dir, exist_ok=True)
        
        # Apply environment-specific overrides if available
        config = self.logging_config.copy()
        env_config = config.get("environments", {}).get(environment, {})
        
        if env_config:
            # Merge environment-specific configuration
            for logger_name, logger_config in env_config.get("loggers", {}).items():
                if logger_name in config["loggers"]:
                    config["loggers"][logger_name].update(logger_config)
        
        # Apply the configuration
        logging.config.dictConfig(config)
        
        # Get the root logger
        logger = logging.getLogger()
        logger.info(f"Logging configured for environment: {environment}")
        
        return logger
    
    def get_agents_config(self) -> Dict[str, Any]:
        """Get the agents configuration."""
        return self.agents_config
    
    def get_tasks_config(self) -> Dict[str, Any]:
        """Get the tasks configuration."""
        return self.tasks_config
    
    def get_api_config(self, provider: str = "openai") -> Dict[str, Any]:
        """Get API configuration for a specific provider."""
        return self.llm_config.get("api", {}).get(provider, {})

# Global configuration instance
_config_loader = None

def get_config_loader(config_dir: str = None) -> ConfigLoader:
    """Get the global configuration loader instance."""
    global _config_loader
    if _config_loader is None:
        _config_loader = ConfigLoader(config_dir)
    return _config_loader

def setup_logging(environment: str = "development"):
    """Setup logging using the global configuration loader."""
    config_loader = get_config_loader()
    return config_loader.setup_logging(environment)