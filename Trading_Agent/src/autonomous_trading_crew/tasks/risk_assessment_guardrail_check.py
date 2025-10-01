"""
Risk Assessment Guardrail Check Task for the Autonomous Trading Crew
"""

def create_risk_assessment_guardrail_check(tasks_config):
    """Create and return the Risk Assessment Guardrail Check task"""
    # Import here to avoid dependency issues during module loading
    from crewai import Task
    
    return Task(
        config=tasks_config["risk_assessment_guardrail_check"],
        markdown=False,
    )