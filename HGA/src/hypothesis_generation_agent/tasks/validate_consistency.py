from .base_task import BaseTask
from crewai import Task
from crewai.agent import Agent
from ..tools import ValidateHypothesisTestAlignmentTool

class ValidateConsistencyTask(BaseTask):
    """Task for validating the logical consistency of the analysis components."""

    def __init__(self, config: dict, agent: Agent):
        tools = [ValidateHypothesisTestAlignmentTool()]
        super().__init__(config, agent, tools)

    def get_task(self) -> Task:
        """
        Creates the task for the Statistical Validator agent.
        It depends on the outputs of context, hypotheses, and test recommendation.
        """
        return self._create_task(
            context=self.config.get("context"),
            async_execution=False
        )