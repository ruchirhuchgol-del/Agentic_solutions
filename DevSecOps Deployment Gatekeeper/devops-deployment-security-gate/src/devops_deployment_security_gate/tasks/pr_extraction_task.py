"""
PR Extraction Task for the DevSecOps Deployment Gatekeeper.
"""
from typing import Dict, Any
from crewai import Task
from ..agents.pr_extractor import PRMetadataExtractionSpecialist

class ExtractPRSecurityContextTask(Task):
    """Task for extracting PR security context."""
    
    def __init__(self, agent: PRMetadataExtractionSpecialist, config: Dict[str, Any]):
        # Extract values from config
        description = config.get('description', 'Extract PR security context')
        expected_output = config.get('expected_output', 'PR metadata')
        
        # Initialize the task with only the required parameters
        super().__init__(
            description=description,
            expected_output=expected_output,
            agent=agent
        )