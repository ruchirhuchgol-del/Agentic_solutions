from .base_agent import BaseAgent
from typing import Dict, Any, List
from crewai_tools import FileReadTool

class TestRecommender(BaseAgent):
    """Agent for recommending statistical tests."""
    
    def __init__(self, config: Dict[str, Any], **kwargs):
        """Initialize the Test Recommender agent."""
        # Add FileReadTool for accessing knowledge base
        tools = kwargs.pop('tools', [])
        tools.append(FileReadTool())
        
        super().__init__(config=config, tools=tools, **kwargs)