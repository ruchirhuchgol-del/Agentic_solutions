"""
Security Decision Task for the DevSecOps Deployment Gatekeeper.
"""
from typing import Dict, Any
from crewai import Task
from ..agents.decision_engine import SecurityPolicyDecisionEngine

class ApplySecurityGateDecisionTask(Task):
    """Task for applying security gate decision."""
    
    def __init__(self, agent: SecurityPolicyDecisionEngine, config: Dict[str, Any]):
        # Extract values from config
        description = config.get('description', 'Apply security gate decision')
        expected_output = config.get('expected_output', 'Security decision')
        
        # Initialize the task with only the required parameters
        super().__init__(
            description=description,
            expected_output=expected_output,
            agent=agent
        )