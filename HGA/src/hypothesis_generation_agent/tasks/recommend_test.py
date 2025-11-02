from .base_task import BaseTask
from crewai import Task
from crewai.agent import Agent
from ..tools import CustomFileReadTool, QdrantVectorSearchTool

class RecommendTestTask(BaseTask):
    """Task for recommending an appropriate statistical test."""

    def __init__(self, config: dict, agent: Agent):
        tools = [CustomFileReadTool(), QdrantVectorSearchTool()]
        super().__init__(config, agent, tools)

    def get_task(self) -> Task:
        """
        Creates the task for the Test Recommender agent.
        It also depends on the initial context extraction.
        """
        return self._create_task(
            context=[self.config.get("context")],
            async_execution=False
        )