"""
Decision Explanation Report Task for the Autonomous Trading Crew
"""

def create_decision_explanation_report(tasks_config):
    """Create and return the Decision Explanation Report task"""
    # Import here to avoid dependency issues during module loading
    from crewai import Task
    
    return Task(
        config=tasks_config["decision_explanation_report"],
        markdown=False,
    )