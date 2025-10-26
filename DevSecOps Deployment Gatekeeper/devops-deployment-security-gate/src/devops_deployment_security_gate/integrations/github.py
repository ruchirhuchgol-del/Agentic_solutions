"""
GitHub integration for the DevSecOps Deployment Gatekeeper.
This module provides low-level GitHub API integration functions.
"""
import requests
from typing import Dict, Any, Optional, List
from ..config.settings import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)

class GitHubIntegration:
    """Low-level GitHub API integration."""
    
    def __init__(self, token: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize GitHub integration.
        
        Args:
            token: GitHub personal access token
            base_url: GitHub API base URL
        """
        self.token = token or settings.github_token
        self.base_url = base_url or settings.github_api_base_url
    
    def get_pull_request(self, repository: str, pr_number: str) -> Dict[str, Any]:
        """
        Get pull request details from GitHub.
        
        Args:
            repository: Repository in format 'owner/repo'
            pr_number: Pull request number
            
        Returns:
            Dictionary containing PR details
            
        Raises:
            requests.exceptions.RequestException: If the request fails
            ValueError: If repository format is invalid
        """
        # Validate inputs
        if not repository or '/' not in repository:
            raise ValueError("Invalid repository format. Must be in 'owner/repo' format.")
        
        if not pr_number:
            raise ValueError("PR number is required")
        
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        url = f"{self.base_url}/repos/{repository}/pulls/{pr_number}"
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            logger.info(f"Retrieved PR #{pr_number} from {repository}")
            return response.json()
        except requests.exceptions.RequestException as e:
            error_message = f"Failed to get PR #{pr_number} from {repository}: {str(e)}"
            logger.error(error_message)
            raise
        except Exception as e:
            error_message = f"Unexpected error retrieving PR #{pr_number} from {repository}: {str(e)}"
            logger.error(error_message)
            raise
    
    def get_pull_request_files(self, repository: str, pr_number: str) -> List[Dict[str, Any]]:
        """
        Get files changed in a pull request.
        
        Args:
            repository: Repository in format 'owner/repo'
            pr_number: Pull request number
            
        Returns:
            List of dictionaries containing file information
            
        Raises:
            requests.exceptions.RequestException: If the request fails
            ValueError: If repository format is invalid
        """
        # Validate inputs
        if not repository or '/' not in repository:
            raise ValueError("Invalid repository format. Must be in 'owner/repo' format.")
        
        if not pr_number:
            raise ValueError("PR number is required")
        
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        url = f"{self.base_url}/repos/{repository}/pulls/{pr_number}/files"
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            logger.info(f"Retrieved files for PR #{pr_number} from {repository}")
            return response.json()
        except requests.exceptions.RequestException as e:
            error_message = f"Failed to get PR files for #{pr_number} from {repository}: {str(e)}"
            logger.error(error_message)
            raise
        except Exception as e:
            error_message = f"Unexpected error retrieving PR files for #{pr_number} from {repository}: {str(e)}"
            logger.error(error_message)
            raise
    
    def update_pull_request_status(self, repository: str, sha: str, state: str, 
                                 target_url: str, description: str, context: str) -> Dict[str, Any]:
        """
        Update the status of a pull request commit.
        
        Args:
            repository: Repository in format 'owner/repo'
            sha: Commit SHA
            state: Status state (pending, success, error, failure)
            target_url: Target URL for details
            description: Status description
            context: Status context
            
        Returns:
            Dictionary containing status update response
            
        Raises:
            requests.exceptions.RequestException: If the request fails
            ValueError: If repository format is invalid or required parameters are missing
        """
        # Validate inputs
        if not repository or '/' not in repository:
            raise ValueError("Invalid repository format. Must be in 'owner/repo' format.")
        
        if not sha:
            raise ValueError("Commit SHA is required")
        
        if not state:
            raise ValueError("State is required")
        
        if not context:
            raise ValueError("Context is required")
        
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        url = f"{self.base_url}/repos/{repository}/statuses/{sha}"
        
        payload = {
            "state": state,
            "target_url": target_url,
            "description": description,
            "context": context
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            logger.info(f"Updated PR status for commit {sha[:8]} in {repository}")
            return response.json()
        except requests.exceptions.RequestException as e:
            error_message = f"Failed to update PR status for commit {sha[:8]} in {repository}: {str(e)}"
            logger.error(error_message)
            raise
        except Exception as e:
            error_message = f"Unexpected error updating PR status for commit {sha[:8]} in {repository}: {str(e)}"
            logger.error(error_message)
            raise
    
    def create_pull_request_comment(self, repository: str, pr_number: str, body: str) -> Dict[str, Any]:
        """
        Create a comment on a pull request.
        
        Args:
            repository: Repository in format 'owner/repo'
            pr_number: Pull request number
            body: Comment body
            
        Returns:
            Dictionary containing comment information
            
        Raises:
            requests.exceptions.RequestException: If the request fails
            ValueError: If repository format is invalid or required parameters are missing
        """
        # Validate inputs
        if not repository or '/' not in repository:
            raise ValueError("Invalid repository format. Must be in 'owner/repo' format.")
        
        if not pr_number:
            raise ValueError("PR number is required")
        
        if not body:
            raise ValueError("Comment body is required")
        
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        url = f"{self.base_url}/repos/{repository}/issues/{pr_number}/comments"
        
        payload = {
            "body": body
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            logger.info(f"Created comment on PR #{pr_number} in {repository}")
            return response.json()
        except requests.exceptions.RequestException as e:
            error_message = f"Failed to create comment on PR #{pr_number} in {repository}: {str(e)}"
            logger.error(error_message)
            raise
        except Exception as e:
            error_message = f"Unexpected error creating comment on PR #{pr_number} in {repository}: {str(e)}"
            logger.error(error_message)
            raise

# Convenience functions
def get_github_integration(token: Optional[str] = None, base_url: Optional[str] = None) -> GitHubIntegration:
    """
    Get a GitHub integration instance.
    
    Args:
        token: GitHub personal access token
        base_url: GitHub API base URL
        
    Returns:
        GitHubIntegration instance
    """
    return GitHubIntegration(token, base_url)