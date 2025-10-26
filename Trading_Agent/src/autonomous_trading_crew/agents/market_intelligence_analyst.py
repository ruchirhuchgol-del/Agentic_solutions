from crewai import Agent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from autonomous_trading_crew.tools.financial_data_tool import FinancialDataTool
from autonomous_trading_crew.tools.financial_sentiment_tool import FinancialSentimentTool

def create_market_intelligence_analyst(agents_config):
    """Create and return the Market Intelligence Analyst agent"""
    # Import PredictiveAnalyticsTool with error handling
    tools = [
        SerperDevTool(),
        ScrapeWebsiteTool(),
        FinancialDataTool(),
        FinancialSentimentTool()
    ]
    
    # Try to add PredictiveAnalyticsTool, but don't fail if it has issues
    try:
        from autonomous_trading_crew.tools.predictive_analytics_tool import PredictiveAnalyticsTool
        tools.append(PredictiveAnalyticsTool())
    except Exception as e:
        print(f"Warning: Could not initialize PredictiveAnalyticsTool: {e}")
        # Continue without the tool rather than failing
    
    return Agent(
        config=agents_config["market_intelligence_analyst"],
        tools=tools,
        reasoning=True,  # Enable reasoning for complex analysis
        max_reasoning_attempts=5,  # Allow multiple reasoning attempts
        inject_date=True,
        allow_delegation=False,
        max_iter=25,
        max_rpm=None,
        max_execution_time=None,
        # Add custom parameters for task requirements
        cache=True,  # Enable caching for repeated queries
        verbose=True,  # Enable detailed logging
        memory=True,  # Enable memory for context retention
    )