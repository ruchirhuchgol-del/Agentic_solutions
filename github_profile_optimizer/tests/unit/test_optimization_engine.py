"""Unit tests for the optimization engine."""
import pytest
from src.github_profile_optimizer.services.optimization_engine import OptimizationEngine


def test_optimization_engine_initialization():
    """Test optimization engine initialization."""
    engine = OptimizationEngine()
    assert isinstance(engine, OptimizationEngine)


def test_generate_profile_recommendations():
    """Test generation of profile recommendations."""
    engine = OptimizationEngine()
    
    # Audit report with missing profile fields
    audit_report = {
        "profile_analysis": {
            "missing_fields": ["bio", "profile picture", "location"]
        },
        "repository_analysis": {
            "repository_count": 5,
            "well_described_count": 3,
            "well_starred_count": 0
        }
    }
    
    recommendations = engine.generate_profile_recommendations(audit_report)
    
    # Check that we have recommendations
    assert len(recommendations) > 0
    
    # Check for specific recommendations
    bio_rec = next((r for r in recommendations if r["title"] == "Add a professional bio"), None)
    assert bio_rec is not None
    assert bio_rec["type"] == "profile"
    assert bio_rec["priority"] == "high"
    
    repo_desc_rec = next((r for r in recommendations if r["title"] == "Improve repository descriptions"), None)
    assert repo_desc_rec is not None
    assert repo_desc_rec["type"] == "repositories"
    assert repo_desc_rec["priority"] == "high"


def test_prioritize_recommendations():
    """Test recommendation prioritization."""
    engine = OptimizationEngine()
    
    recommendations = [
        {"title": "Low priority", "priority": "low"},
        {"title": "High priority", "priority": "high"},
        {"title": "Medium priority", "priority": "medium"},
        {"title": "No priority"},  # No priority field
        {"title": "Another high", "priority": "high"}
    ]
    
    prioritized = engine.prioritize_recommendations(recommendations)
    
    # Check that high priority items come first
    assert prioritized[0]["title"] == "High priority"
    assert prioritized[1]["title"] == "Another high"
    
    # Check that low priority items come last
    assert prioritized[-1]["title"] == "Low priority"


def test_generate_action_plan():
    """Test action plan generation."""
    engine = OptimizationEngine()
    
    recommendations = [
        {"title": "High priority 1", "priority": "high"},
        {"title": "High priority 2", "priority": "high"},
        {"title": "Medium priority", "priority": "medium"},
        {"title": "Low priority", "priority": "low"}
    ]
    
    action_plan = engine.generate_action_plan(recommendations)
    
    # Check that recommendations are properly categorized
    assert len(action_plan["immediate_actions"]) == 2
    assert len(action_plan["short_term_actions"]) == 1
    assert len(action_plan["long_term_actions"]) == 1
    
    # Check that all high priority items are in immediate actions
    immediate_titles = [r["title"] for r in action_plan["immediate_actions"]]
    assert "High priority 1" in immediate_titles
    assert "High priority 2" in immediate_titles


def test_estimate_timeline():
    """Test timeline estimation."""
    engine = OptimizationEngine()
    
    # Test with high priority items
    recommendations = [
        {"title": "High priority", "priority": "high"},
        {"title": "Medium priority", "priority": "medium"}
    ]
    
    timeline = engine._estimate_timeline(recommendations)
    assert "1-2 weeks for immediate actions" in timeline
    
    # Test with only medium priority items
    recommendations = [
        {"title": "Medium priority", "priority": "medium"}
    ]
    
    timeline = engine._estimate_timeline(recommendations)
    assert "2-4 weeks for all improvements" in timeline
    
    # Test with only low priority items
    recommendations = [
        {"title": "Low priority", "priority": "low"}
    ]
    
    timeline = engine._estimate_timeline(recommendations)
    assert "1-2 weeks for all improvements" in timeline