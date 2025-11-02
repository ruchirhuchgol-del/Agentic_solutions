

import logging
from crewai import Crew, Process
from crewai.project import CrewBase

from .config import get_config_loader
from .agents import (
    ContextExtractor,
    HypothesisGenerator,
    TestRecommender,
    Reviewer,
    StatisticalValidator,
    HypothesisRefiner,
    HypothesisLibrarian
)
from .tasks import (
    ExtractContextTask,
    GenerateHypothesesTask,
    RecommendTestTask,
    ValidateConsistencyTask,
    ReviewOutputTask,
    StoreHypothesisTask,
    RefineHypothesisTask
)

logger = logging.getLogger(__name__)

# Mapping from configuration key to the actual agent class
AGENT_MAP = {
    "context_extractor": ContextExtractor,
    "hypothesis_generator": HypothesisGenerator,
    "test_recommender": TestRecommender,
    "reviewer": Reviewer,
    "statistical_validator": StatisticalValidator,
    "hypothesis_refiner": HypothesisRefiner,
    "hypothesis_librarian": HypothesisLibrarian,
}

# Mapping from configuration key to the actual task class
TASK_MAP = {
    "extract_context_and_variables": ExtractContextTask,
    "generate_statistical_hypotheses": GenerateHypothesesTask,
    "recommend_statistical_test": RecommendTestTask,
    "validate_statistical_consistency": ValidateConsistencyTask,
    "review_and_format_output": ReviewOutputTask,
    "store_generated_hypothesis": StoreHypothesisTask,
    "refine_hypothesis_based_on_feedback": RefineHypothesisTask,
}


@CrewBase
class HypothesisGenerationAgentHgaCrew:
    """HypothesisGenerationAgentHga crew"""

    def __init__(self):
        """Initializes the crew by loading configurations and setting up agents and tasks."""
        self.config_loader = get_config_loader()
        self.agents_config = self.agents_config = self.config_loader.get_agents_config()
        self.tasks_config = self.tasks_config = self.config_loader.get_tasks_config()
        
        self.agents = {}
        self.tasks = {}
        
        self._initialize_agents()
        self._initialize_tasks()
        
        logger.info("HGA Crew initialized successfully.")

    def _initialize_agents(self):
        """Instantiates all agent classes based on configuration."""
        logger.info("Initializing agents...")
        for agent_key, agent_config in self.agents_config.items():
            if agent_key in AGENT_MAP:
                agent_class = AGENT_MAP[agent_key]
                agent_instance = agent_class(config=agent_config).get_agent()
                self.agents[agent_key] = agent_instance
                logger.debug(f"Initialized agent: {agent_instance.role}")
            else:
                logger.warning(f"No agent class found for key: {agent_key}")

    def _initialize_tasks(self):
        """Instantiates all task classes, linking them to their respective agents."""
        logger.info("Initializing tasks...")
        for task_key, task_config in self.tasks_config.items():
            if task_key in TASK_MAP:
                task_class = TASK_MAP[task_key]
                
                # Find the agent for this task
                agent_key = task_config.get("agent")
                agent = self.agents.get(agent_key)
                
                if not agent:
                    logger.error(f"Agent '{agent_key}' not found for task '{task_key}'. Skipping task.")
                    continue
                
                task_instance = task_class(config=task_config, agent=agent).get_task()
                self.tasks[task_key] = task_instance
                logger.debug(f"Initialized task: {task_config.get('description', '').split('.')[0]}")
            else:
                logger.warning(f"No task class found for key: {task_key}")

    @crew
    def crew(self) -> Crew:
        """Creates and returns the CrewAI Crew instance."""
        return Crew(
            agents=list(self.agents.values()),
            tasks=list(self.tasks.values()),
            process=Process.sequential,
            verbose=True,
        )

    def kickoff(self, inputs: dict) -> str:
        """
        Kicks off the crew execution with the given inputs.

        Args:
            inputs (dict): A dictionary containing the inputs for the crew (e.g., business_problem).

        Returns:
            str: The final output from the crew.
        """
        logger.info(f"Kicking off crew with inputs: {inputs}")
        try:
            result = self.crew().kickoff(inputs=inputs)
            logger.info("Crew execution finished successfully.")
            return result
        except Exception as e:
            logger.error(f"An error occurred during crew execution: {e}", exc_info=True)
            # Re-raise the exception or return a formatted error message
            raise e