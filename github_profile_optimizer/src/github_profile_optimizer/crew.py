"""
Enhanced crew orchestration with new agent and tool integrations.

Provides orchestration capabilities for coordinating multiple AI agents in profile optimization tasks.
"""

import os
from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool
from src.github_profile_optimizer.tools.github_client import GitHubProfileTool
from src.github_profile_optimizer.tools.file_operation_tool import FileOperationTool
from src.github_profile_optimizer.services.audit_service import AuditService
from src.github_profile_optimizer.services.optimization_engine import OptimizationEngine


@CrewBase
class GithubProfileOptimizerCrew:
    """Enhanced GithubProfileOptimizer crew with new capabilities."""

    @agent
    def github_automation_agent(self) -> Agent:
        """Create the GitHub automation agent."""
        return Agent(
            config=self.agents_config["github_automation_agent"],
            tools=[
                ScrapeWebsiteTool(),
                GitHubProfileTool(),
                FileOperationTool()
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
    def profile_analyst_agent(self) -> Agent:
        """Create the profile analyst agent."""
        return Agent(
            config=self.agents_config["profile_analyst_agent"],
            tools=[
                ScrapeWebsiteTool()
            ],
            reasoning=True,
            allow_delegation=True,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.5,
            ),
        )

    @agent
    def optimization_specialist_agent(self) -> Agent:
        """Create the optimization specialist agent."""
        return Agent(
            config=self.agents_config["optimization_specialist_agent"],
            tools=[
                ScrapeWebsiteTool()
            ],
            reasoning=True,
            allow_delegation=True,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.3,
            ),
        )

    @task
    def analyze_github_profile(self) -> Task:
        """Create the profile analysis task."""
        return Task(
            config=self.tasks_config["analyze_github_profile"],
            agent=self.github_automation_agent(),
            markdown=False,
        )

    @task
    def generate_optimizations(self) -> Task:
        """Create the optimization generation task."""
        return Task(
            config=self.tasks_config["generate_optimizations"],
            agent=self.optimization_specialist_agent(),
            markdown=False,
        )

    @task
    def implement_optimizations(self) -> Task:
        """Create the optimization implementation task."""
        return Task(
            config=self.tasks_config["implement_optimizations"],
            agent=self.github_automation_agent(),
            markdown=False,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the enhanced GithubProfileOptimizer crew."""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )