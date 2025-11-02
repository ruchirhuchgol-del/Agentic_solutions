from .base_task import BaseTask
from crewai import Task
from crewai.agent import Agent

class ExtractContextTask(BaseTask):
    """Task for extracting context and variables from a business problem."""

    def get_task(self) -> Task:
        """
        Creates the task for the Context Extractor agent.
        This is the first task in the sequence and has no dependencies.
        """
        return self._create_task(
            async_execution=False
        )