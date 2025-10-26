"""
Agents module for GitHub Profile Optimizer.

Contains implementations of various AI agents for GitHub profile analysis and optimization.
"""

from .base_agent import BaseAgent
from .github_automation import GitHubAutomationAgent

__all__ = [
    "BaseAgent",
    "GitHubAutomationAgent",
]