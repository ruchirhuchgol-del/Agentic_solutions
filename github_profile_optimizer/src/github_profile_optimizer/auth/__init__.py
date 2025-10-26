"""
Authentication and authorization module for GitHub Profile Optimizer.

Contains multi-tenancy management and authentication utilities.
"""

from .tenant_manager import TenantManager, tenant_manager

__all__ = [
    "TenantManager",
    "tenant_manager",
]