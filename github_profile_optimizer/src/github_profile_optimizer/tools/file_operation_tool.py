"""
File operation tool with safety checks.

Provides safe file operations with diffing capabilities for profile optimization.
"""

import os
import shutil
from typing import Dict, Any, Optional
from difflib import unified_diff
from .base_tool import BaseTool
from ..models.github import Operation, Diff
from ..utils.logger import get_logger


class FileOperationTool(BaseTool):
    """
    Tool for safe file operations with diffing capabilities.
    
    This tool provides methods for reading, writing, and manipulating files
    with built-in safety checks and diff generation.
    """
    
    def __init__(self, dry_run: bool = True):
        """
        Initialize file operation tool.
        
        Args:
            dry_run: Whether to run in dry-run mode
        """
        super().__init__(dry_run)
        self.logger = get_logger(self.__class__.__name__)
    
    def execute(self, params: Operation) -> Dict[str, Any]:
        """
        Execute file operation.
        
        Args:
            params: File operation parameters
            
        Returns:
            Dictionary containing operation result
        """
        if not self.safety_check(params):
            raise ValueError("Safety checks failed")
            
        try:
            # Generate diff
            diff = self.generate_diff(params)
            
            # In dry-run mode, just return the diff
            if self.dry_run:
                self.logger.info(f"Dry-run: Would apply changes to {params.path}")
                return {
                    "success": True,
                    "diff": diff.dict(),
                    "message": "Dry-run completed successfully"
                }
            
            # Apply changes in live mode
            self._apply_changes(params)
            self.logger.info(f"Successfully applied changes to {params.path}")
            
            return {
                "success": True,
                "diff": diff.dict(),
                "message": "Changes applied successfully"
            }
        except Exception as e:
            self.logger.error(f"Error executing file operation: {e}")
            raise
    
    def safety_check(self, params: Operation) -> bool:
        """
        Perform safety checks for file operations.
        
        Args:
            params: File operation parameters
            
        Returns:
            True if safety checks pass, False otherwise
        """
        # Check if path is absolute and within allowed directories
        if os.path.isabs(params.path):
            self.logger.error("Absolute paths are not allowed")
            return False
            
        # Prevent directory traversal
        if ".." in params.path:
            self.logger.error("Directory traversal detected")
            return False
            
        # Check file extension permissions
        allowed_extensions = {'.md', '.txt', '.py', '.json', '.yml', '.yaml'}
        _, ext = os.path.splitext(params.path)
        if ext and ext.lower() not in allowed_extensions:
            self.logger.error(f"File extension {ext} not allowed")
            return False
            
        return True
    
    def generate_diff(self, operation: Operation) -> Diff:
        """
        Generate diff for a file operation.
        
        Args:
            operation: File operation
            
        Returns:
            Diff object
        """
        original_content = ""
        if os.path.exists(operation.path):
            try:
                with open(operation.path, 'r', encoding='utf-8') as f:
                    original_content = f.read()
            except Exception as e:
                self.logger.warning(f"Could not read original file: {e}")
        
        return Diff(
            path=operation.path,
            original=original_content,
            proposed=operation.content,
            metadata={"tool": operation.tool_name}
        )
    
    def _apply_changes(self, params: Operation) -> None:
        """
        Apply changes to a file.
        
        Args:
            params: File operation parameters
        """
        # Create backup
        if os.path.exists(params.path):
            backup_path = f"{params.path}.backup"
            shutil.copy2(params.path, backup_path)
            self.logger.debug(f"Created backup at {backup_path}")
        
        # Write new content
        # Ensure directory exists
        os.makedirs(os.path.dirname(params.path), exist_ok=True)
        
        with open(params.path, 'w', encoding='utf-8') as f:
            f.write(params.content)