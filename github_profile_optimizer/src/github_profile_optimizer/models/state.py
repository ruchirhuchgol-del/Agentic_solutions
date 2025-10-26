"""
State management models.

Provides data models for state management and persistence.
"""

from typing import List, Dict, Any
from pydantic import BaseModel
from dataclasses import dataclass
from src.github_profile_optimizer.models.github import Diff


@dataclass
class OptimizationState:
    """
    State for optimization tasks.
    
    Contains the complete state information for an optimization task
    including diffs, safety checks, and execution context.
    """
    task_id: str
    dry_run: bool
    current_diffs: List[Diff]
    safety_checks: Dict[str, bool]