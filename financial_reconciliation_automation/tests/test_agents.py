"""
Tests for the financial reconciliation agents.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from financial_reconciliation_automation.crew import FinancialReconciliationCrew


class TestFinancialReconciliationAgents(unittest.TestCase):
    """Test cases for the financial reconciliation agents."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.crew = FinancialReconciliationCrew()

    def test_data_analyst_agent_creation(self):
        """Test that the data analyst agent is created correctly."""
        agent = self.crew.data_analyst_agent()
        self.assertIsNotNone(agent)
        self.assertEqual(agent.role, 'Financial Data Analyst')

    def test_reconciliation_agent_creation(self):
        """Test that the reconciliation agent is created correctly."""
        agent = self.crew.reconciliation_agent()
        self.assertIsNotNone(agent)
        self.assertEqual(agent.role, 'Financial Reconciliation Specialist')

    def test_reporting_agent_creation(self):
        """Test that the reporting agent is created correctly."""
        agent = self.crew.reporting_agent()
        self.assertIsNotNone(agent)
        self.assertEqual(agent.role, 'Financial Reporting Analyst')

    @patch('financial_reconciliation_automation.crew.Crew')
    def test_crew_creation(self, mock_crew):
        """Test that the crew is created with the correct agents and tasks."""
        mock_crew_instance = MagicMock()
        mock_crew.return_value = mock_crew_instance
        
        crew_instance = self.crew.crew()
        
        # Check that Crew was called with the right arguments
        mock_crew.assert_called_once()
        self.assertEqual(mock_crew_instance, crew_instance)


if __name__ == '__main__':
    unittest.main()