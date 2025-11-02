# src/hypothesis_generation_agent/tasks/base_task.py

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from crewai import Task
from crewai.agent import Agent

logger = logging.getLogger(__name__)

class BaseTask(ABC):
    """Base class for all tasks in the HGA system."""

    def __init__(self, config: Dict[str, Any], agent: Agent, tools: Optional[List] = None):
        """
        Initializes the task with its configuration, agent, and tools.

        Args:
            config (Dict[str, Any]): The task configuration loaded from tasks.yaml.
            agent (Agent): The CrewAI agent instance that will perform this task.
            tools (Optional[List]): A list of tools the agent can use for this task.
        """
        self.config = config
        self.agent = agent
        self.tools = tools or []
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @abstractmethod
    def get_task(self) -> Task:
        """
        Creates and returns the CrewAI Task object.
        Subclasses must implement this method to define the specific task.
        """
        pass

    def _create_task(self, **kwargs) -> Task:
        """
        A helper method to create the CrewAI Task with common parameters.

        Args:
            **kwargs: Additional keyword arguments to pass to the Task constructor.

        Returns:
            Task: The configured CrewAI Task instance.
        """
        task_params = {
            "description": self.config.get("description"),
            "expected_output": self.config.get("expected_output"),
            "agent": self.agent,
            "tools": self.tools,
            **kwargs
        }
        
        # Filter out None values for parameters like 'context'
        task_params = {k: v for k, v in task_params.items() if v is not None}
        
        self.logger.info(f"Creating task '{self.config.get('description', '').split('.')[0].strip()}' for agent '{self.agent.role}'")
        return Task(**task_params)