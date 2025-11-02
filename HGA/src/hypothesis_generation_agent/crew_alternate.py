import os
import json

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	FileReadTool
)






@CrewBase
class HypothesisGenerationAgentHgaCrew:
    """HypothesisGenerationAgentHga crew"""

    
    @agent
    def context_extractor(self) -> Agent:

        
        return Agent(
            config=self.agents_config["context_extractor"],
            
            
            tools=[

            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def hypothesis_generator(self) -> Agent:

        
        return Agent(
            config=self.agents_config["hypothesis_generator"],
            
            
            tools=[
				FileReadTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def test_recommender(self) -> Agent:

        
        return Agent(
            config=self.agents_config["test_recommender"],
            
            
            tools=[
				FileReadTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def reviewer(self) -> Agent:

        
        return Agent(
            config=self.agents_config["reviewer"],
            
            
            tools=[

            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def statistical_validator(self) -> Agent:

        
        return Agent(
            config=self.agents_config["statistical_validator"],
            
            
            tools=[

            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def hypothesis_refiner(self) -> Agent:

        
        return Agent(
            config=self.agents_config["hypothesis_refiner"],
            
            
            tools=[

            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def hypothesis_librarian(self) -> Agent:

        
        return Agent(
            config=self.agents_config["hypothesis_librarian"],
            
            
            tools=[
				FileReadTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    

    
    @task
    def extract_context_and_variables(self) -> Task:
        return Task(
            config=self.tasks_config["extract_context_and_variables"],
            markdown=False,
            
            
        )
    
    @task
    def generate_statistical_hypotheses(self) -> Task:
        return Task(
            config=self.tasks_config["generate_statistical_hypotheses"],
            markdown=False,
            
            
        )
    
    @task
    def recommend_statistical_test(self) -> Task:
        return Task(
            config=self.tasks_config["recommend_statistical_test"],
            markdown=False,
            
            
        )
    
    @task
    def validate_statistical_consistency(self) -> Task:
        return Task(
            config=self.tasks_config["validate_statistical_consistency"],
            markdown=False,
            
            
        )
    
    @task
    def review_and_format_output(self) -> Task:
        return Task(
            config=self.tasks_config["review_and_format_output"],
            markdown=False,
            
            
        )
    
    @task
    def store_generated_hypothesis(self) -> Task:
        return Task(
            config=self.tasks_config["store_generated_hypothesis"],
            markdown=False,
            
            
        )
    
    @task
    def refine_hypothesis_based_on_feedback(self) -> Task:
        return Task(
            config=self.tasks_config["refine_hypothesis_based_on_feedback"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the HypothesisGenerationAgentHga crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

    def _load_response_format(self, name):
        with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
            json_schema = json.loads(f.read())

        return SchemaConverter.build(json_schema)
