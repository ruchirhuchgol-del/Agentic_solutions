"""
Data models for GitHub Profile Optimizer.

Contains Pydantic models for data validation and serialization.
"""

from .github import (
    GitHubProfile,
    GitHubRepository,
    GitHubParams,
    Diff,
    Operation,
    CheckResult,
)
from .state import OptimizationState

__all__ = [
    "GitHubProfile",
    "GitHubRepository",
    "GitHubParams",
    "Diff",
    "Operation",
    "CheckResult",
    "OptimizationState",
]