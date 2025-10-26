"""
GitHub API tool using PyGithub.

Provides functionality for interacting with the GitHub API to analyze and update profiles.
"""

from typing import Dict, Any, List, Optional
from github import Github
import os
from .base_tool import BaseTool
from ..models.github import GitHubParams, GitHubProfile, GitHubRepository
from ..services.safety_checker import SafetyChecker
from ..utils.logger import get_logger
from ..utils.cache_manager import cache_manager
from ..utils.rate_limiter import rate_limiter, RateLimitExceeded


class SafetyViolationError(Exception):
    """
    Exception raised for safety violations.
    
    This exception is raised when safety validations prevent a GitHub operation
    from proceeding due to potential risks or violations.
    """
    pass


class GitHubProfileTool(BaseTool):
    """
    Tool for interacting with GitHub API to analyze and update profiles.
    
    This tool provides methods for fetching GitHub profile and repository data,
    with built-in caching and rate limiting capabilities.
    """
    
    def __init__(self, dry_run: bool = True):
        """
        Initialize GitHub client tool.
        
        Args:
            dry_run: Whether to run in dry-run mode
        """
        super().__init__(dry_run)
        self.safety_checker = SafetyChecker()
        self.logger = get_logger(self.__class__.__name__)
    
    def execute(self, params: GitHubParams) -> Dict[str, Any]:
        """
        Execute GitHub profile analysis.
        
        Args:
            params: GitHub parameters
            
        Returns:
            Dictionary containing profile and repository information
        """
        if not self.safety_check(params):
            raise SafetyViolationError("GitHub token validation failed")
            
        try:
            github = Github(params.token)
            user = github.get_user(params.handle)
            
            return {
                "profile": self._parse_profile(user),
                "repos": self._parse_repos(user.get_repos())
            }
        except Exception as e:
            self.logger.error(f"Error executing GitHub tool: {e}")
            raise
    
    def safety_check(self, params: GitHubParams) -> bool:
        """
        Perform safety checks for GitHub operations.
        
        Args:
            params: GitHub parameters
            
        Returns:
            True if safety checks pass, False otherwise
        """
        # Validate token format
        if not params.token or len(params.token) < 10:
            self.logger.error("Invalid GitHub token")
            return False
            
        # Validate handle format
        if not params.handle or len(params.handle) < 1:
            self.logger.error("Invalid GitHub handle")
            return False
            
        return True
    
    def _parse_profile(self, user) -> Dict[str, Any]:
        """
        Parse GitHub user profile with caching.
        
        Args:
            user: GitHub user object
            
        Returns:
            Dictionary representation of user profile
        """
        cache_key = f"github_profile_{user.login}"
        
        # Check cache first
        cached_profile = cache_manager.get(cache_key)
        if cached_profile:
            self.logger.debug(f"Cache hit for profile {user.login}")
            return cached_profile
        
        # Check rate limit
        try:
            rate_limiter.api_call(f"/users/{user.login}")
        except RateLimitExceeded:
            self.logger.warning(f"Rate limit exceeded for profile {user.login}")
            # Return cached data if available, even if stale
            if cached_profile:
                return cached_profile
            # Otherwise, raise the exception
            raise
        
        profile_data = {
            "login": user.login,
            "name": user.name,
            "bio": user.bio,
            "location": user.location,
            "company": user.company,
            "blog": user.blog,
            "email": user.email,
            "public_repos": user.public_repos,
            "followers": user.followers,
            "following": user.following,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "avatar_url": user.avatar_url
        }
        
        # Cache the result for 1 hour
        cache_manager.set(cache_key, profile_data)
        
        return profile_data
    
    def _parse_repos(self, repos) -> List[Dict[str, Any]]:
        """
        Parse GitHub repositories with caching.
        
        Args:
            repos: GitHub repository iterator
            
        Returns:
            List of repository dictionaries
        """
        repo_list = []
        
        for repo in repos:
            cache_key = f"github_repo_{repo.owner.login}_{repo.name}"
            
            # Check cache first
            cached_repo = cache_manager.get(cache_key)
            if cached_repo:
                self.logger.debug(f"Cache hit for repository {repo.name}")
                repo_list.append(cached_repo)
                continue
            
            # Check rate limit
            try:
                rate_limiter.api_call(f"/repos/{repo.owner.login}/{repo.name}")
            except RateLimitExceeded:
                self.logger.warning(f"Rate limit exceeded for repository {repo.name}")
                # Return cached data if available, even if stale
                if cached_repo:
                    repo_list.append(cached_repo)
                    continue
                # Otherwise, raise the exception
                raise
            
            repo_data = {
                "name": repo.name,
                "description": repo.description,
                "language": repo.language,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "private": repo.private,
                "updated_at": repo.updated_at
            }
            
            # Cache the result for 1 hour
            cache_manager.set(cache_key, repo_data)
            repo_list.append(repo_data)
            
        return repo_list