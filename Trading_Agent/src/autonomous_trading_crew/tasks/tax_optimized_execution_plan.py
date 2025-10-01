"""
Tax Optimized Execution Plan Task for the Autonomous Trading Crew
"""

def create_tax_optimized_execution_plan(tasks_config):
    """Create and return the Tax Optimized Execution Plan task"""
    # Import here to avoid dependency issues during module loading
    from crewai import Task
    
    return Task(
        config=tasks_config["tax_optimized_execution_plan"],
        markdown=False,
    )