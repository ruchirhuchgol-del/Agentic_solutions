"""
API module for GitHub Profile Optimizer.

Contains Flask applications for the API gateway and microservices.
"""

from .gateway import app as gateway_app

__all__ = [
    "gateway_app",
]