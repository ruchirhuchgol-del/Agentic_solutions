"""
Tests for the financial reconciliation tasks.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from financial_reconciliation_automation.crew import FinancialReconciliationCrew


class TestFinancialReconciliationTasks(unittest.TestCase):
    """Test cases for the financial reconciliation tasks."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.crew = FinancialReconciliationCrew()
        # Create mock agents for testing
        self.mock_data_analyst = MagicMock()
        self.mock_reconciliation_agent = MagicMock()
        self.mock_reporting_agent = MagicMock()

    def test_data_analysis_task_creation(self):
        """Test that the data analysis task is created correctly."""
        task = self.crew.data_analysis_task(self.mock_data_analyst)
        self.assertIsNotNone(task)
        self.assertIn('analyze financial data', task.description.lower())

    def test_reconciliation_task_creation(self):
        """Test that the reconciliation task is created correctly."""
        task = self.crew.reconciliation_task(self.mock_reconciliation_agent)
        self.assertIsNotNone(task)
        self.assertIn('match transactions', task.description.lower())

    def test_reporting_task_creation(self):
        """Test that the reporting task is created correctly."""
        task = self.crew.reporting_task(self.mock_reporting_agent)
        self.assertIsNotNone(task)
        self.assertIn('generate a detailed report', task.description.lower())


if __name__ == '__main__':
    unittest.main()