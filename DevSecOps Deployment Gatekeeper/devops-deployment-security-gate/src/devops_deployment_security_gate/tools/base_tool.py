"""
Base Tool for the DevSecOps Deployment Gatekeeper.
This module provides a base class for all tools with common functionality.
"""
from crewai.tools import BaseTool
from typing import Dict, Any, Optional
from ..utils.logger import get_logger

class DevSecOpsBaseTool(BaseTool):
    """Base class for all DevSecOps tools with common functionality."""
    
    def __init__(self, **kwargs):
        """Initialize the base tool."""
        super().__init__(**kwargs)
        # Store logger in a way that doesn't conflict with Pydantic
        object.__setattr__(self, '_logger', get_logger(f"{self.__class__.__module__}.{self.__class__.__name__}"))
    
    @property
    def logger(self):
        """Get the logger instance."""
        return getattr(self, '_logger', None) or get_logger(f"{self.__class__.__module__}.{self.__class__.__name__}")
    
    def _run(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool.
        
        Args:
            **kwargs: Tool-specific arguments
            
        Returns:
            Dictionary containing tool results
        """
        raise NotImplementedError("Subclasses must implement _run method")
    
    def _handle_error(self, error: Exception, context: str = "") -> None:
        """
        Handle tool errors consistently.
        
        Args:
            error: The exception that occurred
            context: Additional context about where the error occurred
        """
        error_message = str(error)
        if context:
            error_message = f"{context}: {error_message}"
        
        self.logger.error(error_message)
        raise error
    
    def _validate_required_params(self, params: Dict[str, Any], required_params: list) -> None:
        """
        Validate that required parameters are present.
        
        Args:
            params: Dictionary of parameters
            required_params: List of required parameter names
        """
        missing_params = [param for param in required_params if param not in params or not params[param]]
        if missing_params:
            raise ValueError(f"Missing required parameters: {missing_params}")

# Export the base tool
__all__ = ["DevSecOpsBaseTool"]