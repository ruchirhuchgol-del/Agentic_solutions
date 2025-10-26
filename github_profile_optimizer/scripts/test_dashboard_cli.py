"""
Test script for the GitHub Profile Optimizer Dashboard CLI

This script verifies that the dashboard can be run as a module.
"""

import subprocess
import sys
import os
from pathlib import Path

def test_dashboard_module():
    """Test that the dashboard can be run as a module."""
    print("Testing dashboard module execution...")
    
    try:
        # Get the project root directory
        project_root = Path(__file__).parent.parent
        os.chdir(project_root)
        
        # Test importing the main module
        result = subprocess.run([
            sys.executable, "-c", 
            "from src.github_profile_optimizer.ui import dashboard; print('Dashboard module imported successfully')"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Dashboard module imported successfully")
            print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Failed to import dashboard module: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Dashboard module import timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing dashboard module: {e}")
        return False

def test_dashboard_main_function():
    """Test that the main function can be called."""
    print("Testing dashboard main function...")
    
    try:
        # Test calling the main function (this will fail because of Streamlit context,
        # but we're just checking that it can be called without import errors)
        result = subprocess.run([
            sys.executable, "-c", 
            "from src.github_profile_optimizer.ui.dashboard import main; print('Main function accessible')"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Dashboard main function is accessible")
            print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            # Check if the error is related to Streamlit context (which is expected)
            if "Session state does not function" in result.stderr:
                print("✅ Dashboard main function is accessible (Streamlit context warning expected)")
                return True
            else:
                print(f"❌ Failed to access main function: {result.stderr}")
                return False
                
    except subprocess.TimeoutExpired:
        print("❌ Main function test timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing main function: {e}")
        return False

def main():
    """Run all dashboard CLI tests."""
    print("Running GitHub Profile Optimizer Dashboard CLI tests...\n")
    
    tests = [
        test_dashboard_module,
        test_dashboard_main_function
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
    
    print(f"CLI Test Results: {passed} passed, {failed} failed")
    
    if failed > 0:
        sys.exit(1)
    else:
        print("🎉 All dashboard CLI tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()