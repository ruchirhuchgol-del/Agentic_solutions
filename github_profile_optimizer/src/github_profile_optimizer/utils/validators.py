"""
Input sanitization utilities.

Provides input validation and sanitization capabilities for security and data integrity.
"""

import re
from typing import Any, Dict, List, Union
from ..utils.logger import get_logger


class InputValidator:
    """
    Utility class for validating and sanitizing inputs.
    
    Provides comprehensive input validation and sanitization
    to prevent security vulnerabilities and ensure data integrity.
    """
    
    def __init__(self):
        """Initialize the input validator."""
        self.logger = get_logger(self.__class__.__name__)
    
    @staticmethod
    def sanitize_string(text: str, max_length: int = 1000) -> str:
        """
        Sanitize a string input.
        
        Args:
            text: String to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized string
        """
        if not isinstance(text, str):
            text = str(text)
            
        # Truncate if too long
        if len(text) > max_length:
            text = text[:max_length]
            
        # Remove potentially dangerous characters
        text = re.sub(r'[<>"\']', '', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @staticmethod
    def validate_github_username(username: str) -> bool:
        """
        Validate a GitHub username format.
        
        Args:
            username: Username to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(username, str):
            return False
            
        # GitHub username rules:
        # - 1-39 characters
        # - Only alphanumeric characters and hyphens
        # - Cannot start or end with hyphen
        # - Cannot have consecutive hyphens in first two positions
        pattern = re.compile(r'^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38}$')
        return bool(pattern.match(username))
    
    @staticmethod
    def validate_repository_name(name: str) -> bool:
        """
        Validate a repository name format.
        
        Args:
            name: Repository name to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(name, str):
            return False
            
        # Repository name rules:
        # - 1-100 characters
        # - Cannot start or end with dot or hyphen
        # - Cannot contain consecutive dots
        # - Cannot be . or ..
        if name in ['.', '..']:
            return False
            
        if name.startswith('.') or name.startswith('-') or name.endswith('.') or name.endswith('-'):
            return False
            
        if '..' in name:
            return False
            
        # Basic character check
        if not re.match(r'^[a-zA-Z0-9._-]+$', name):
            return False
            
        return 1 <= len(name) <= 100
    
    @staticmethod
    def sanitize_dict(data: Dict[str, Any], allowed_keys: List[str]) -> Dict[str, Any]:
        """
        Sanitize a dictionary by filtering allowed keys.
        
        Args:
            data: Dictionary to sanitize
            allowed_keys: List of allowed keys
            
        Returns:
            Sanitized dictionary with only allowed keys
        """
        sanitized = {}
        
        for key in allowed_keys:
            if key in data:
                value = data[key]
                # Apply appropriate sanitization based on key
                if isinstance(value, str):
                    sanitized[key] = InputValidator.sanitize_string(value)
                else:
                    sanitized[key] = value
                    
        return sanitized
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email: Email to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(email, str):
            return False
            
        pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return bool(pattern.match(email))
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate URL format.
        
        Args:
            url: URL to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(url, str):
            return False
            
        pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return bool(pattern.match(url))


def validate_input(data: Union[Dict[str, Any], str], validator_type: str) -> bool:
    """
    Validate input using a specific validator.
    
    Args:
        data: Data to validate
        validator_type: Type of validation ('username', 'email', 'url', 'repo_name')
        
    Returns:
        True if valid, False otherwise
    """
    validator = InputValidator()
    
    if validator_type == "username":
        return validator.validate_github_username(data)
    elif validator_type == "email":
        return validator.validate_email(data)
    elif validator_type == "url":
        return validator.validate_url(data)
    elif validator_type == "repo_name":
        return validator.validate_repository_name(data)
    else:
        return False