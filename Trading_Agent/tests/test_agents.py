"""
Unit tests for the agents
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestMarketIntelligenceAnalyst(unittest.TestCase):
    """Test cases for the Market Intelligence Analyst agent"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.agents_config = {
            "market_intelligence_analyst": {
                "role": "Market Intelligence Analyst",
                "goal": "Analyze market data and generate trading signals",
                "backstory": "Expert in market analysis"
            }
        }
    
    def test_agent_creation(self):
        """Test that the agent can be created"""
        try:
            from autonomous_trading_crew.agents.market_intelligence_analyst import create_market_intelligence_analyst
            # Mock the Agent class to avoid dependency issues
            with patch('autonomous_trading_crew.agents.market_intelligence_analyst.Agent') as mock_agent:
                mock_agent.return_value = MagicMock()
                agent = create_market_intelligence_analyst(self.agents_config)
                self.assertIsNotNone(agent)
        except ImportError:
            self.skipTest("Market Intelligence Analyst module not available")

class TestRiskManagementOfficer(unittest.TestCase):
    """Test cases for the Risk Management Officer agent"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.agents_config = {
            "risk_management_officer": {
                "role": "Risk Management Officer",
                "goal": "Assess and manage trading risks",
                "backstory": "Expert in risk management"
            }
        }
    
    def test_agent_creation(self):
        """Test that the agent can be created"""
        try:
            from autonomous_trading_crew.agents.risk_management_officer import create_risk_management_officer
            # Mock the Agent class to avoid dependency issues
            with patch('autonomous_trading_crew.agents.risk_management_officer.Agent') as mock_agent:
                mock_agent.return_value = MagicMock()
                agent = create_risk_management_officer(self.agents_config)
                self.assertIsNotNone(agent)
        except ImportError:
            self.skipTest("Risk Management Officer module not available")

class TestTradeExecutionSpecialist(unittest.TestCase):
    """Test cases for the Trade Execution Specialist agent"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.agents_config = {
            "trade_execution_specialist": {
                "role": "Trade Execution Specialist",
                "goal": "Create execution plans for trades",
                "backstory": "Expert in trade execution"
            }
        }
    
    def test_agent_creation(self):
        """Test that the agent can be created"""
        try:
            from autonomous_trading_crew.agents.trade_execution_specialist import create_trade_execution_specialist
            # Mock the Agent class to avoid dependency issues
            with patch('autonomous_trading_crew.agents.trade_execution_specialist.Agent') as mock_agent:
                mock_agent.return_value = MagicMock()
                agent = create_trade_execution_specialist(self.agents_config)
                self.assertIsNotNone(agent)
        except ImportError:
            self.skipTest("Trade Execution Specialist module not available")

class TestExplainabilityReporter(unittest.TestCase):
    """Test cases for the Explainability Reporter agent"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.agents_config = {
            "explainability_reporter": {
                "role": "Explainability Reporter",
                "goal": "Generate explainable reports",
                "backstory": "Expert in creating understandable reports"
            }
        }
    
    def test_agent_creation(self):
        """Test that the agent can be created"""
        try:
            from autonomous_trading_crew.agents.explainability_reporter import create_explainability_reporter
            # Mock the Agent class to avoid dependency issues
            with patch('autonomous_trading_crew.agents.explainability_reporter.Agent') as mock_agent:
                mock_agent.return_value = MagicMock()
                agent = create_explainability_reporter(self.agents_config)
                self.assertIsNotNone(agent)
        except ImportError:
            self.skipTest("Explainability Reporter module not available")

if __name__ == '__main__':
    unittest.main()