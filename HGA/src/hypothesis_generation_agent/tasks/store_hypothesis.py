from .base_task import BaseTask
from crewai import Task
from crewai.agent import Agent

class RefineHypothesisTask(BaseTask):
    """
    Task for refining an existing hypothesis based on user feedback.
    This is an on-demand task, not part of the main sequential workflow.
    """

    def get_task(self) -> Task:
        """
        Creates the task for the Hypothesis Refiner agent.
        The context for this task would be dynamically provided when called,
        including the original output and the user's feedback.
        """
        # The context is not defined in the YAML because it's dynamic.
        # It will be passed when this task is instantiated and run.
        return self._create_task(
            # Context will be passed programmatically, e.g.,
            # context=[original_output_task, user_feedback_dict]
            async_execution=False
        )