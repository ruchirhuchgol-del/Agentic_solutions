#!/usr/bin/env python
"""
Test script to verify that all tools can be imported and instantiated without errors
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_tool_imports():
    """Test that all tools can be imported and instantiated"""
    print("Testing tool imports and instantiation...")
    
    # Test FinancialDataTool
    try:
        from src.autonomous_trading_crew.tools.financial_data_tool import FinancialDataTool
        tool = FinancialDataTool()
        print("✅ FinancialDataTool: Import and instantiation successful")
    except Exception as e:
        print(f"❌ FinancialDataTool: Failed - {e}")
        return False
    
    # Test FinancialSentimentTool
    try:
        from src.autonomous_trading_crew.tools.financial_sentiment_tool import FinancialSentimentTool
        tool = FinancialSentimentTool()
        print("✅ FinancialSentimentTool: Import and instantiation successful")
    except Exception as e:
        print(f"❌ FinancialSentimentTool: Failed - {e}")
        return False
    
    # Test RiskAssessmentTool
    try:
        from src.autonomous_trading_crew.tools.risk_assessment_tool import RiskAssessmentTool
        tool = RiskAssessmentTool()
        print("✅ RiskAssessmentTool: Import and instantiation successful")
    except Exception as e:
        print(f"❌ RiskAssessmentTool: Failed - {e}")
        return False
    
    # Test PredictiveAnalyticsTool
    try:
        from src.autonomous_trading_crew.tools.predictive_analytics_tool import PredictiveAnalyticsTool
        tool = PredictiveAnalyticsTool()
        print("✅ PredictiveAnalyticsTool: Import and instantiation successful")
    except Exception as e:
        print(f"❌ PredictiveAnalyticsTool: Failed - {e}")
        return False
    
    # Test TaxOptimizationTool
    try:
        from src.autonomous_trading_crew.tools.tax_optimization_tool import TaxOptimizationTool
        tool = TaxOptimizationTool()
        print("✅ TaxOptimizationTool: Import and instantiation successful")
    except Exception as e:
        print(f"❌ TaxOptimizationTool: Failed - {e}")
        return False
    
    return True

def test_agent_imports():
    """Test that all agents can be imported and created"""
    print("\nTesting agent imports and creation...")
    
    # Mock agents config
    agents_config = {
        "market_intelligence_analyst": {
            "role": "Market Intelligence Analyst",
            "goal": "Analyze market data",
            "backstory": "Expert analyst"
        },
        "risk_management_officer": {
            "role": "Risk Management Officer", 
            "goal": "Manage risks",
            "backstory": "Risk expert"
        },
        "trade_execution_specialist": {
            "role": "Trade Execution Specialist",
            "goal": "Execute trades",
            "backstory": "Execution expert"
        },
        "explainability_reporter": {
            "role": "Explainability Reporter",
            "goal": "Explain decisions",
            "backstory": "Communication expert"
        }
    }
    
    # Test Market Intelligence Analyst
    try:
        from src.autonomous_trading_crew.agents.market_intelligence_analyst import create_market_intelligence_analyst
        agent = create_market_intelligence_analyst(agents_config)
        print("✅ Market Intelligence Analyst: Creation successful")
    except Exception as e:
        print(f"❌ Market Intelligence Analyst: Failed - {e}")
        return False
    
    # Test Risk Management Officer
    try:
        from src.autonomous_trading_crew.agents.risk_management_officer import create_risk_management_officer
        agent = create_risk_management_officer(agents_config)
        print("✅ Risk Management Officer: Creation successful")
    except Exception as e:
        print(f"❌ Risk Management Officer: Failed - {e}")
        return False
    
    # Test Trade Execution Specialist
    try:
        from src.autonomous_trading_crew.agents.trade_execution_specialist import create_trade_execution_specialist
        agent = create_trade_execution_specialist(agents_config)
        print("✅ Trade Execution Specialist: Creation successful")
    except Exception as e:
        print(f"❌ Trade Execution Specialist: Failed - {e}")
        return False
    
    # Test Explainability Reporter
    try:
        from src.autonomous_trading_crew.agents.explainability_reporter import create_explainability_reporter
        agent = create_explainability_reporter(agents_config)
        print("✅ Explainability Reporter: Creation successful")
    except Exception as e:
        print(f"❌ Explainability Reporter: Failed - {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Testing Tool and Agent Integration")
    print("=" * 40)
    
    tool_success = test_tool_imports()
    agent_success = test_agent_imports()
    
    print(f"\n🏁 Test Results:")
    if tool_success and agent_success:
        print("🎉 All tests passed! Tools and agents are working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())