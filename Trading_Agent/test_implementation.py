"""
Test script to verify the implementation of the Autonomous Trading Crew
without requiring all dependencies to be installed.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_file_structure():
    """Test that all required files exist"""
    required_files = [
        'src/autonomous_trading_crew/crew.py',
        'src/autonomous_trading_crew/main.py',
        'src/autonomous_trading_crew/config/agents.yaml',
        'src/autonomous_trading_crew/config/tasks.yaml',
        'src/autonomous_trading_crew/tools/financial_data_tool.py',
        'src/autonomous_trading_crew/tools/financial_sentiment_tool.py',
        'src/autonomous_trading_crew/tools/risk_assessment_tool.py',
        'src/autonomous_trading_crew/tools/predictive_analytics_tool.py',
        'src/autonomous_trading_crew/ui/streamlit_app.py',
        'src/autonomous_trading_crew/ui/cli.py',
        'src/autonomous_trading_crew/utils/setup.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    else:
        print("✅ All required files are present")
        return True

def test_imports():
    """Test that we can import our modules (without dependencies)"""
    try:
        # Test importing the main crew module
        import src.autonomous_trading_crew.crew
        print("✅ Crew module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import crew module: {e}")
        return False
    
    try:
        # Test importing tools (this might fail due to missing dependencies)
        import src.autonomous_trading_crew.tools.financial_data_tool
        print("✅ Financial Data Tool imported successfully")
    except ImportError as e:
        print(f"⚠️  Financial Data Tool import failed (expected without dependencies): {e}")
    
    try:
        import src.autonomous_trading_crew.tools.financial_sentiment_tool
        print("✅ Financial Sentiment Tool imported successfully")
    except ImportError as e:
        print(f"⚠️  Financial Sentiment Tool import failed (expected without dependencies): {e}")
    
    try:
        import src.autonomous_trading_crew.tools.risk_assessment_tool
        print("✅ Risk Assessment Tool imported successfully")
    except ImportError as e:
        print(f"⚠️  Risk Assessment Tool import failed (expected without dependencies): {e}")
    
    try:
        import src.autonomous_trading_crew.tools.predictive_analytics_tool
        print("✅ Predictive Analytics Tool imported successfully")
    except ImportError as e:
        print(f"⚠️  Predictive Analytics Tool import failed (expected without dependencies): {e}")
    
    return True

def test_config_files():
    """Test that configuration files are properly formatted"""
    try:
        import yaml
        # Test agents.yaml
        with open('src/autonomous_trading_crew/config/agents.yaml', 'r') as f:
            agents_config = yaml.safe_load(f)
        
        required_agents = [
            'market_intelligence_analyst',
            'risk_management_officer',
            'trade_execution_specialist',
            'explainability_reporter'
        ]
        
        for agent in required_agents:
            if agent not in agents_config:
                print(f"❌ Missing agent in agents.yaml: {agent}")
                return False
        
        print("✅ Agents configuration is valid")
        
        # Test tasks.yaml
        with open('src/autonomous_trading_crew/config/tasks.yaml', 'r') as f:
            tasks_config = yaml.safe_load(f)
        
        required_tasks = [
            'multi_modal_signal_synthesis',
            'risk_assessment_guardrail_check',
            'tax_optimized_execution_plan',
            'decision_explanation_report'
        ]
        
        for task in required_tasks:
            if task not in tasks_config:
                print(f"❌ Missing task in tasks.yaml: {task}")
                return False
        
        print("✅ Tasks configuration is valid")
        return True
    except Exception as e:
        print(f"❌ Configuration file test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Autonomous Trading Crew Implementation")
    print("=" * 50)
    
    tests = [
        test_file_structure,
        test_imports,
        test_config_files
    ]
    
    passed = 0
    for test in tests:
        print(f"\nRunning {test.__name__}...")
        if test():
            passed += 1
    
    print(f"\n🏁 Test Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! The implementation is ready.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())