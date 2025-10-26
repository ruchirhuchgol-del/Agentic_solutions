"""
Risk Management Officer Agent for the Autonomous Trading Crew
"""

def create_risk_management_officer(agents_config):
    """Create and return the Risk Management Officer agent"""
    # Import here to avoid dependency issues during module loading
    from crewai import Agent
    from crewai_tools import SerperDevTool, ScrapeWebsiteTool
    from autonomous_trading_crew.tools.risk_assessment_tool import RiskAssessmentTool
    from autonomous_trading_crew.tools.financial_data_tool import FinancialDataTool
    
    return Agent(
        config=agents_config["risk_management_officer"],
        tools=[
            SerperDevTool(),
            ScrapeWebsiteTool(),
            RiskAssessmentTool(),
            FinancialDataTool()
        ],
        reasoning=True,  # Enable reasoning for risk analysis
        max_reasoning_attempts=5,
        inject_date=True,
        allow_delegation=False,
        max_iter=25,
        max_rpm=None,
        max_execution_time=None,
        # Add custom parameters for risk validation
        cache=True,
        verbose=True,
        memory=True,
        # Add risk-specific configuration
        risk_threshold=0.6,  # Minimum signal strength threshold
        risk_tolerance="medium",  # Default risk tolerance
    )