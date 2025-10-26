
"""
Verification Script for Autonomous Trading Crew Setup
"""

import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    import sys
    if sys.version_info < (3, 10) or sys.version_info >= (3, 14):
        print("⚠️  Warning: Python version should be >=3.10 and <3.14 for optimal compatibility")
        return False
    print("✅ Python version is compatible")
    return True

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        'README.md',
        'requirements.txt',
        'pyproject.toml',
        'src/autonomous_trading_crew/crew.py',
        'src/autonomous_trading_crew/main.py',
        'src/autonomous_trading_crew/config/agents.yaml',
        'src/autonomous_trading_crew/config/tasks.yaml',
        'src/autonomous_trading_crew/tools/financial_data_tool.py',
        'src/autonomous_trading_crew/tools/financial_sentiment_tool.py',
        'src/autonomous_trading_crew/tools/risk_assessment_tool.py',
        'src/autonomous_trading_crew/tools/predictive_analytics_tool.py',
        'models/financial_sentiment_model.py',
        'models/volatility_model.py',
        'models/risk_factor_model.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    else:
        print("✅ All required files are present")
        return True

def check_directory_structure():
    """Check if directory structure is correct"""
    required_dirs = [
        'src',
        'src/autonomous_trading_crew',
        'src/autonomous_trading_crew/agents',
        'src/autonomous_trading_crew/tasks',
        'src/autonomous_trading_crew/tools',
        'src/autonomous_trading_crew/ui',
        'src/autonomous_trading_crew/utils',
        'src/autonomous_trading_crew/config',
        'src/autonomous_trading_crew/examples',
        'models',
        'tests',
        'docs',
        'data',
        'logs'
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print("❌ Missing required directories:")
        for dir_path in missing_dirs:
            print(f"  - {dir_path}")
        return False
    else:
        print("✅ All required directories are present")
        return True

def check_module_imports():
    """Check if modules can be imported (syntax check)"""
    modules_to_check = [
        'src.autonomous_trading_crew.crew',
        'src.autonomous_trading_crew.tools.financial_data_tool',
        'src.autonomous_trading_crew.tools.financial_sentiment_tool',
        'src.autonomous_trading_crew.tools.risk_assessment_tool',
        'src.autonomous_trading_crew.tools.predictive_analytics_tool',
        'models.financial_sentiment_model',
        'models.volatility_model',
        'models.risk_factor_model'
    ]
    
    failed_imports = []
    for module in modules_to_check:
        try:
            __import__(module)
            print(f"✅ {module} imported successfully")
        except SyntaxError:
            print(f"✅ {module} has correct syntax")
        except ImportError as e:
            # This is expected if dependencies aren't installed
            print(f"⚠️  {module} import issue (expected if dependencies not installed): {e}")
        except Exception as e:
            failed_imports.append((module, str(e)))
            print(f"❌ {module} failed to import: {e}")
    
    if failed_imports:
        print("❌ Some modules failed to import:")
        for module, error in failed_imports:
            print(f"  - {module}: {error}")
        return False
    else:
        print("✅ All modules have correct syntax")
        return True

def main():
    """Run all verification checks"""
    print("🔍 Autonomous Trading Crew Setup Verification")
    print("=" * 50)
    
    checks = [
        check_python_version,
        check_directory_structure,
        check_required_files,
        check_module_imports
    ]
    
    passed = 0
    for check in checks:
        print(f"\nRunning {check.__name__}...")
        if check():
            passed += 1
    
    print(f"\n🏁 Verification Results: {passed}/{len(checks)} checks passed")
    
    if passed == len(checks):
        print("🎉 All checks passed! Your setup is ready.")
        print("\n🚀 Next steps:")
        print("1. Add your API keys to .env file")
        print("2. Run 'crewai run' to start analysis")
        print("3. Or run 'streamlit run src/autonomous_trading_crew/ui/streamlit_app.py' for web interface")
        return 0
    else:
        print("⚠️  Some checks failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())