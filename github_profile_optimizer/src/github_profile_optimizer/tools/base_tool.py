"""
Base tool interface with safety checks.

Provides the foundation for implementing specialized tools used by AI agents.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel
from ..utils.logger import get_logger


class BaseTool(ABC):
    """
    Abstract base class for all tools.
    
    This class defines the common interface and functionality for all tools
    used by AI agents in the GitHub Profile Optimizer system.
    """
    
    def __init__(self, dry_run: bool = True):
        """
        Initialize the base tool.
        
        Args:
            dry_run: Whether to run in dry-run mode
        """
        self.dry_run = dry_run
        self.logger = get_logger(self.__class__.__name__)
    
    @abstractmethod
    def execute(self, params: BaseModel) -> Dict[str, Any]:
        """
        Execute the tool with given parameters.
        
        Args:
            params: Tool-specific parameters as a Pydantic model
            
        Returns:
            Dict containing the result of the tool execution
        """
        pass
    
    def safety_check(self, params: BaseModel) -> bool:
        """
        Perform safety checks before execution.
        
        Args:
            params: Tool parameters
            
        Returns:
            True if safety checks pass, False otherwise
        """
        # Override for tool-specific safety checks
        return True
    
    @property
    def name(self) -> str:
        """Return the name of the tool."""
        return self.__class__.__name__
    
    @property
    def description(self) -> str:
        """Return the description of the tool."""
        return self.__doc__ or "No description available"