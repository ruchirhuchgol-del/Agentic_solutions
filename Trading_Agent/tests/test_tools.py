"""
Unit tests for the custom financial tools module
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

    
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestFinancialDataTool(unittest.TestCase):
    """Test cases for the Financial Data Tool"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        try:
            from autonomous_trading_crew.tools.financial_data_tool import FinancialDataTool
            self.tool = FinancialDataTool()
        except ImportError:
            self.tool = None
    
    def test_tool_initialization(self):
        """Test that the tool initializes correctly"""
        if self.tool:
            self.assertIsNotNone(self.tool)
            self.assertEqual(self.tool.name, "Financial Data API")
            self.assertEqual(self.tool.description, "Fetches real-time and historical market data from Yahoo Finance")
        else:
            self.skipTest("FinancialDataTool not available due to missing dependencies")

class TestFinancialSentimentTool(unittest.TestCase):
    """Test cases for the Financial Sentiment Tool"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        try:
            from autonomous_trading_crew.tools.financial_sentiment_tool import FinancialSentimentTool
            self.tool = FinancialSentimentTool()
        except ImportError:
            self.tool = None
    
    def test_tool_initialization(self):
        """Test that the tool initializes correctly"""
        if self.tool:
            self.assertIsNotNone(self.tool)
            self.assertEqual(self.tool.name, "Financial Sentiment Analyzer")
            self.assertEqual(self.tool.description, "Analyzes sentiment of financial news with specialized financial model")
        else:
            self.skipTest("FinancialSentimentTool not available due to missing dependencies")

class TestRiskAssessmentTool(unittest.TestCase):
    """Test cases for the Risk Assessment Tool"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        try:
            from autonomous_trading_crew.tools.risk_assessment_tool import RiskAssessmentTool
            self.tool = RiskAssessmentTool()
        except ImportError:
            self.tool = None
    
    def test_tool_initialization(self):
        """Test that the tool initializes correctly"""
        if self.tool:
            self.assertIsNotNone(self.tool)
            self.assertEqual(self.tool.name, "Risk Assessment Analyzer")
            self.assertEqual(self.tool.description, "Calculates financial risk metrics including Value at Risk (VaR), Conditional VaR, and other risk indicators")
        else:
            self.skipTest("RiskAssessmentTool not available due to missing dependencies")

class TestPredictiveAnalyticsTool(unittest.TestCase):
    """Test cases for the Predictive Analytics Tool"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        try:
            from autonomous_trading_crew.tools.predictive_analytics_tool import PredictiveAnalyticsTool
            self.tool = PredictiveAnalyticsTool()
        except ImportError:
            self.tool = None
    
    def test_tool_initialization(self):
        """Test that the tool initializes correctly"""
        if self.tool:
            self.assertIsNotNone(self.tool)
            self.assertEqual(self.tool.name, "Predictive Analytics Tool")
            self.assertEqual(self.tool.description, "Uses LSTM, ARIMA, and SARIMA models to predict future stock prices")
        else:
            self.skipTest("PredictiveAnalyticsTool not available due to missing dependencies")

if __name__ == '__main__':
    unittest.main()