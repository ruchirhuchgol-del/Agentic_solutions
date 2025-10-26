"""
Abstract agent base class.

Provides the foundation for implementing specialized AI agents for GitHub profile optimization.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from src.github_profile_optimizer.tools.base_tool import BaseTool


class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    
    This class defines the common interface and functionality for all AI agents
    used in the GitHub Profile Optimizer system.
    """
    
    def __init__(self, name: str, tools: List[BaseTool]):
        """
        Initialize the agent.
        
        Args:
            name: Name of the agent
            tools: List of tools available to the agent
        """
        self.name = name
        self.tools = tools
    
    @abstractmethod
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task.
        
        Args:
            task: Task definition dictionary
            
        Returns:
            Result of the task execution
        """
        pass
    
    def get_available_tools(self) -> List[str]:
        """
        Get list of available tool names.
        
        Returns:
            List of tool names
        """
        return [tool.name for tool in self.tools]
    
    def run_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Run a specific tool by name.
        
        Args:
            tool_name: Name of the tool to run
            **kwargs: Arguments to pass to the tool
            
        Returns:
            Result from the tool execution
        """
        for tool in self.tools:
            if tool.name == tool_name:
                return tool.run(**kwargs)
        
        raise ValueError(f"Tool '{tool_name}' not found")