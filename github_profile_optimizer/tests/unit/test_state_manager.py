"""Unit tests for the state manager."""
import pytest
import json
from src.github_profile_optimizer.utils.state_manager import RedisStateManager
from src.github_profile_optimizer.models.github import Diff


def test_state_manager_initialization():
    """Test state manager initialization."""
    # Test with default Redis URL
    manager = RedisStateManager()
    assert manager.redis_url == "redis://localhost:6379"
    
    # Test with custom Redis URL
    custom_url = "redis://custom:6379"
    manager = RedisStateManager(redis_url=custom_url)
    assert manager.redis_url == custom_url


def test_state_operations():
    """Test state set and get operations."""
    manager = RedisStateManager()
    
    # Test with in-memory fallback since we may not have Redis in test environment
    task_id = "test_task_123"
    test_data = {
        "task_id": task_id,
        "dry_run": True,
        "current_diffs": [],
        "safety_checks": {"preflight": True}
    }
    
    # Test setting state
    result = manager.save_state(test_data)
    assert result is True
    
    # Test getting state
    retrieved_state = manager.get_state(task_id)
    assert retrieved_state is not None
    assert retrieved_state["task_id"] == task_id
    assert retrieved_state["dry_run"] is True
    assert retrieved_state["safety_checks"]["preflight"] is True


def test_state_manager_create_state():
    """Test creating a new state."""
    manager = RedisStateManager()
    
    task_id = "new_task_456"
    state = manager.create_state(task_id, dry_run=False)
    
    assert state["task_id"] == task_id
    assert state["dry_run"] is False
    assert state["current_diffs"] == []
    assert state["safety_checks"] == {}


def test_state_manager_update_operations():
    """Test state update operations."""
    manager = RedisStateManager()
    
    task_id = "update_task_789"
    manager.create_state(task_id, dry_run=True)
    
    # Test updating diffs
    diffs = [
        Diff(
            path="test.md",
            original="# Original",
            proposed="# Updated",
            metadata={"tool": "test_tool"}
        )
    ]
    
    result = manager.update_diffs(task_id, diffs)
    assert result is True
    
    # Test updating safety check
    result = manager.update_safety_check(task_id, "ownership", True)
    assert result is True
    
    # Verify updates
    state = manager.get_state(task_id)
    assert len(state["current_diffs"]) == 1
    assert state["safety_checks"]["ownership"] is True


def test_state_manager_delete_and_exists():
    """Test state deletion and existence checking."""
    manager = RedisStateManager()
    
    task_id = "delete_test_task"
    manager.create_state(task_id)
    
    # Test existence
    # Note: The current implementation doesn't have an exists method
    # but we can test through get operations
    state = manager.get_state(task_id)
    assert state is not None
    
    # The current implementation doesn't have a delete method
    # but we can test that non-existent tasks return None
    non_existent_state = manager.get_state("non_existent_task")
    assert non_existent_state is None


def test_state_manager_increment():
    """Test increment operation."""
    manager = RedisStateManager()
    
    key = "test_counter"
    
    # Test initial increment
    result = manager.increment(key)
    assert result == 1
    
    # Test subsequent increments
    result = manager.increment(key, 5)
    assert result == 6
    
    # Test negative increment
    result = manager.increment(key, -2)
    assert result == 4


def test_state_manager_get_all():
    """Test getting all state data."""
    manager = RedisStateManager()
    
    # Set some test data
    manager.set("key1", "value1")
    manager.set("key2", {"nested": "value"})
    
    # Get all data
    all_data = manager.get_all()
    
    assert "key1" in all_data
    assert "key2" in all_data
    assert all_data["key1"] == "value1"
    assert all_data["key2"]["nested"] == "value"