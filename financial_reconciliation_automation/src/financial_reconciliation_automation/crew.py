import os
from typing import Type
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, DirectoryReadTool, CSVSearchTool

# Import our custom tools
from .tools.financial_tools import (
    match_transactions, validate_data, generate_report
)
from .tools.langchain_tools import (
    DiscrepancyAnalysisTool, TransactionCategorizationTool
)
from .utils.data_loader import load_csv_data
from .utils.validators import (
    validate_transaction_data, validate_invoice_data
)
from .utils.formatters import (
    format_matching_results_as_text
)

@CrewBase
class FinancialReconciliationCrew:
    """FinancialReconciliation crew with enhanced capabilities"""

    @agent
    def financial_data_collector(self) -> Agent:
        return Agent(
            config=self.agents_config["financial_data_collector"],
            tools=[
                FileReadTool(),
                DirectoryReadTool()
                # CSVSearchTool(csv='./data/financial_transactions.csv')
            ],
            verbose=True,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.2,
            )
        )

    @agent
    def transaction_matching_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["transaction_matching_specialist"],
            tools=[
                FileReadTool()
                # CSVSearchTool(csv='./data/financial_transactions.csv'),
                # DiscrepancyAnalysisTool()
            ],
            verbose=True,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.1,
            )
        )

    @agent
    def discrepancy_reporter(self) -> Agent:
        return Agent(
            config=self.agents_config["discrepancy_reporter"],
            tools=[
                FileReadTool()
                # TransactionCategorizationTool()
            ],
            verbose=True,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.3,
            )
        )

    @agent
    def data_quality_validator(self) -> Agent:
        return Agent(
            config=self.agents_config["data_quality_validator"],
            tools=[
                FileReadTool()
                # CSVSearchTool(csv='./data/financial_transactions.csv')
            ],
            verbose=True,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.1,
            )
        )

    @task
    def validate_data_quality_and_integrity(self) -> Task:
        return Task(
            config=self.tasks_config["validate_data_quality_and_integrity"],
            agent=self.data_quality_validator()
        )

    @task
    def fetch_financial_data(self) -> Task:
        return Task(
            config=self.tasks_config["fetch_financial_data"],
            agent=self.financial_data_collector(),
            context=[self.validate_data_quality_and_integrity()]
        )

    @task
    def match_transactions_and_invoices(self) -> Task:
        return Task(
            config=self.tasks_config["match_transactions_and_invoices"],
            agent=self.transaction_matching_specialist(),
            context=[self.fetch_financial_data()]
        )

    @task
    def generate_reconciliation_report_and_alerts(self) -> Task:
        return Task(
            config=self.tasks_config["generate_reconciliation_report_and_alerts"],
            agent=self.discrepancy_reporter(),
            context=[self.match_transactions_and_invoices()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the FinancialReconciliation crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )