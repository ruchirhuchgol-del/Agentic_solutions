"""
Integration test to verify all components work together correctly.
"""

import unittest
import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from financial_reconciliation_automation.crew import FinancialReconciliationCrew
from financial_reconciliation_automation.tools.financial_tools import match_transactions, validate_data, generate_report
from financial_reconciliation_automation.tools.langchain_tools import DiscrepancyAnalysisTool, TransactionCategorizationTool

class TestIntegration(unittest.TestCase):
    """Test cases for integration of all components."""

    def test_crew_creation(self):
        """Test that the crew can be created successfully."""
        crew = FinancialReconciliationCrew()
        self.assertIsInstance(crew, FinancialReconciliationCrew)

    def test_financial_tools_integration(self):
        """Test that financial tools work together."""
        # Sample data
        transactions = [
            {"date": "2023-01-01", "amount": 100.00, "description": "Office supplies", "account": "Expense"},
            {"date": "2023-01-02", "amount": 250.00, "description": "Software subscription", "account": "Expense"},
        ]
        
        invoices = [
            {"date": "2023-01-01", "amount": 100.00, "invoice_number": "INV-001", "vendor": "Office Supply Co"},
            {"date": "2023-01-02", "amount": 250.00, "invoice_number": "INV-002", "vendor": "Software Inc"},
        ]
        
        # Validate data
        transaction_validation = validate_data(transactions, 'transactions')
        invoice_validation = validate_data(invoices, 'invoices')
        
        self.assertTrue(transaction_validation['valid'])
        self.assertTrue(invoice_validation['valid'])
        
        # Match transactions
        matching_results = match_transactions(transactions, invoices)
        
        self.assertEqual(len(matching_results['matched']), 2)
        self.assertEqual(len(matching_results['unmatched_transactions']), 0)
        self.assertEqual(len(matching_results['unmatched_invoices']), 0)
        
        # Generate report
        report = generate_report(matching_results)
        self.assertIsInstance(report, str)
        self.assertIn("Financial Reconciliation Report", report)

    def test_langchain_tools_creation(self):
        """Test that langchain tools can be created successfully."""
        discrepancy_tool = DiscrepancyAnalysisTool()
        categorization_tool = TransactionCategorizationTool()
        
        self.assertEqual(discrepancy_tool.name, "discrepancy_analyzer")
        self.assertEqual(categorization_tool.name, "transaction_categorizer")

    def test_agent_tools_integration(self):
        """Test that agents have the correct tools."""
        crew = FinancialReconciliationCrew()
        
        # Test that we can create all agents
        data_collector = crew.financial_data_collector()
        matching_specialist = crew.transaction_matching_specialist()
        discrepancy_reporter = crew.discrepancy_reporter()
        data_validator = crew.data_quality_validator()
        
        # Verify agents were created
        self.assertIsNotNone(data_collector)
        self.assertIsNotNone(matching_specialist)
        self.assertIsNotNone(discrepancy_reporter)
        self.assertIsNotNone(data_validator)

if __name__ == '__main__':
    unittest.main()