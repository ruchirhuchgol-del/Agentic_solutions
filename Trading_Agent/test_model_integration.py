#!/usr/bin/env python
"""
Test script to verify the integration of new models with existing tools
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_model_files():
    """Test that model files exist and can be imported"""
    try:
        from models.financial_sentiment_model import FinancialSentimentModel, get_sentiment_model
        print("✅ Financial Sentiment Model imported successfully")
        
        # Test singleton instance
        model1 = get_sentiment_model()
        model2 = get_sentiment_model()
        if model1 is model2:
            print("✅ Singleton pattern working for sentiment model")
        else:
            print("⚠️  Singleton pattern not working for sentiment model")
            
    except ImportError as e:
        print(f"❌ Failed to import Financial Sentiment Model: {e}")
        return False
    
    try:
        from models.volatility_model import VolatilityPredictor, get_volatility_model
        print("✅ Volatility Prediction Model imported successfully")
        
        # Test singleton instance
        model1 = get_volatility_model()
        model2 = get_volatility_model()
        if model1 is model2:
            print("✅ Singleton pattern working for volatility model")
        else:
            print("⚠️  Singleton pattern not working for volatility model")
            
    except ImportError as e:
        print(f"❌ Failed to import Volatility Prediction Model: {e}")
        return False
    
    try:
        from models.risk_factor_model import RiskFactorModel, get_risk_factor_model
        print("✅ Risk Factor Model imported successfully")
        
        # Test singleton instance
        model1 = get_risk_factor_model()
        model2 = get_risk_factor_model()
        if model1 is model2:
            print("✅ Singleton pattern working for risk factor model")
        else:
            print("⚠️  Singleton pattern not working for risk factor model")
            
    except ImportError as e:
        print(f"❌ Failed to import Risk Factor Model: {e}")
        return False
    
    return True

def test_model_functionality():
    """Test basic functionality of models"""
    try:
        from models.financial_sentiment_model import get_sentiment_model
        
        # Test sentiment analysis
        model = get_sentiment_model()
        test_texts = [
            "The company reported strong earnings and exceeded expectations",
            "The stock price declined due to market concerns",
            "Market analysts are bullish on the company's growth prospects"
        ]
        
        results = model.predict(test_texts)
        if len(results) == 3 and all('sentiment' in r for r in results):
            print("✅ Sentiment model prediction working")
        else:
            print("❌ Sentiment model prediction failed")
            
    except Exception as e:
        print(f"❌ Sentiment model functionality test failed: {e}")
        return False
    
    try:
        from models.volatility_model import get_volatility_model
        
        # Test volatility prediction
        model = get_volatility_model()
        # Features: return, volume, rsi, macd, vix
        features = [0.01, 1000000, 60, 0.5, 20]
        prediction = model.predict(features)
        if isinstance(prediction, float) and prediction > 0:
            print("✅ Volatility model prediction working")
        else:
            print("❌ Volatility model prediction failed")
            
    except Exception as e:
        print(f"❌ Volatility model functionality test failed: {e}")
        return False
    
    try:
        from models.risk_factor_model import get_risk_factor_model
        
        # Test risk factor prediction
        model = get_risk_factor_model()
        # Features: volatility, beta, sharpe_ratio, max_drawdown, var_95, correlation_market, liquidity_ratio, earnings_volatility
        features = [0.2, 1.2, 1.5, 0.1, 0.05, 0.6, 1.0, 0.3]
        prediction = model.predict(features)
        if isinstance(prediction, dict) and 'risk_level' in prediction:
            print("✅ Risk factor model prediction working")
        else:
            print("❌ Risk factor model prediction failed")
            
    except Exception as e:
        print(f"❌ Risk factor model functionality test failed: {e}")
        return False
    
    return True

def test_tool_integration():
    """Test that tools can integrate with models"""
    try:
        # Test that financial sentiment tool can be imported
        from src.autonomous_trading_crew.tools.financial_sentiment_tool import FinancialSentimentTool
        tool = FinancialSentimentTool()
        print("✅ Financial Sentiment Tool imported and instantiated successfully")
        
        # Test that risk assessment tool can be imported
        from src.autonomous_trading_crew.tools.risk_assessment_tool import RiskAssessmentTool
        tool = RiskAssessmentTool()
        print("✅ Risk Assessment Tool imported and instantiated successfully")
        
        # Test that predictive analytics tool can be imported
        from src.autonomous_trading_crew.tools.predictive_analytics_tool import PredictiveAnalyticsTool
        tool = PredictiveAnalyticsTool()
        print("✅ Predictive Analytics Tool imported and instantiated successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Tool import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Tool instantiation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Model Integration")
    print("=" * 40)
    
    tests = [
        test_model_files,
        test_model_functionality,
        test_tool_integration
    ]
    
    passed = 0
    for test in tests:
        print(f"\nRunning {test.__name__}...")
        if test():
            passed += 1
    
    print(f"\n🏁 Test Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Model integration is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())