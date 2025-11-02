from .base_task import BaseTask
from crewai import Task
from crewai.agent import Agent

class ReviewOutputTask(BaseTask):
    """Task for reviewing, synthesizing, and formatting the final output."""

    def get_task(self) -> Task:
        """
        Creates the task for the Reviewer agent.
        It depends on all preceding tasks to produce the final, polished output.
        """
        return self._create_task(
            context=self.config.get("context"),
            async_execution=False
        )