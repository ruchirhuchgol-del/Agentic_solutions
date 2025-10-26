"""
Health check endpoints for monitoring.

Provides comprehensive health checking capabilities for the application.
"""

import os
import json
from typing import Dict, Any
from datetime import datetime
from .utils.state_manager import RedisStateManager
from .metrics import metrics_collector
from .config.settings import settings


class HealthChecker:
    """
    Performs health checks for the application.
    
    This class provides methods for checking the health of various
    application components including Redis, GitHub API, and environment configuration.
    """
    
    def __init__(self):
        """Initialize the health checker."""
        self.state_manager = RedisStateManager()
    
    def check_health(self) -> Dict[str, Any]:
        """
        Perform comprehensive health check.
        
        Returns:
            Health check results
        """
        checks = {
            "timestamp": datetime.utcnow().isoformat(),
            "status": "healthy",
            "checks": {}
        }
        
        # Check Redis connection
        checks["checks"]["redis"] = self._check_redis()
        
        # Check GitHub token
        checks["checks"]["github_token"] = self._check_github_token()
        
        # Check environment variables
        checks["checks"]["environment"] = self._check_environment()
        
        # Check metrics
        checks["checks"]["metrics"] = self._check_metrics()
        
        # Determine overall status
        if any(check["status"] == "unhealthy" for check in checks["checks"].values()):
            checks["status"] = "unhealthy"
        
        return checks
    
    def _check_redis(self) -> Dict[str, Any]:
        """
        Check Redis connection.
        
        Returns:
            Redis health check results
        """
        try:
            # Try to ping Redis
            if hasattr(self.state_manager, 'redis') and self.state_manager.redis:
                self.state_manager.redis.ping()
                return {
                    "status": "healthy",
                    "details": {"connection": "successful"}
                }
            else:
                return {
                    "status": "degraded",
                    "details": {"connection": "using in-memory fallback"}
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "details": {"error": str(e)}
            }
    
    def _check_github_token(self) -> Dict[str, Any]:
        """
        Check GitHub token.
        
        Returns:
            GitHub token health check results
        """
        token = settings.github_token
        if not token:
            return {
                "status": "unhealthy",
                "details": {"error": "GITHUB_TOKEN environment variable not set"}
            }
        
        # Check token length (basic validation)
        if len(token) < 10:
            return {
                "status": "unhealthy",
                "details": {"error": "GitHub token appears invalid (too short)"}
            }
        
        return {
            "status": "healthy",
            "details": {"validation": "basic token format check passed"}
        }
    
    def _check_environment(self) -> Dict[str, Any]:
        """
        Check environment variables.
        
        Returns:
            Environment health check results
        """
        required_vars = ["GITHUB_TOKEN"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            return {
                "status": "unhealthy",
                "details": {"missing_variables": missing_vars}
            }
        
        return {
            "status": "healthy",
            "details": {"required_variables": "all present"}
        }
    
    def _check_metrics(self) -> Dict[str, Any]:
        """
        Check metrics collection.
        
        Returns:
            Metrics health check results
        """
        try:
            metrics = metrics_collector.get_metrics()
            return {
                "status": "healthy",
                "details": {"metrics_count": len(metrics)}
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "details": {"error": str(e)}
            }


def health_check() -> str:
    """
    Perform health check and return JSON response.
    
    Returns:
        JSON string with health check results
    """
    health_checker = HealthChecker()
    results = health_checker.check_health()
    return json.dumps(results, indent=2)