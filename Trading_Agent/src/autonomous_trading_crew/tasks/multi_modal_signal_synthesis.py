"""
Multi-Modal Signal Synthesis Task for the Autonomous Trading Crew
"""

def create_multi_modal_signal_synthesis(tasks_config):
    """Create and return the Multi-Modal Signal Synthesis task"""
    # Import here to avoid dependency issues during module loading
    from crewai import Task
    
    return Task(
        config=tasks_config["multi_modal_signal_synthesis"],
        markdown=False,
    )