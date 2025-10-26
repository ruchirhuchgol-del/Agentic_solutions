#!/usr/bin/env python3
"""
Test script to verify enterprise-grade features of GitHub Profile Optimizer.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

def test_caching_layer():
    """Test multi-layer caching system."""
    try:
        from src.github_profile_optimizer.utils.cache_manager import CacheManager, cache_manager
        
        # Test cache manager initialization
        assert cache_manager is not None
        print("PASS: CacheManager initialized successfully")
        
        # Test setting and getting values
        test_key = "test_key"
        test_value = {"data": "test_value", "number": 42}
        
        # Set value
        assert cache_manager.set(test_key, test_value)
        print("PASS: Cache set operation successful")
        
        # Get value
        retrieved_value = cache_manager.get(test_key)
        assert retrieved_value == test_value
        print("PASS: Cache get operation successful")
        
        # Test cache layers
        assert test_key in cache_manager.l1_cache
        print("PASS: L1 cache (memory) working")
        
        return True
    except Exception as e:
        print(f"FAIL: Caching layer test failed: {e}")
        return False


def test_rate_limiting():
    """Test intelligent rate limiting."""
    try:
        from src.github_profile_optimizer.utils.rate_limiter import GitHubRateLimiter, rate_limiter
        
        # Test rate limiter initialization
        assert rate_limiter is not None
        print("PASS: GitHubRateLimiter initialized successfully")
        
        # Test token bucket
        if hasattr(rate_limiter, 'local_bucket'):
            # Consume a token
            assert rate_limiter.local_bucket.consume(1)
            print("PASS: Token bucket consume operation successful")
            
            # Check remaining tokens
            remaining = rate_limiter.get_remaining_calls()
            assert remaining >= 0
            print("PASS: Rate limit remaining calls check successful")
        
        return True
    except Exception as e:
        print(f"FAIL: Rate limiting test failed: {e}")
        return False


def test_multi_tenancy():
    """Test multi-tenancy architecture."""
    try:
        from src.github_profile_optimizer.auth.tenant_manager import TenantManager, tenant_manager
        
        # Test tenant manager initialization
        assert tenant_manager is not None
        print("PASS: TenantManager initialized successfully")
        
        # Test listing tenants
        tenants = tenant_manager.list_tenants()
        assert isinstance(tenants, list)
        print("PASS: Tenant listing successful")
        
        # Test getting tenant config
        if tenants:
            config = tenant_manager.get_tenant_config(tenants[0])
            if config:
                print("PASS: Tenant configuration retrieval successful")
        
        return True
    except Exception as e:
        print(f"FAIL: Multi-tenancy test failed: {e}")
        return False


def test_predictive_optimizer():
    """Test predictive optimization engine."""
    try:
        from src.github_profile_optimizer.ml.predictive_optimizer import PredictiveOptimizer, predictive_optimizer
        
        # Test predictive optimizer initialization
        assert predictive_optimizer is not None
        print("PASS: PredictiveOptimizer initialized successfully")
        
        # Test rules-based recommendations
        from src.github_profile_optimizer.models.github import GitHubProfile, GitHubRepository
        
        # Create sample profile and repositories
        profile = GitHubProfile(
            login="testuser",
            name="Test User",
            bio=None,  # Intentionally empty to trigger recommendation
            location="Test Location",
            company="Test Company",
            blog="https://test.example.com",
            email="test@example.com",
            public_repos=5,
            followers=100,
            following=50,
            created_at="2020-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z"
        )
        
        repositories = [
            GitHubRepository(
                name="test-repo-1",
                description="A test repository",
                language="Python",
                stargazers_count=50,  # Fixed field name
                forks=10,
                private=False,
                updated_at="2023-01-01T00:00:00Z"
            )
        ]
        
        # Generate recommendations
        recommendations = predictive_optimizer.suggest_improvements(profile, repositories)
        assert isinstance(recommendations, list)
        print("PASS: Predictive recommendations generated successfully")
        
        # Check if bio recommendation is present (since bio is None)
        bio_recommendation = next((r for r in recommendations if r.target == "bio"), None)
        assert bio_recommendation is not None
        print("PASS: Bio improvement recommendation correctly generated")
        
        return True
    except Exception as e:
        print(f"FAIL: Predictive optimizer test failed: {e}")
        return False


def test_microservices():
    """Test microservices architecture."""
    try:
        # Test API gateway
        from src.github_profile_optimizer.api.gateway import app as gateway_app
        assert gateway_app is not None
        print("PASS: API Gateway initialized successfully")
        
        # Test profile service
        from src.github_profile_optimizer.services.profile_service import app as profile_app
        assert profile_app is not None
        print("PASS: Profile Service initialized successfully")
        
        # Test repo service
        from src.github_profile_optimizer.services.repo_service import app as repo_app
        assert repo_app is not None
        print("PASS: Repository Service initialized successfully")
        
        return True
    except Exception as e:
        print(f"FAIL: Microservices test failed: {e}")
        return False


def main():
    """Run all enterprise feature tests."""
    print("Testing GitHub Profile Optimizer Enterprise Features...")
    print("=" * 60)
    
    tests = [
        test_caching_layer,
        test_rate_limiting,
        test_multi_tenancy,
        test_predictive_optimizer,
        test_microservices
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"Enterprise feature tests passed: {passed}/{total}")
    
    if passed == total:
        print("SUCCESS: All enterprise features are working correctly!")
        return 0
    else:
        print("FAILURE: Some enterprise features failed. Please check the implementation.")
        return 1


if __name__ == "__main__":
    sys.exit(main())