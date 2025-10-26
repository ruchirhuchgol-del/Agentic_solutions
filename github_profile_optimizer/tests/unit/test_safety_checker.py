"""Unit tests for the safety checker."""
import pytest
from src.github_profile_optimizer.services.safety_checker import SafetyChecker


def test_safety_checker_initialization():
    """Test safety checker initialization."""
    checker = SafetyChecker()
    assert isinstance(checker, SafetyChecker)


def test_validate_profile_update_valid():
    """Test validation of valid profile updates."""
    checker = SafetyChecker()
    updates = {
        "bio": "A short bio",
        "blog": "https://example.com",
        "email": "test@example.com",
        "company": "Test Company"
    }
    
    result = checker.validate_profile_update(updates)
    assert result["valid"] is True
    assert len(result["issues"]) == 0


def test_validate_profile_update_invalid():
    """Test validation of invalid profile updates."""
    checker = SafetyChecker()
    updates = {
        "bio": "A" * 200,  # Too long
        "blog": "invalid-url",  # Invalid URL
        "email": "invalid-email",  # Invalid email
        "company": "A" * 150  # Too long
    }
    
    result = checker.validate_profile_update(updates)
    assert result["valid"] is False
    assert len(result["issues"]) == 4


def test_validate_repository_changes_valid():
    """Test validation of valid repository changes."""
    checker = SafetyChecker()
    changes = [
        {
            "description": "A valid description",
            "topics": ["python", "ai", "automation"]
        }
    ]
    
    result = checker.validate_repository_changes(changes)
    assert result["valid"] is True
    assert len(result["issues"]) == 0


def test_validate_repository_changes_invalid():
    """Test validation of invalid repository changes."""
    checker = SafetyChecker()
    changes = [
        {
            "description": "A" * 2500,  # Too long
            "topics": ["topic" + str(i) for i in range(25)]  # Too many topics
        }
    ]
    
    result = checker.validate_repository_changes(changes)
    assert result["valid"] is False
    assert len(result["issues"]) == 2


def test_sanitize_input():
    """Test input sanitization."""
    checker = SafetyChecker()
    data = {
        "name": "John <script>alert('xss')</script> Doe",
        "email": "test@example.com",
        "age": 30
    }
    
    sanitized = checker.sanitize_input(data)
    assert "<script>" not in sanitized["name"]
    assert "alert('xss')" not in sanitized["name"]
    assert sanitized["email"] == "test@example.com"
    assert sanitized["age"] == 30