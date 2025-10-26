"""
Multi-tenancy management for enterprise GitHub Profile Optimizer.

Provides tenant isolation and management capabilities for enterprise deployments.
"""

import os
from typing import Dict, Any, Optional
from ..utils.logger import get_logger


class TenantConfig:
    """
    Configuration for a tenant.
    
    Contains all configuration parameters for a specific tenant
    in a multi-tenant deployment environment.
    """
    
    def __init__(self, tenant_id: str, config: Dict[str, Any]):
        """
        Initialize tenant configuration.
        
        Args:
            tenant_id: Unique identifier for the tenant
            config: Configuration dictionary
        """
        self.tenant_id = tenant_id
        self.github_token = config.get('github_token')
        self.rate_limit = config.get('rate_limit', 5000)
        self.allowed_roles = config.get('allowed_roles', [])
        self.whitelisted_repos = config.get('whitelisted_repos', [])
        self.blacklisted_repos = config.get('blacklisted_repos', [])


class TenantManager:
    """
    Manages tenant configurations and GitHub clients.
    
    Provides centralized management of tenant configurations,
    authentication credentials, and access control policies.
    """
    
    def __init__(self):
        """Initialize tenant manager."""
        self.logger = get_logger(self.__class__.__name__)
        self.tenant_configs: Dict[str, TenantConfig] = {}
        self._load_tenant_configs()
    
    def _load_tenant_configs(self) -> None:
        """Load tenant configurations from environment or config files."""
        # In a real implementation, this would load from a database or config files
        # For now, we'll load from environment variables
        
        # Example: TENANT_ACME_CORP_CONFIG={"github_token": "ghp_...", "rate_limit": 1000, "allowed_roles": ["Engineer", "Manager"]}
        for key, value in os.environ.items():
            if key.startswith('TENANT_') and key.endswith('_CONFIG'):
                try:
                    import json
                    tenant_id = key.replace('TENANT_', '').replace('_CONFIG', '').lower()
                    config = json.loads(value)
                    self.tenant_configs[tenant_id] = TenantConfig(tenant_id, config)
                    self.logger.info(f"Loaded configuration for tenant: {tenant_id}")
                except Exception as e:
                    self.logger.error(f"Error loading tenant config for {key}: {e}")
        
        # Add default tenant if none exist
        if not self.tenant_configs:
            default_config = {
                'github_token': os.getenv('GITHUB_TOKEN'),
                'rate_limit': 5000,
                'allowed_roles': ['*']  # Allow all roles
            }
            self.tenant_configs['default'] = TenantConfig('default', default_config)
            self.logger.info("Loaded default tenant configuration")
    
    def get_tenant_config(self, tenant_id: str) -> Optional[TenantConfig]:
        """
        Get configuration for a tenant.
        
        Args:
            tenant_id: Tenant identifier
            
        Returns:
            Tenant configuration or None if not found
        """
        return self.tenant_configs.get(tenant_id)
    
    def get_client(self, tenant_id: str) -> Optional[Any]:
        """
        Get GitHub client for a tenant.
        
        Args:
            tenant_id: Tenant identifier
            
        Returns:
            GitHub client configured for the tenant or None if tenant not found
        """
        config = self.get_tenant_config(tenant_id)
        if not config:
            self.logger.error(f"Tenant not found: {tenant_id}")
            return None
            
        if not config.github_token:
            self.logger.error(f"No GitHub token configured for tenant: {tenant_id}")
            return None
            
        try:
            # We can't import GitHubClient directly due to circular imports
            # In a real implementation, we would create the client here
            self.logger.info(f"Created GitHub client for tenant: {tenant_id}")
            return {"token": config.github_token}  # Placeholder
        except Exception as e:
            self.logger.error(f"Error creating GitHub client for tenant {tenant_id}: {e}")
            return None
    
    def is_repo_allowed(self, tenant_id: str, repo_name: str) -> bool:
        """
        Check if a repository is allowed for a tenant.
        
        Args:
            tenant_id: Tenant identifier
            repo_name: Repository name
            
        Returns:
            True if repository is allowed, False otherwise
        """
        config = self.get_tenant_config(tenant_id)
        if not config:
            return False
            
        # If whitelist exists, repo must be in it
        if config.whitelisted_repos:
            return repo_name in config.whitelisted_repos
            
        # If blacklist exists, repo must not be in it
        if config.blacklisted_repos:
            return repo_name not in config.blacklisted_repos
            
        # If no restrictions, allow all
        return True
    
    def list_tenants(self) -> list:
        """
        List all tenant IDs.
        
        Returns:
            List of tenant IDs
        """
        return list(self.tenant_configs.keys())
    
    def add_tenant(self, tenant_id: str, config: Dict[str, Any]) -> bool:
        """
        Add a new tenant.
        
        Args:
            tenant_id: Tenant identifier
            config: Tenant configuration
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.tenant_configs[tenant_id] = TenantConfig(tenant_id, config)
            self.logger.info(f"Added tenant: {tenant_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding tenant {tenant_id}: {e}")
            return False
    
    def remove_tenant(self, tenant_id: str) -> bool:
        """
        Remove a tenant.
        
        Args:
            tenant_id: Tenant identifier
            
        Returns:
            True if successful, False otherwise
        """
        if tenant_id in self.tenant_configs:
            del self.tenant_configs[tenant_id]
            self.logger.info(f"Removed tenant: {tenant_id}")
            return True
        return False


# Global tenant manager instance
tenant_manager = TenantManager()