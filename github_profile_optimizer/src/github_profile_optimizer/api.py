"""
API endpoints for the GitHub Profile Optimizer.

Provides RESTful API endpoints for profile optimization and analysis services.
"""

import json
from typing import Dict, Any
from flask import Flask, request, jsonify
from .crew import GithubProfileOptimizerCrew
from .health import health_check
from .config.settings import settings
from .utils.logger import get_logger


app = Flask(__name__)
logger = get_logger("api")


@app.route("/health", methods=["GET"])
def health_endpoint():
    """
    Health check endpoint.
    
    Returns:
        JSON response with health check results
    """
    try:
        health_data = health_check()
        return health_data, 200, {"Content-Type": "application/json"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({"error": "Health check failed", "details": str(e)}), 500


@app.route("/optimize", methods=["POST"])
def optimize_endpoint():
    """
    Optimize GitHub profile endpoint.
    
    Expects JSON payload with:
    - github_handle: GitHub username
    - target_roles: Target job roles
    - repos_scope: Repository scope
    - dry_run: Whether to run in dry-run mode
    - limits: Optimization limits
    
    Returns:
        JSON response with optimization results
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Required fields
        required_fields = ["github_handle"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400
        
        # Prepare inputs for the crew
        inputs = {
            "github_handle": data["github_handle"],
            "target_roles": data.get("target_roles", "Software Engineer"),
            "repos_scope": data.get("repos_scope", "public"),
            "dry_run": data.get("dry_run", True),
            "limits": data.get("limits", "minimal")
        }
        
        # Run the crew
        logger.info(f"Starting optimization for {data['github_handle']}")
        result = GithubProfileOptimizerCrew().crew().kickoff(inputs=inputs)
        
        # Return result
        return jsonify({
            "status": "success",
            "result": result
        }), 200
        
    except Exception as e:
        logger.error(f"Optimization failed: {e}")
        return jsonify({"error": "Optimization failed", "details": str(e)}), 500


@app.route("/analyze", methods=["POST"])
def analyze_endpoint():
    """
    Analyze GitHub profile endpoint.
    
    Expects JSON payload with:
    - github_handle: GitHub username
    
    Returns:
        JSON response with analysis results
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Required fields
        if "github_handle" not in data:
            return jsonify({"error": "Missing required field: github_handle"}), 400
        
        # Prepare inputs for analysis
        inputs = {
            "github_handle": data["github_handle"],
            "analysis_only": "true"
        }
        
        # Run the crew in analysis mode
        logger.info(f"Starting analysis for {data['github_handle']}")
        result = GithubProfileOptimizerCrew().crew().kickoff(inputs=inputs)
        
        # Return result
        return jsonify({
            "status": "success",
            "result": result
        }), 200
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return jsonify({"error": "Analysis failed", "details": str(e)}), 500


def create_app():
    """
    Create Flask app instance.
    
    Returns:
        Flask app instance
    """
    app.config["DEBUG"] = settings.debug
    return app


if __name__ == "__main__":
    # Run the app
    app.run(
        host=settings.api_host,
        port=settings.api_port,
        debug=settings.debug
    )