"""
Test script to verify the restructured implementation of the Autonomous Trading Crew
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_new_structure():
    """Test that the new directory structure exists"""
    required_dirs = [
        'src/autonomous_trading_crew/agents',
        'src/autonomous_trading_crew/tasks',
        'src/autonomous_trading_crew/tools',
        'src/autonomous_trading_crew/ui',
        'src/autonomous_trading_crew/utils',
        'src/autonomous_trading_crew/examples'
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print("❌ Missing directories:")
        for dir_path in missing_dirs:
            print(f"  - {dir_path}")
        return False
    else:
        print("✅ All required directories are present")
        return True

def test_agent_files():
    """Test that agent files exist"""
    required_files = [
        'src/autonomous_trading_crew/agents/__init__.py',
        'src/autonomous_trading_crew/agents/market_intelligence_analyst.py',
        'src/autonomous_trading_crew/agents/risk_management_officer.py',
        'src/autonomous_trading_crew/agents/trade_execution_specialist.py',
        'src/autonomous_trading_crew/agents/explainability_reporter.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing agent files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    else:
        print("✅ All agent files are present")
        return True

def test_task_files():
    """Test that task files exist"""
    required_files = [
        'src/autonomous_trading_crew/tasks/__init__.py',
        'src/autonomous_trading_crew/tasks/multi_modal_signal_synthesis.py',
        'src/autonomous_trading_crew/tasks/risk_assessment_guardrail_check.py',
        'src/autonomous_trading_crew/tasks/tax_optimized_execution_plan.py',
        'src/autonomous_trading_crew/tasks/decision_explanation_report.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing task files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    else:
        print("✅ All task files are present")
        return True

def main():
    """Run all tests"""
    print("🧪 Testing Restructured Autonomous Trading Crew Implementation")
    print("=" * 60)
    
    tests = [
        test_new_structure,
        test_agent_files,
        test_task_files
    ]
    
    passed = 0
    for test in tests:
        print(f"\nRunning {test.__name__}...")
        if test():
            passed += 1
    
    print(f"\n🏁 Test Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! The restructured implementation is ready.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())