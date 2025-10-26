"""
Custom exceptions for the GitHub Profile Optimizer.

Defines custom exception classes for various error conditions in the application.
"""

from typing import Optional


class GitHubProfileOptimizerError(Exception):
    """
    Base exception for GitHub Profile Optimizer errors.
    
    Args:
        message: Error message
        details: Additional error details
    """
    
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class SafetyViolationError(GitHubProfileOptimizerError):
    """
    Raised when safety checks fail.
    
    This exception is raised when safety validations prevent an operation
    from proceeding due to potential risks or violations.
    """
    pass


class ConfigurationError(GitHubProfileOptimizerError):
    """
    Raised when configuration is invalid.
    
    This exception is raised when required configuration parameters
    are missing or have invalid values.
    """
    pass


class GitHubAPIError(GitHubProfileOptimizerError):
    """
    Raised when GitHub API calls fail.
    
    This exception is raised when there are issues communicating
    with the GitHub API, such as network errors or API limitations.
    """
    pass


class FileOperationError(GitHubProfileOptimizerError):
    """
    Raised when file operations fail.
    
    This exception is raised when there are issues performing
    file system operations, such as read, write, or permission errors.
    """
    pass


class StateManagementError(GitHubProfileOptimizerError):
    """
    Raised when state management operations fail.
    
    This exception is raised when there are issues with
    state persistence or retrieval operations.
    """
    pass