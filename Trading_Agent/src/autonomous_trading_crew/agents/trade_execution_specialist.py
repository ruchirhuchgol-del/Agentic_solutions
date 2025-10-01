"""
Trade Execution Specialist Agent for the Autonomous Trading Crew
"""

def create_trade_execution_specialist(agents_config):
    """Create and return the Trade Execution Specialist agent"""
    # Import here to avoid dependency issues during module loading
    from crewai import Agent
    from crewai_tools import SerperDevTool, ScrapeWebsiteTool
    from autonomous_trading_crew.tools.financial_data_tool import FinancialDataTool
    
    # Try to import TaxOptimizationTool with error handling
    tools = [
        SerperDevTool(),
        ScrapeWebsiteTool(),
        FinancialDataTool()
    ]
    
    # Try to add TaxOptimizationTool, but don't fail if it has issues
    try:
        from autonomous_trading_crew.tools.tax_optimization_tool import TaxOptimizationTool
        tools.append(TaxOptimizationTool())
    except Exception as e:
        print(f"Warning: Could not initialize TaxOptimizationTool: {e}")
        # Continue without the tool rather than failing
    
    return Agent(
        config=agents_config["trade_execution_specialist"],
        tools=tools,
        reasoning=True,  # Enable reasoning for execution planning
        max_reasoning_attempts=5,
        inject_date=True,
        allow_delegation=False,
        max_iter=25,
        max_rpm=None,
        max_execution_time=None,
        # Add custom parameters for execution planning
        cache=True,
        verbose=True,
        memory=True,
        # Add execution-specific configuration
        default_order_type="limit",  # Default order type
        max_position_size=0.05,  # 5% max position size
    )