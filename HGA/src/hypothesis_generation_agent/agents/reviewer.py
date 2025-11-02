from .base_agent import BaseAgent
from typing import Dict, Any, List

class Reviewer(BaseAgent):
    """Agent for reviewing and formatting outputs."""
    
    def __init__(self, config: Dict[str, Any], **kwargs):
        """Initialize the Reviewer agent."""
        super().__init__(config=config, **kwargs)