"""
Tests for the langchain tools.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from financial_reconciliation_automation.tools.langchain_tools import (
    DiscrepancyAnalysisTool, 
    TransactionCategorizationTool,
    DiscrepancyAnalysisInput,
    TransactionCategorizationInput
)

class TestLangchainTools(unittest.TestCase):
    """Test cases for the langchain tools."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        pass

    def test_discrepancy_analysis_tool_creation(self):
        """Test that the discrepancy analysis tool is created correctly."""
        tool = DiscrepancyAnalysisTool()
        self.assertEqual(tool.name, "discrepancy_analyzer")
        self.assertEqual(tool.description, "Analyzes financial discrepancies and provides insights.")
        self.assertEqual(tool.args_schema, DiscrepancyAnalysisInput)

    def test_transaction_categorization_tool_creation(self):
        """Test that the transaction categorization tool is created correctly."""
        tool = TransactionCategorizationTool()
        self.assertEqual(tool.name, "transaction_categorizer")
        self.assertEqual(tool.description, "Categorizes financial transactions using AI.")
        self.assertEqual(tool.args_schema, TransactionCategorizationInput)

    @patch('financial_reconciliation_automation.tools.langchain_tools.ChatOpenAI')
    def test_discrepancy_analysis_tool_run(self, mock_chat_openai):
        """Test running the discrepancy analysis tool."""
        # Mock the LLM response
        mock_llm_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "Potential Reasons:\n1. Timing differences\n2. Data entry errors\n\nRecommendations:\n1. Review timing\n2. Verify data"
        mock_llm_instance.invoke.return_value = mock_response
        mock_chat_openai.return_value = mock_llm_instance
        
        # Mock the prompt
        with patch('financial_reconciliation_automation.tools.langchain_tools.ChatPromptTemplate') as mock_prompt:
            mock_prompt_instance = MagicMock()
            mock_chain = MagicMock()
            mock_chain.__or__ = MagicMock(return_value=mock_chain)
            mock_chain.invoke = MagicMock(return_value=mock_response)
            mock_prompt_instance.__or__ = MagicMock(return_value=mock_chain)
            mock_prompt.from_template.return_value = mock_prompt_instance
            
            # Run the tool
            tool = DiscrepancyAnalysisTool()
            result = tool._run(
                unmatched_items="Transaction 1: $100, Invoice 1: $90",
                context="Q1 2024 financial period"
            )
            
            # Verify the result
            self.assertEqual(result, "Potential Reasons:\n1. Timing differences\n2. Data entry errors\n\nRecommendations:\n1. Review timing\n2. Verify data")
            mock_chat_openai.assert_called_once_with(model="gpt-4o-mini", temperature=0.3)

    @patch('financial_reconciliation_automation.tools.langchain_tools.ChatOpenAI')
    def test_transaction_categorization_tool_run(self, mock_chat_openai):
        """Test running the transaction categorization tool."""
        # Mock the LLM response
        mock_llm_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "Category: Office Supplies\n- Transaction 1\n- Transaction 2"
        mock_llm_instance.invoke.return_value = mock_response
        mock_chat_openai.return_value = mock_llm_instance
        
        # Mock the prompt
        with patch('financial_reconciliation_automation.tools.langchain_tools.ChatPromptTemplate') as mock_prompt:
            mock_prompt_instance = MagicMock()
            mock_chain = MagicMock()
            mock_chain.__or__ = MagicMock(return_value=mock_chain)
            mock_chain.invoke = MagicMock(return_value=mock_response)
            mock_prompt_instance.__or__ = MagicMock(return_value=mock_chain)
            mock_prompt.from_template.return_value = mock_prompt_instance
            
            # Run the tool
            tool = TransactionCategorizationTool()
            result = tool._run(
                transactions="Transaction 1: $50 Office Supplies, Transaction 2: $75 Office Supplies",
                categories="Office Supplies, Travel, Meals"
            )
            
            # Verify the result
            self.assertEqual(result, "Category: Office Supplies\n- Transaction 1\n- Transaction 2")
            mock_chat_openai.assert_called_once_with(model="gpt-4o-mini", temperature=0.3)

if __name__ == '__main__':
    unittest.main()