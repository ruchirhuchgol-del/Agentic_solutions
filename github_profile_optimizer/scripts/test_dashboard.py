
"""
Test script for the GitHub Profile Optimizer Dashboard

This script verifies that the dashboard components can be imported
and initialized correctly.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_dashboard_imports():
    """Test that dashboard components can be imported."""
    try:
        # Test importing the main dashboard module
        from src.github_profile_optimizer.ui.dashboard import (
            Config,
            RepoScope,
            OptimizationDepth,
            ProfessionalRole,
            TenantConfiguration,
            OptimizationRequest,
            OptimizationResult,
            SessionStateManager,
            APIClient,
            DashboardUI,
            ResultsDisplay,
            validate_inputs,
            main
        )
        print("✅ All dashboard components imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import dashboard components: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during import: {e}")
        return False

def test_data_models():
    """Test that data models work correctly."""
    try:
        from src.github_profile_optimizer.ui.dashboard import (
            TenantConfiguration,
            OptimizationRequest,
            ProfessionalRole,
            RepoScope,
            OptimizationDepth
        )
        
        # Test TenantConfiguration
        tenant_config = TenantConfiguration(
            tenant_id="test-tenant",
            github_token="test-token",
            openai_key="test-key",
            rate_limit=5000,
            allowed_roles=[role.value for role in ProfessionalRole]
        )
        print("✅ TenantConfiguration model works correctly")
        
        # Test OptimizationRequest
        opt_request = OptimizationRequest(
            github_handle="test-user",
            target_roles=["Software Engineer"],
            repos_scope=RepoScope.PUBLIC.value,
            dry_run=True,
            limits=OptimizationDepth.MODERATE.value,
            tenant_id="test-tenant"
        )
        print("✅ OptimizationRequest model works correctly")
        
        return True
    except Exception as e:
        print(f"❌ Error testing data models: {e}")
        return False

def test_enums():
    """Test that enums work correctly."""
    try:
        from src.github_profile_optimizer.ui.dashboard import (
            RepoScope,
            OptimizationDepth,
            ProfessionalRole
        )
        
        # Test enum values
        assert RepoScope.PUBLIC.value == "public"
        assert OptimizationDepth.COMPREHENSIVE.value == "comprehensive"
        assert ProfessionalRole.SOFTWARE_ENGINEER.value == "Software Engineer"
        
        print("✅ All enums work correctly")
        return True
    except Exception as e:
        print(f"❌ Error testing enums: {e}")
        return False

def main():
    """Run all dashboard tests."""
    print("Running GitHub Profile Optimizer Dashboard tests...\n")
    
    tests = [
        test_dashboard_imports,
        test_data_models,
        test_enums
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            failed += 1
        print()  # Add spacing between tests
    
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed > 0:
        sys.exit(1)
    else:
        print("🎉 All dashboard tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()