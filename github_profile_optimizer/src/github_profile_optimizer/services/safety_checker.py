"""
Pre-change validation service.

Provides validation and safety checking capabilities for GitHub profile operations.
"""

from typing import Dict, Any, List, Optional
import re
import os
from ..models.github import Operation, CheckResult, Diff
from ..utils.logger import get_logger


class SafetyChecker:
    """
    Service for validating changes before applying them to GitHub profiles.
    
    This service provides comprehensive validation and safety checking
    for all operations that modify GitHub profiles or repositories.
    """
    
    def __init__(self):
        """Initialize the safety checker."""
        self.logger = get_logger(self.__class__.__name__)
    
    def preflight_check(self, operations: List[Operation]) -> CheckResult:
        """
        Validate operations before execution.
        
        Args:
            operations: List of operations to validate
            
        Returns:
            Check result
        """
        errors = []
        
        # Check ownership
        ownership_result = self._check_ownership(operations)
        if not ownership_result.passed:
            errors.extend(ownership_result.errors)
            
        # Check license compliance
        license_result = self._check_license_compliance(operations)
        if not license_result.passed:
            errors.extend(license_result.errors)
            
        # Check branch protection
        branch_result = self._check_branch_protection(operations)
        if not branch_result.passed:
            errors.extend(branch_result.errors)
            
        return CheckResult(
            passed=len(errors) == 0,
            errors=errors
        )
    
    def generate_diff(self, operation: Operation) -> Diff:
        """
        Create reversible change records.
        
        Args:
            operation: Operation to generate diff for
            
        Returns:
            Diff object
        """
        # This would read the current file content
        original_content = ""
        try:
            if os.path.exists(operation.path):
                with open(operation.path, 'r', encoding='utf-8') as f:
                    original_content = f.read()
        except Exception as e:
            self.logger.warning(f"Could not read original file {operation.path}: {e}")
        
        return Diff(
            path=operation.path,
            original=original_content,
            proposed=operation.content,
            metadata={"tool": operation.tool_name}
        )
    
    def _check_ownership(self, operations: List[Operation]) -> CheckResult:
        """
        Check file ownership.
        
        Args:
            operations: List of operations to check
            
        Returns:
            Check result
        """
        # In a real implementation, this would check if the user has write access
        # to the repositories they're trying to modify
        errors = []
        for op in operations:
            # Placeholder for actual ownership check
            if not op.path:  # Example check
                errors.append(f"Invalid path: {op.path}")
                
        return CheckResult(
            passed=len(errors) == 0,
            errors=errors
        )
    
    def _check_license_compliance(self, operations: List[Operation]) -> CheckResult:
        """
        Check license compliance.
        
        Args:
            operations: List of operations to check
            
        Returns:
            Check result
        """
        # In a real implementation, this would check for license headers
        # and ensure compliance with existing licenses
        errors = []
        for op in operations:
            # Placeholder for actual license check
            if "proprietary" in op.content.lower():  # Example check
                errors.append(f"Proprietary content detected in {op.path}")
                
        return CheckResult(
            passed=len(errors) == 0,
            errors=errors
        )
    
    def _check_branch_protection(self, operations: List[Operation]) -> CheckResult:
        """
        Check branch protection rules.
        
        Args:
            operations: List of operations to check
            
        Returns:
            Check result
        """
        # In a real implementation, this would check if the target branch
        # has protection rules that would prevent these changes
        errors = []
        for op in operations:
            # Placeholder for actual branch protection check
            if op.path.startswith(".git/"):  # Example check
                errors.append(f"Modification of git files not allowed: {op.path}")
                
        return CheckResult(
            passed=len(errors) == 0,
            errors=errors
        )
    
    def validate_profile_update(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate profile update parameters.
        
        Args:
            updates: Dictionary of profile fields to update
            
        Returns:
            Validation results with any issues found
        """
        issues = []
        
        # Validate bio length
        bio = updates.get("bio")
        if bio and len(bio) > 160:
            issues.append({
                "field": "bio",
                "issue": "Bio exceeds 160 characters",
                "severity": "warning"
            })
            
        # Validate blog URL format
        blog = updates.get("blog")
        if blog and not self._is_valid_url(blog):
            issues.append({
                "field": "blog",
                "issue": "Blog URL format is invalid",
                "severity": "error"
            })
            
        # Validate email format
        email = updates.get("email")
        if email and not self._is_valid_email(email):
            issues.append({
                "field": "email",
                "issue": "Email format is invalid",
                "severity": "error"
            })
            
        # Validate company name
        company = updates.get("company")
        if company and len(company) > 100:
            issues.append({
                "field": "company",
                "issue": "Company name exceeds 100 characters",
                "severity": "warning"
            })
            
        return {
            "valid": len([issue for issue in issues if issue["severity"] == "error"]) == 0,
            "issues": issues
        }
    
    def validate_repository_changes(self, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate repository changes.
        
        Args:
            changes: List of repository changes to validate
            
        Returns:
            Validation results with any issues found
        """
        issues = []
        
        for i, change in enumerate(changes):
            # Validate description length
            description = change.get("description")
            if description and len(description) > 2000:
                issues.append({
                    "repository_index": i,
                    "field": "description",
                    "issue": "Description exceeds 2000 characters",
                    "severity": "warning"
                })
                
            # Validate topic count (GitHub allows up to 20 topics)
            topics = change.get("topics", [])
            if len(topics) > 20:
                issues.append({
                    "repository_index": i,
                    "field": "topics",
                    "issue": "Too many topics (maximum 20 allowed)",
                    "severity": "error"
                })
                
        return {
            "valid": len([issue for issue in issues if issue["severity"] == "error"]) == 0,
            "issues": issues
        }
    
    def sanitize_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize input data to prevent injection attacks.
        
        Args:
            data: Input data to sanitize
            
        Returns:
            Sanitized data
        """
        sanitized = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                # Remove potentially dangerous characters
                sanitized[key] = re.sub(r'[<>"\']', '', value)
            else:
                sanitized[key] = value
                
        return sanitized
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Check if a string is a valid URL.
        
        Args:
            url: String to validate
            
        Returns:
            True if valid URL, False otherwise
        """
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None
    
    def _is_valid_email(self, email: str) -> bool:
        """
        Check if a string is a valid email.
        
        Args:
            email: String to validate
            
        Returns:
            True if valid email, False otherwise
        """
        email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        return email_pattern.match(email) is not None