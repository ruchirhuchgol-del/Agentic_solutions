"""Repository Service for GitHub Profile Optimizer."""
from flask import Flask, request, jsonify
import os
from ..models.github import GitHubRepository
from ..auth.tenant_manager import tenant_manager
from ..utils.cache_manager import cache_manager
from ..utils.rate_limiter import rate_limiter, RateLimitExceeded
from ..utils.logger import get_logger


app = Flask(__name__)
logger = get_logger("repo_service")


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "repo-service"
    }), 200


@app.route("/repo/<tenant_id>/<github_handle>/<repo_name>", methods=["GET"])
def get_repository(tenant_id: str, github_handle: str, repo_name: str):
    """Get specific GitHub repository for a tenant."""
    try:
        # Validate tenant
        tenant_config = tenant_manager.get_tenant_config(tenant_id)
        if not tenant_config:
            return jsonify({"error": "Tenant not found"}), 404
        
        # Check if repo is allowed for this tenant
        if not tenant_manager.is_repo_allowed(tenant_id, repo_name):
            return jsonify({"error": "Repository not allowed for this tenant"}), 403
        
        # Check cache first
        cache_key = f"repo_{tenant_id}_{github_handle}_{repo_name}"
        cached_repo = cache_manager.get(cache_key)
        if cached_repo:
            logger.info(f"Cache hit for repository {repo_name}")
            return jsonify(cached_repo), 200
        
        # Get GitHub client for tenant
        github_client = tenant_manager.get_client(tenant_id)
        if not github_client:
            return jsonify({"error": "Could not initialize GitHub client"}), 500
        
        # In a real implementation, we would fetch the specific repository
        # For now, we'll return a mock response
        repo_data = {
            "name": repo_name,
            "description": "Sample repository description",
            "language": "Python",
            "stars": 100,
            "forks": 25,
            "private": False,
            "updated_at": "2023-01-01T00:00:00Z"
        }
        
        # Cache the result
        cache_manager.set(cache_key, repo_data)
        
        return jsonify(repo_data), 200
        
    except RateLimitExceeded:
        return jsonify({"error": "GitHub API rate limit exceeded"}), 429
    except Exception as e:
        logger.error(f"Error in get_repository: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/repo/<tenant_id>/<github_handle>/<repo_name>/optimize", methods=["POST"])
def optimize_repository(tenant_id: str, github_handle: str, repo_name: str):
    """Optimize specific GitHub repository for a tenant."""
    try:
        # Validate tenant
        tenant_config = tenant_manager.get_tenant_config(tenant_id)
        if not tenant_config:
            return jsonify({"error": "Tenant not found"}), 404
        
        # Check if repo is allowed for this tenant
        if not tenant_manager.is_repo_allowed(tenant_id, repo_name):
            return jsonify({"error": "Repository not allowed for this tenant"}), 403
        
        # Get request data
        data = request.get_json()
        optimization_type = data.get("type", "readme")
        
        # Get GitHub client for tenant
        github_client = tenant_manager.get_client(tenant_id)
        if not github_client:
            return jsonify({"error": "Could not initialize GitHub client"}), 500
        
        # In a real implementation, we would perform the optimization
        # For now, we'll return a mock response
        return jsonify({
            "status": "success",
            "message": f"Optimization job started for {repo_name}",
            "job_id": f"optimize_{tenant_id}_{github_handle}_{repo_name}",
            "optimization_type": optimization_type
        }), 202
        
    except RateLimitExceeded:
        return jsonify({"error": "GitHub API rate limit exceeded"}), 429
    except Exception as e:
        logger.error(f"Error in optimize_repository: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=True)