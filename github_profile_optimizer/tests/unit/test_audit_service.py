"""Unit tests for the audit service."""
import pytest
from src.github_profile_optimizer.services.audit_service import AuditService


def test_audit_service_initialization():
    """Test audit service initialization."""
    service = AuditService()
    assert isinstance(service, AuditService)


def test_analyze_profile_completeness():
    """Test profile completeness analysis."""
    service = AuditService()
    
    # Complete profile
    complete_profile = {
        "avatar_url": "https://example.com/avatar.jpg",
        "bio": "A complete bio",
        "location": "San Francisco, CA",
        "blog": "https://example.com",
        "email": "test@example.com",
        "company": "Test Company"
    }
    
    result = service.analyze_profile_completeness(complete_profile)
    assert result["completeness_score"] == 6
    assert result["total_checks"] == 6
    assert result["completeness_percentage"] == 100.0
    assert len(result["missing_fields"]) == 0
    
    # Incomplete profile
    incomplete_profile = {
        "bio": "A short bio",
        "location": "San Francisco, CA"
    }
    
    result = service.analyze_profile_completeness(incomplete_profile)
    assert result["completeness_score"] == 2
    assert result["total_checks"] == 6
    assert result["completeness_percentage"] == pytest.approx(33.33, 0.01)
    assert len(result["missing_fields"]) == 4


def test_analyze_repository_quality():
    """Test repository quality analysis."""
    service = AuditService()
    
    # Empty repositories list
    result = service.analyze_repository_quality([])
    assert result["repository_count"] == 0
    assert result["total_stars"] == 0
    assert result["average_stars"] == 0
    
    # Repositories with various qualities
    repositories = [
        {
            "name": "repo1",
            "stars": 10,
            "description": "A well-described repository"
        },
        {
            "name": "repo2",
            "stars": 3,
            "description": "Another good repo"
        },
        {
            "name": "repo3",
            "stars": 0,
            "description": None  # No description
        }
    ]
    
    result = service.analyze_repository_quality(repositories)
    assert result["repository_count"] == 3
    assert result["total_stars"] == 13
    assert result["average_stars"] == pytest.approx(4.33, 0.01)
    assert result["well_starred_count"] == 1  # Only repo1 has > 5 stars
    assert result["well_described_count"] == 2  # repo1 and repo2 have descriptions


def test_generate_audit_report():
    """Test audit report generation."""
    service = AuditService()
    
    profile = {
        "avatar_url": "https://example.com/avatar.jpg",
        "bio": "A complete bio",
        "location": "San Francisco, CA",
        "blog": "https://example.com",
        "email": "test@example.com",
        "company": "Test Company"
    }
    
    repositories = [
        {
            "name": "repo1",
            "stars": 10,
            "description": "A well-described repository"
        }
    ]
    
    report = service.generate_audit_report(profile, repositories)
    
    assert "profile_analysis" in report
    assert "repository_analysis" in report
    assert "overall_score" in report
    assert "recommendations" in report
    
    # Check overall score calculation
    assert 0 <= report["overall_score"] <= 100