
from abc import ABC
from crewai import Agent, LLM
from typing import Dict, Any, List
import os
from ..config import get_config_loader

class BaseAgent(ABC):
    """Base class for all agents in the HGA system."""
    
    def __init__(self, config: Dict[str, Any], tools: List = None, **kwargs):
        """Initialize the agent with configuration and tools."""
        self.config = config
        self.tools = tools or []
        self._setup_agent(**kwargs)
    
    def _setup_agent(self, **kwargs):
        """Setup the CrewAI agent with common configurations."""
        # Get configuration loader
        config_loader = get_config_loader()
        
        # Get agent name from config
        agent_name = self.config.get("role", "").lower().replace(" ", "_")
        
        # Get LLM configuration for this agent
        llm_config_dict = config_loader.get_agent_llm_config(agent_name)
        
        # Override with environment variables if provided
        llm_config_dict["model"] = os.getenv("DEFAULT_LLM_MODEL", llm_config_dict.get("model", "gpt-4o-mini"))
        llm_config_dict["temperature"] = float(os.getenv("DEFAULT_LLM_TEMPERATURE", llm_config_dict.get("temperature", 0.7)))
        
        # Create LLM instance
        llm_config = kwargs.pop('llm', None)
        if not llm_config:
            llm_config = LLM(**llm_config_dict)
        
        # Default agent parameters
        default_params = {
            "reasoning": os.getenv("DEFAULT_REASONING", "False").lower() == "true",
            "max_reasoning_attempts": None,
            "inject_date": os.getenv("DEFAULT_INJECT_DATE", "True").lower() == "true",
            "allow_delegation": os.getenv("DEFAULT_ALLOW_DELEGATION", "False").lower() == "true",
            "max_iter": int(os.getenv("DEFAULT_MAX_ITER", "25")),
            "max_rpm": None,
            "max_execution_time": None,
            "llm": llm_config,
        }
        
        # Merge with provided parameters
        params = {**default_params, **kwargs}
        
        self.agent = Agent(
            config=self.config,
            tools=self.tools,
            **params
        )
    
    def get_agent(self):
        """Return the CrewAI agent instance."""
        return self.agent