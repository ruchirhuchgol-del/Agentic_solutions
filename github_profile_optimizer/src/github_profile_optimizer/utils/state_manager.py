"""
Redis-backed state tracking.

Provides state management capabilities with Redis backend and in-memory fallback.
"""

from typing import Any, Dict, Optional, List
import json
import os
import redis
from ..models.state import OptimizationState
from ..models.github import Diff
from ..utils.logger import get_logger


class RedisStateManager:
    """
    Manager for tracking application state with Redis.
    
    Provides persistent state management with Redis backend
    and in-memory fallback for reliability.
    """
    
    def __init__(self, redis_url: Optional[str] = None):
        """
        Initialize the Redis state manager.
        
        Args:
            redis_url: Redis connection URL
        """
        self.redis_url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379")
        self.logger = get_logger(self.__class__.__name__)
        
        try:
            self.redis = redis.Redis.from_url(self.redis_url)
            # Test connection
            self.redis.ping()
            self.logger.info("Connected to Redis successfully")
        except Exception as e:
            self.logger.warning(f"Could not connect to Redis: {e}. Using in-memory fallback.")
            self.redis = None
            self._state = {}  # Fallback to in-memory storage
    
    def save_state(self, state: OptimizationState) -> bool:
        """
        Save optimization state.
        
        Args:
            state: Optimization state to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            key = f"state:{state.task_id}"
            data = {
                "task_id": state.task_id,
                "dry_run": state.dry_run,
                "current_diffs": [diff.dict() for diff in state.current_diffs],
                "safety_checks": state.safety_checks
            }
            
            if self.redis:
                self.redis.set(key, json.dumps(data))
            else:
                self._state[key] = json.dumps(data)
                
            self.logger.debug(f"Saved state for task {state.task_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving state: {e}")
            return False
    
    def get_state(self, task_id: str) -> Optional[OptimizationState]:
        """
        Get optimization state by task ID.
        
        Args:
            task_id: Task ID
            
        Returns:
            Optimization state or None if not found
        """
        try:
            key = f"state:{task_id}"
            data = None
            
            if self.redis:
                data = self.redis.get(key)
            else:
                data = self._state.get(key)
                
            if data:
                state_data = json.loads(data)
                diffs = [Diff(**diff_data) for diff_data in state_data.get("current_diffs", [])]
                
                return OptimizationState(
                    task_id=state_data["task_id"],
                    dry_run=state_data["dry_run"],
                    current_diffs=diffs,
                    safety_checks=state_data["safety_checks"]
                )
                
            return None
        except Exception as e:
            self.logger.error(f"Error retrieving state: {e}")
            return None
    
    def create_state(self, task_id: str, dry_run: bool = True) -> OptimizationState:
        """
        Create a new optimization state.
        
        Args:
            task_id: Task ID
            dry_run: Whether running in dry-run mode
            
        Returns:
            New optimization state
        """
        state = OptimizationState(
            task_id=task_id,
            dry_run=dry_run,
            current_diffs=[],
            safety_checks={}
        )
        
        self.save_state(state)
        return state
    
    def update_diffs(self, task_id: str, diffs: List[Diff]) -> bool:
        """
        Update diffs in the state.
        
        Args:
            task_id: Task ID
            diffs: List of diffs to update
            
        Returns:
            True if successful, False otherwise
        """
        state = self.get_state(task_id)
        if not state:
            self.logger.error(f"State not found for task {task_id}")
            return False
            
        state.current_diffs = diffs
        return self.save_state(state)
    
    def update_safety_check(self, task_id: str, check_name: str, passed: bool) -> bool:
        """
        Update a safety check result.
        
        Args:
            task_id: Task ID
            check_name: Name of the safety check
            passed: Whether the check passed
            
        Returns:
            True if successful, False otherwise
        """
        state = self.get_state(task_id)
        if not state:
            self.logger.error(f"State not found for task {task_id}")
            return False
            
        state.safety_checks[check_name] = passed
        return self.save_state(state)