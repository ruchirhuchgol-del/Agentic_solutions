"""
Security Notification Task for the DevSecOps Deployment Gatekeeper.
"""
from typing import Dict, Any
from crewai import Task
from ..agents.notification_manager import SecurityAlertNotificationManager

class DeliverSecurityAlertNotificationsTask(Task):
    """Task for delivering security alert notifications."""
    
    def __init__(self, agent: SecurityAlertNotificationManager, config: Dict[str, Any]):
        # Extract values from config
        description = config.get('description', 'Deliver security alert notifications')
        expected_output = config.get('expected_output', 'Notification delivery confirmation')
        
        # Initialize the task with only the required parameters
        super().__init__(
            description=description,
            expected_output=expected_output,
            agent=agent
        )