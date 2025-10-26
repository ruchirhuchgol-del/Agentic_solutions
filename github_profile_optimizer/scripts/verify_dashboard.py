"""
Verification script for the GitHub Profile Optimizer Dashboard

This script verifies that all dashboard components work correctly
without running the full Streamlit application.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all dashboard components can be imported."""
    print("Testing dashboard component imports...")
    
    try:
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

def test_models():
    """Test that data models work correctly."""
    print("Testing data models...")
    
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
    print("Testing enums...")
    
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

def test_config():
    """Test that configuration works correctly."""
    print("Testing configuration...")
    
    try:
        from src.github_profile_optimizer.ui.dashboard import Config
        
        # Test that config values are accessible
        assert hasattr(Config, 'API_BASE_URL')
        assert hasattr(Config, 'REQUEST_TIMEOUT')
        assert hasattr(Config, 'COLOR_PRIMARY')
        
        print("✅ Configuration works correctly")
        return True
    except Exception as e:
        print(f"❌ Error testing configuration: {e}")
        return False

def test_session_state():
    """Test that session state manager works correctly."""
    print("Testing session state manager...")
    
    try:
        from src.github_profile_optimizer.ui.dashboard import SessionStateManager, Config
        
        # Test initialization
        SessionStateManager.initialize()
        print("✅ Session state manager initialization works correctly")
        
        # Test getting tenant config
        config = SessionStateManager.get_tenant_config()
        assert isinstance(config, dict)
        print("✅ Session state manager get_tenant_config works correctly")
        
        # Test updating tenant config
        original_rate_limit = config.get("rate_limit", Config.DEFAULT_RATE_LIMIT)
        SessionStateManager.update_tenant_config({"rate_limit": 6000})
        updated_config = SessionStateManager.get_tenant_config()
        assert updated_config.get("rate_limit") == 6000
        print("✅ Session state manager update_tenant_config works correctly")
        
        # Restore original value
        SessionStateManager.update_tenant_config({"rate_limit": original_rate_limit})
        
        return True
    except Exception as e:
        print(f"❌ Error testing session state manager: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all dashboard verification tests."""
    print("Running GitHub Profile Optimizer Dashboard verification...\n")
    
    tests = [
        test_imports,
        test_models,
        test_enums,
        test_config,
        test_session_state
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
    
    print(f"Verification Results: {passed} passed, {failed} failed")
    
    if failed > 0:
        sys.exit(1)
    else:
        print("🎉 All dashboard verification tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()