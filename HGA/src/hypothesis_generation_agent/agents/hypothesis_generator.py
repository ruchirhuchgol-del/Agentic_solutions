from .base_agent import BaseAgent
from typing import Dict, Any, List
from crewai_tools import FileReadTool

class HypothesisGenerator(BaseAgent):
    """Agent for generating statistical hypotheses."""
    
    def __init__(self, config: Dict[str, Any], **kwargs):
        """Initialize the Hypothesis Generator agent."""
        # Add FileReadTool for accessing knowledge base
        tools = kwargs.pop('tools', [])
        tools.append(FileReadTool())
        
        super().__init__(config=config, tools=tools, **kwargs)