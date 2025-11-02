from .base_task import BaseTask
from crewai import Task
from crewai.agent import Agent
from ..tools import CustomFileReadTool, QdrantVectorSearchTool

class GenerateHypothesesTask(BaseTask):
    """Task for generating statistical hypotheses based on extracted context."""

    def __init__(self, config: dict, agent: Agent):
        # Initialize with the tools the agent needs
        tools = [CustomFileReadTool(), QdrantVectorSearchTool()]
        super().__init__(config, agent, tools)

    def get_task(self) -> Task:
        """
        Creates the task for the Hypothesis Generator agent.
        It depends on the output of the context extraction task.
        """
        return self._create_task(
            context=[self.config.get("context")],
            async_execution=False
        )