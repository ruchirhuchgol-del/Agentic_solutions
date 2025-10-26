"""DevSecOps Deployment Gatekeeper - Automated Security Checks for CI/CD."""

__version__ = "0.1.0"

from .core.crew import DevopsDeploymentSecurityGateCrew

__all__ = ["DevopsDeploymentSecurityGateCrew"]