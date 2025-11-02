from .base_agent import BaseAgent
from typing import Dict, Any, List

class ContextExtractor(BaseAgent):
    """Agent for extracting context and variables from business problems."""
    
    def __init__(self, config: Dict[str, Any], **kwargs):
        """Initialize the Context Extractor agent."""
        super().__init__(config=config, **kwargs)