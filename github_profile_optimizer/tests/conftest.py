"""pytest configuration and fixtures."""
import pytest
import os
import sys


# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


@pytest.fixture
def sample_github_profile():
    """Sample GitHub profile data for testing."""
    return {
        "login": "testuser",
        "name": "Test User",
        "bio": "A test user for GitHub Profile Optimizer",
        "location": "San Francisco, CA",
        "company": "Test Company",
        "blog": "https://testuser.example.com",
        "email": "test@testuser.example.com",
        "public_repos": 10,
        "followers": 100,
        "following": 50,
        "created_at": "2020-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z",
        "avatar_url": "https://avatars.githubusercontent.com/u/123456"
    }


@pytest.fixture
def sample_github_repositories():
    """Sample GitHub repositories data for testing."""
    return [
        {
            "name": "test-repo-1",
            "description": "A test repository",
            "language": "Python",
            "stars": 50,
            "forks": 10,
            "private": False,
            "updated_at": "2023-01-01T00:00:00Z"
        },
        {
            "name": "test-repo-2",
            "description": "Another test repository",
            "language": "JavaScript",
            "stars": 25,
            "forks": 5,
            "private": False,
            "updated_at": "2022-01-01T00:00:00Z"
        }
    ]


@pytest.fixture
def sample_audit_report():
    """Sample audit report for testing."""
    return {
        "profile_analysis": {
            "completeness_score": 6,
            "total_checks": 6,
            "completeness_percentage": 100.0,
            "missing_fields": []
        },
        "repository_analysis": {
            "repository_count": 2,
            "total_stars": 75,
            "average_stars": 37.5,
            "well_starred_count": 2,
            "well_described_count": 2
        },
        "overall_score": 95.0,
        "recommendations": []
    }