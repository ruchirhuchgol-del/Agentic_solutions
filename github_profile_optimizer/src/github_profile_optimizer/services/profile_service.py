"""Profile Service for GitHub Profile Optimizer."""
from flask import Flask, request, jsonify
import os
from ..models.github import GitHubProfile, GitHubRepository
from ..auth.tenant_manager import tenant_manager
from ..utils.cache_manager import cache_manager
from ..utils.rate_limiter import rate_limiter, RateLimitExceeded
from ..services.audit_service import AuditService
from ..ml.predictive_optimizer import predictive_optimizer
from ..utils.logger import get_logger


app = Flask(__name__)
logger = get_logger("profile_service")


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "profile-service"
    }), 200


@app.route("/profile/<tenant_id>/<github_handle>", methods=["GET"])
def get_profile(tenant_id: str, github_handle: str):
    """Get GitHub profile for a tenant."""
    try:
        # Validate tenant
        tenant_config = tenant_manager.get_tenant_config(tenant_id)
        if not tenant_config:
            return jsonify({"error": "Tenant not found"}), 404
        
        # Check cache first
        cache_key = f"profile_{tenant_id}_{github_handle}"
        cached_profile = cache_manager.get(cache_key)
        if cached_profile:
            logger.info(f"Cache hit for profile {github_handle}")
            return jsonify(cached_profile), 200
        
        # Get GitHub client for tenant
        github_client = tenant_manager.get_client(tenant_id)
        if not github_client:
            return jsonify({"error": "Could not initialize GitHub client"}), 500
        
        # In a real implementation, we would fetch the profile data from GitHub
        # For now, we'll return mock data
        profile_data = {
            "login": github_handle,
            "name": "Test User",
            "bio": "A passionate developer",
            "location": "San Francisco, CA",
            "company": "Tech Corp",
            "blog": "https://testuser.dev",
            "email": "test@example.com",
            "public_repos": 15,
            "followers": 100,
            "following": 50,
            "created_at": "2020-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z",
            "avatar_url": "https://avatars.githubusercontent.com/u/123456"
        }
        
        # Cache the result
        cache_manager.set(cache_key, profile_data)
        
        return jsonify(profile_data), 200
        
    except RateLimitExceeded:
        return jsonify({"error": "GitHub API rate limit exceeded"}), 429
    except Exception as e:
        logger.error(f"Error in get_profile: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/profile/<tenant_id>/<github_handle>/repos", methods=["GET"])
def get_repositories(tenant_id: str, github_handle: str):
    """Get GitHub repositories for a tenant."""
    try:
        # Validate tenant
        tenant_config = tenant_manager.get_tenant_config(tenant_id)
        if not tenant_config:
            return jsonify({"error": "Tenant not found"}), 404
        
        # Check cache first
        cache_key = f"repos_{tenant_id}_{github_handle}"
        cached_repos = cache_manager.get(cache_key)
        if cached_repos:
            logger.info(f"Cache hit for repositories of {github_handle}")
            return jsonify(cached_repos), 200
        
        # In a real implementation, we would fetch the repositories from GitHub
        # For now, we'll return mock data
        repos_data = [
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
                "private": True,
                "updated_at": "2023-01-01T00:00:00Z"
            }
        ]
        
        # Cache the result
        cache_manager.set(cache_key, repos_data)
        
        return jsonify(repos_data), 200
        
    except RateLimitExceeded:
        return jsonify({"error": "GitHub API rate limit exceeded"}), 429
    except Exception as e:
        logger.error(f"Error in get_repositories: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/profile/<tenant_id>/<github_handle>/analyze", methods=["POST"])
def analyze_profile(tenant_id: str, github_handle: str):
    """Analyze GitHub profile for a tenant."""
    try:
        # Validate tenant
        tenant_config = tenant_manager.get_tenant_config(tenant_id)
        if not tenant_config:
            return jsonify({"error": "Tenant not found"}), 404
        
        # Get profile and repositories
        profile_response = get_profile(tenant_id, github_handle)
        if profile_response[1] != 200:
            return profile_response
            
        repos_response = get_repositories(tenant_id, github_handle)
        if repos_response[1] != 200:
            return repos_response
        
        profile_data = profile_response[0].get_json()
        repos_data = repos_response[0].get_json()
        
        # Convert data to models
        profile = GitHubProfile(**profile_data)
        repositories = [GitHubRepository(**repo_data) for repo_data in repos_data]
        
        # Run audit
        audit_service = AuditService()
        audit_report = audit_service.generate_audit_report(profile.dict(), repos_data)
        
        # Generate predictions
        recommendations = predictive_optimizer.suggest_improvements(profile, repositories)
        
        result = {
            "profile": profile.dict(),
            "repositories": repos_data,
            "audit": audit_report,
            "recommendations": [rec.__dict__ for rec in recommendations]
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in analyze_profile: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)