"""Safe file editor with diffing capabilities."""
import os
import shutil
from typing import Optional
from difflib import unified_diff


class FileOperations:
    """Safe file operations with backup and diffing support."""
    
    @staticmethod
    def read_file(file_path: str) -> str:
        """Read content from a file.
        
        Args:
            file_path: Path to the file to read
            
        Returns:
            Content of the file as string
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def write_file(file_path: str, content: str, backup: bool = True) -> bool:
        """Write content to a file with optional backup.
        
        Args:
            file_path: Path to the file to write
            content: Content to write to the file
            backup: Whether to create a backup before writing
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create backup if requested and file exists
            if backup and os.path.exists(file_path):
                backup_path = f"{file_path}.backup"
                shutil.copy2(file_path, backup_path)
            
            # Write new content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return True
        except Exception as e:
            print(f"Error writing file: {e}")
            return False
    
    @staticmethod
    def show_diff(old_content: str, new_content: str, file_name: str = "file") -> str:
        """Show unified diff between old and new content.
        
        Args:
            old_content: Original content
            new_content: New content
            file_name: Name of the file for diff header
            
        Returns:
            Unified diff as string
        """
        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)
        
        diff = unified_diff(
            old_lines, 
            new_lines, 
            fromfile=f'a/{file_name}', 
            tofile=f'b/{file_name}'
        )
        
        return ''.join(diff)
    
    @staticmethod
    def create_backup(file_path: str) -> Optional[str]:
        """Create a backup of a file.
        
        Args:
            file_path: Path to the file to backup
            
        Returns:
            Path to the backup file, or None if failed
        """
        try:
            if os.path.exists(file_path):
                backup_path = f"{file_path}.backup"
                shutil.copy2(file_path, backup_path)
                return backup_path
        except Exception as e:
            print(f"Error creating backup: {e}")
            
        return None