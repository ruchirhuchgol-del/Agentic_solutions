"""
SonarQube Security Scan Task for the DevSecOps Deployment Gatekeeper.
"""
from typing import Dict, Any
from crewai import Task
from ..agents.scanner_agent import SonarQubeSecurityScanner

class ExecuteSonarQubeSecurityScanTask(Task):
    """Task for executing SonarQube security scan."""
    
    def __init__(self, agent: SonarQubeSecurityScanner, config: Dict[str, Any]):
        # Extract values from config
        description = config.get('description', 'Execute SonarQube security scan')
        expected_output = config.get('expected_output', 'Security scan report')
        
        # Initialize the task with only the required parameters
        super().__init__(
            description=description,
            expected_output=expected_output,
            agent=agent
        )