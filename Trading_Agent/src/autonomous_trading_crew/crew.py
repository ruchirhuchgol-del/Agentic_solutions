import os
from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Import our custom agents and tasks
from autonomous_trading_crew.agents.market_intelligence_analyst import create_market_intelligence_analyst
from autonomous_trading_crew.agents.risk_management_officer import create_risk_management_officer
from autonomous_trading_crew.agents.trade_execution_specialist import create_trade_execution_specialist
from autonomous_trading_crew.agents.explainability_reporter import create_explainability_reporter

from autonomous_trading_crew.tasks.multi_modal_signal_synthesis import create_multi_modal_signal_synthesis
from autonomous_trading_crew.tasks.risk_assessment_guardrail_check import create_risk_assessment_guardrail_check
from autonomous_trading_crew.tasks.tax_optimized_execution_plan import create_tax_optimized_execution_plan
from autonomous_trading_crew.tasks.decision_explanation_report import create_decision_explanation_report

@CrewBase
class AutonomousTradingCrewCrew:
    """AutonomousTradingCrew crew"""

    @agent
    def market_intelligence_analyst(self) -> Agent:
        return create_market_intelligence_analyst(self.agents_config)

    @agent
    def risk_management_officer(self) -> Agent:
        return create_risk_management_officer(self.agents_config)

    @agent
    def trade_execution_specialist(self) -> Agent:
        return create_trade_execution_specialist(self.agents_config)

    @agent
    def explainability_reporter(self) -> Agent:
        return create_explainability_reporter(self.agents_config)

    @task
    def multi_modal_signal_synthesis(self) -> Task:
        return create_multi_modal_signal_synthesis(self.tasks_config)

    @task
    def risk_assessment_guardrail_check(self) -> Task:
        return create_risk_assessment_guardrail_check(self.tasks_config)

    @task
    def tax_optimized_execution_plan(self) -> Task:
        return create_tax_optimized_execution_plan(self.tasks_config)

    @task
    def decision_explanation_report(self) -> Task:
        return create_decision_explanation_report(self.tasks_config)

    @crew
    def crew(self) -> Crew:
        """Creates the AutonomousTradingCrew crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
