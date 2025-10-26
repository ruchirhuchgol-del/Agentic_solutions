#!/usr/bin/env python3
"""
Test script to verify the installation of GitHub Profile Optimizer.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

def test_imports():
    """Test that all modules can be imported."""
    try:
        # Test core modules
        from src.github_profile_optimizer.crew import GithubProfileOptimizerCrew
        from src.github_profile_optimizer.agents.github_automation import GitHubAutomationAgent
        from src.github_profile_optimizer.tools.base_tool import BaseTool
        from src.github_profile_optimizer.tools.github_client import GitHubProfileTool
        from src.github_profile_optimizer.tools.file_operation_tool import FileOperationTool
        from src.github_profile_optimizer.services.audit_service import AuditService
        from src.github_profile_optimizer.services.optimization_engine import OptimizationEngine
        from src.github_profile_optimizer.services.safety_checker import SafetyChecker
        from src.github_profile_optimizer.utils.logger import get_logger
        from src.github_profile_optimizer.utils.state_manager import RedisStateManager
        from src.github_profile_optimizer.utils.validators import InputValidator
        from src.github_profile_optimizer.metrics import metrics_collector
        from src.github_profile_optimizer.health import HealthChecker
        from src.github_profile_optimizer.exceptions import GitHubProfileOptimizerError
        
        print("PASS: All modules imported successfully")
        return True
    except Exception as e:
        print(f"FAIL: Import failed: {e}")
        return False

def test_agent_creation():
    """Test that agents can be created."""
    try:
        from src.github_profile_optimizer.agents.github_automation import GitHubAutomationAgent
        agent = GitHubAutomationAgent()
        print("PASS: GitHubAutomationAgent created successfully")
        return True
    except Exception as e:
        print(f"FAIL: Agent creation failed: {e}")
        return False

def test_tool_creation():
    """Test that tools can be created."""
    try:
        from src.github_profile_optimizer.tools.github_client import GitHubProfileTool
        from src.github_profile_optimizer.tools.file_operation_tool import FileOperationTool
        
        github_tool = GitHubProfileTool()
        file_tool = FileOperationTool()
        
        print("PASS: Tools created successfully")
        return True
    except Exception as e:
        print(f"FAIL: Tool creation failed: {e}")
        return False

def test_service_creation():
    """Test that services can be created."""
    try:
        from src.github_profile_optimizer.services.audit_service import AuditService
        from src.github_profile_optimizer.services.optimization_engine import OptimizationEngine
        from src.github_profile_optimizer.services.safety_checker import SafetyChecker
        
        audit_service = AuditService()
        optimization_engine = OptimizationEngine()
        safety_checker = SafetyChecker()
        
        print("PASS: Services created successfully")
        return True
    except Exception as e:
        print(f"FAIL: Service creation failed: {e}")
        return False

def test_utilities():
    """Test that utilities work."""
    try:
        from src.github_profile_optimizer.utils.logger import get_logger
        from src.github_profile_optimizer.utils.validators import InputValidator
        
        logger = get_logger("test")
        validator = InputValidator()
        
        # Test validator
        assert validator.validate_github_username("testuser") == True
        assert validator.validate_github_username("invalid-user-") == False
        
        print("PASS: Utilities work correctly")
        return True
    except Exception as e:
        print(f"FAIL: Utilities test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing GitHub Profile Optimizer installation...")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_agent_creation,
        test_tool_creation,
        test_service_creation,
        test_utilities
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("SUCCESS: All tests passed! Installation is working correctly.")
        return 0
    else:
        print("FAILURE: Some tests failed. Please check the installation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())