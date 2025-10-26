"""
Tests for the financial reconciliation chains.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from financial_reconciliation_automation.chains.validation_chain import (
    create_validation_chain, run_validation_chain
)
from financial_reconciliation_automation.chains.matching_chain import (
    create_matching_chain, run_matching_chain
)
from financial_reconciliation_automation.chains.reporting_chain import (
    create_reporting_chain, run_reporting_chain
)


class TestValidationChain(unittest.TestCase):
    """Test cases for the validation chain."""

    @patch('financial_reconciliation_automation.chains.validation_chain.LLMChain')
    def test_create_validation_chain(self, mock_llm_chain):
        """Test creating a validation chain."""
        mock_llm = MagicMock()
        chain = create_validation_chain(mock_llm)
        
        self.assertIsNotNone(chain)
        mock_llm_chain.assert_called_once()

    @patch('financial_reconciliation_automation.chains.validation_chain.LLMChain')
    def test_run_validation_chain(self, mock_llm_chain):
        """Test running a validation chain."""
        mock_chain = MagicMock()
        mock_chain.run.return_value = "Validation results"
        
        result = run_validation_chain(mock_chain, "test data", "transactions")
        
        self.assertEqual(result, "Validation results")
        mock_chain.run.assert_called_once_with(data="test data", data_type="transactions")


class TestMatchingChain(unittest.TestCase):
    """Test cases for the matching chain."""

    @patch('financial_reconciliation_automation.chains.matching_chain.LLMChain')
    def test_create_matching_chain(self, mock_llm_chain):
        """Test creating a matching chain."""
        mock_llm = MagicMock()
        chain = create_matching_chain(mock_llm)
        
        self.assertIsNotNone(chain)
        mock_llm_chain.assert_called_once()

    @patch('financial_reconciliation_automation.chains.matching_chain.LLMChain')
    def test_run_matching_chain(self, mock_llm_chain):
        """Test running a matching chain."""
        mock_chain = MagicMock()
        mock_chain.run.return_value = "Matching results"
        
        result = run_matching_chain(mock_chain, "transactions data", "invoices data")
        
        self.assertEqual(result, "Matching results")
        mock_chain.run.assert_called_once_with(transactions="transactions data", invoices="invoices data")


class TestReportingChain(unittest.TestCase):
    """Test cases for the reporting chain."""

    @patch('financial_reconciliation_automation.chains.reporting_chain.LLMChain')
    def test_create_reporting_chain(self, mock_llm_chain):
        """Test creating a reporting chain."""
        mock_llm = MagicMock()
        chain = create_reporting_chain(mock_llm)
        
        self.assertIsNotNone(chain)
        mock_llm_chain.assert_called_once()

    @patch('financial_reconciliation_automation.chains.reporting_chain.LLMChain')
    def test_run_reporting_chain(self, mock_llm_chain):
        """Test running a reporting chain."""
        mock_chain = MagicMock()
        mock_chain.run.return_value = "Report content"
        
        result = run_reporting_chain(mock_chain, "matching results")
        
        self.assertEqual(result, "Report content")
        mock_chain.run.assert_called_once_with(matching_results="matching results")


if __name__ == '__main__':
    unittest.main()