from .base_agent import BaseAgent
from typing import Dict, Any, List
from crewai_tools import FileReadTool

class HypothesisLibrarian(BaseAgent):
    """Agent for managing the hypothesis library."""
    
    def __init__(self, config: Dict[str, Any], **kwargs):
        """Initialize the Hypothesis Librarian agent."""
        # Add FileReadTool for accessing existing hypotheses
        tools = kwargs.pop('tools', [])
        tools.append(FileReadTool())
        
        super().__init__(config=config, tools=tools, **kwargs)