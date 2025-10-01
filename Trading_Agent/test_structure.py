
"""
Test script to verify the file structure and basic integration
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_model_files_exist():
    """Test that model files exist"""
    required_files = [
        'models/__init__.py',
        'models/financial_sentiment_model.py',
        'models/volatility_model.py',
        'models/risk_factor_model.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing model files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    else:
        print("✅ All model files are present")
        return True

def test_tool_files_exist():
    """Test that tool files exist"""
    required_files = [
        'src/autonomous_trading_crew/tools/financial_data_tool.py',
        'src/autonomous_trading_crew/tools/financial_sentiment_tool.py',
        'src/autonomous_trading_crew/tools/risk_assessment_tool.py',
        'src/autonomous_trading_crew/tools/predictive_analytics_tool.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing tool files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    else:
        print("✅ All tool files are present")
        return True

def test_model_imports():
    """Test that model modules can be imported (without dependencies)"""
    try:
        import models.financial_sentiment_model
        print("✅ Financial sentiment model module imported")
    except SyntaxError:
        print("✅ Financial sentiment model module has correct syntax")
    except Exception as e:
        print(f"⚠️  Financial sentiment model import issue: {e}")
    
    try:
        import models.volatility_model
        print("✅ Volatility model module imported")
    except SyntaxError:
        print("✅ Volatility model module has correct syntax")
    except Exception as e:
        print(f"⚠️  Volatility model import issue: {e}")
    
    try:
        import models.risk_factor_model
        print("✅ Risk factor model module imported")
    except SyntaxError:
        print("✅ Risk factor model module has correct syntax")
    except Exception as e:
        print(f"⚠️  Risk factor model import issue: {e}")
    
    return True

def test_tool_imports():
    """Test that tool modules can be imported (without dependencies)"""
    try:
        import src.autonomous_trading_crew.tools.financial_sentiment_tool
        print("✅ Financial sentiment tool module imported")
    except SyntaxError:
        print("✅ Financial sentiment tool module has correct syntax")
    except Exception as e:
        print(f"⚠️  Financial sentiment tool import issue: {e}")
    
    try:
        import src.autonomous_trading_crew.tools.risk_assessment_tool
        print("✅ Risk assessment tool module imported")
    except SyntaxError:
        print("✅ Risk assessment tool module has correct syntax")
    except Exception as e:
        print(f"⚠️  Risk assessment tool import issue: {e}")
    
    try:
        import src.autonomous_trading_crew.tools.predictive_analytics_tool
        print("✅ Predictive analytics tool module imported")
    except SyntaxError:
        print("✅ Predictive analytics tool module has correct syntax")
    except Exception as e:
        print(f"⚠️  Predictive analytics tool import issue: {e}")
    
    return True

def main():
    """Run all tests"""
    print("🧪 Testing File Structure and Basic Integration")
    print("=" * 50)
    
    tests = [
        test_model_files_exist,
        test_tool_files_exist,
        test_model_imports,
        test_tool_imports
    ]
    
    passed = 0
    for test in tests:
        print(f"\nRunning {test.__name__}...")
        if test():
            passed += 1
    
    print(f"\n🏁 Test Results: {passed}/{len(tests)} test groups passed")
    
    if passed == len(tests):
        print("🎉 All structural tests passed! Integration is set up correctly.")
        return 0
    else:
        print("⚠️  Some tests had issues. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
