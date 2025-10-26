"""Dynamic tool loader and registry."""
from typing import Dict, Type, Any
import importlib
import os


class ToolRegistry:
    """Registry for dynamically loading and managing tools."""
    
    def __init__(self):
        """Initialize the tool registry."""
        self._tools: Dict[str, Type[Any]] = {}
    
    def register(self, name: str, tool_class: Type[Any]) -> None:
        """Register a tool class.
        
        Args:
            name: Name to register the tool under
            tool_class: The tool class to register
        """
        self._tools[name] = tool_class
    
    def get_tool(self, name: str, **kwargs) -> Any:
        """Get an instance of a registered tool.
        
        Args:
            name: Name of the tool to instantiate
            **kwargs: Arguments to pass to the tool constructor
            
        Returns:
            Instance of the requested tool
        """
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' not registered")
            
        tool_class = self._tools[name]
        return tool_class(**kwargs)
    
    def list_tools(self) -> list:
        """List all registered tools.
        
        Returns:
            List of registered tool names
        """
        return list(self._tools.keys())
    
    def load_tools_from_directory(self, directory: str) -> None:
        """Dynamically load all tools from a directory.
        
        Args:
            directory: Directory to load tools from
        """
        if not os.path.exists(directory):
            return
            
        for filename in os.listdir(directory):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]  # Remove .py extension
                try:
                    # Import the module
                    spec = importlib.util.spec_from_file_location(
                        module_name, 
                        os.path.join(directory, filename)
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Look for classes that might be tools
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (isinstance(attr, type) and 
                            hasattr(attr, 'name') and 
                            hasattr(attr, 'run')):
                            self.register(attr.name, attr)
                            
                except Exception as e:
                    print(f"Error loading tool from {filename}: {e}")


# Global tool registry instance
tool_registry = ToolRegistry()