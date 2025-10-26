"""
Tests for the financial reconciliation tools.
"""

import unittest
import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from financial_reconciliation_automation.tools.financial_tools import (
    match_transactions, validate_data, generate_report
)


class TestFinancialTools(unittest.TestCase):
    """Test cases for the financial tools."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.sample_transactions = [
            {"date": "2023-01-01", "amount": 100.00, "description": "Office supplies", "account": "Expense"},
            {"date": "2023-01-02", "amount": 250.00, "description": "Software subscription", "account": "Expense"},
        ]
        
        self.sample_invoices = [
            {"date": "2023-01-01", "amount": 100.00, "invoice_number": "INV-001", "vendor": "Office Supply Co"},
            {"date": "2023-01-02", "amount": 250.00, "invoice_number": "INV-002", "vendor": "Software Inc"},
        ]

    def test_match_transactions_exact_matches(self):
        """Test matching transactions with exact amount matches."""
        results = match_transactions(self.sample_transactions, self.sample_invoices)
        
        self.assertEqual(len(results['matched']), 2)
        self.assertEqual(len(results['unmatched_transactions']), 0)
        self.assertEqual(len(results['unmatched_invoices']), 0)

    def test_match_transactions_with_unmatched(self):
        """Test matching transactions with some unmatched items."""
        # Add a transaction without a matching invoice
        transactions = self.sample_transactions + [
            {"date": "2023-01-03", "amount": 500.00, "description": "Consulting", "account": "Expense"}
        ]
        
        results = match_transactions(transactions, self.sample_invoices)
        
        self.assertEqual(len(results['matched']), 2)
        self.assertEqual(len(results['unmatched_transactions']), 1)
        self.assertEqual(len(results['unmatched_invoices']), 0)

    def test_validate_data_valid_transactions(self):
        """Test validating valid transaction data."""
        results = validate_data(self.sample_transactions, 'transactions')
        
        self.assertTrue(results['valid'])
        self.assertEqual(len(results['errors']), 0)

    def test_validate_data_invalid_transactions(self):
        """Test validating invalid transaction data."""
        invalid_transactions = [
            {"date": "2023-01-01", "amount": 100.00},  # Missing required fields
        ]
        
        results = validate_data(invalid_transactions, 'transactions')
        
        self.assertFalse(results['valid'])
        self.assertGreater(len(results['errors']), 0)

    def test_generate_report(self):
        """Test generating a reconciliation report."""
        matching_results = {
            'matched': [],
            'unmatched_transactions': self.sample_transactions,
            'unmatched_invoices': self.sample_invoices
        }
        
        report = generate_report(matching_results)
        
        self.assertIsInstance(report, str)
        self.assertIn("Financial Reconciliation Report", report)
        self.assertIn("Unmatched Transactions", report)
        self.assertIn("Unmatched Invoices", report)


if __name__ == '__main__':
    unittest.main()