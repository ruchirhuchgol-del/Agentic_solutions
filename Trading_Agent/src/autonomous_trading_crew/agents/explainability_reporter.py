"""
Explainability Reporter Agent for the Autonomous Trading Crew
"""

def create_explainability_reporter(agents_config):
    """Create and return the Explainability Reporter agent"""
    # Import here to avoid dependency issues during module loading
    from crewai import Agent
    from autonomous_trading_crew.tools.financial_data_tool import FinancialDataTool
    from autonomous_trading_crew.tools.risk_assessment_tool import RiskAssessmentTool
    from autonomous_trading_crew.tools.predictive_analytics_tool import PredictiveAnalyticsTool
    # Add report generation tool
    from autonomous_trading_crew.tools.report_generator_tool import ReportGeneratorTool
    
    return Agent(
        config=agents_config["explainability_reporter"],
        tools=[
            FinancialDataTool(),
            RiskAssessmentTool(),
            PredictiveAnalyticsTool(),
            ReportGeneratorTool()  # Add report generation tool
        ],
        reasoning=True,  # Enable reasoning for report synthesis
        max_reasoning_attempts=5,
        inject_date=True,
        allow_delegation=False,
        max_iter=25,
        max_rpm=None,
        max_execution_time=None,
        # Add custom parameters for report generation
        cache=True,
        verbose=True,
        memory=True,
        # Add report-specific configuration
        report_format="markdown",  # Default report format
        include_appendix=True,  # Include supporting data appendix
    )