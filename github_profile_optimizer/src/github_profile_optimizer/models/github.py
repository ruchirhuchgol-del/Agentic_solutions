"""
GitHub data models.

Provides Pydantic models for GitHub API data validation and serialization.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class GitHubProfile(BaseModel):
    """
    GitHub user profile model.
    
    Represents a GitHub user profile with all relevant fields
    for profile analysis and optimization.
    """
    login: str
    name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    company: Optional[str] = None
    blog: Optional[str] = None
    email: Optional[str] = None
    public_repos: int
    followers: int
    following: int
    created_at: datetime
    updated_at: datetime
    avatar_url: Optional[str] = None


class GitHubRepository(BaseModel):
    """
    GitHub repository model.
    
    Represents a GitHub repository with metadata for
    analysis and optimization purposes.
    """
    name: str
    description: Optional[str] = None
    language: Optional[str] = None
    stars: int = Field(alias="stargazers_count")
    forks: int
    private: bool
    updated_at: datetime
    
    class Config:
        allow_population_by_field_name = True


class GitHubParams(BaseModel):
    """
    Parameters for GitHub operations.
    
    Contains parameters required for GitHub API operations
    with validation and type checking.
    """
    token: str
    handle: str
    dry_run: bool = True


class Diff(BaseModel):
    """
    Diff model for tracking changes.
    
    Represents a difference between original and proposed content
    for change tracking and review purposes.
    """
    path: str
    original: str
    proposed: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Operation(BaseModel):
    """
    Operation model for tracking file operations.
    
    Represents a file operation with all necessary parameters
    for execution and tracking.
    """
    path: str
    content: str
    tool_name: str


class CheckResult(BaseModel):
    """
    Result of safety checks.
    
    Contains the results of safety validation operations
    with pass/fail status and detailed error information.
    """
    passed: bool
    errors: List[str] = Field(default_factory=list)