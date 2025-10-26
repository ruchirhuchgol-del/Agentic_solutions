

"""
Example script demonstrating how to use the langchain tools.
"""

import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from financial_reconciliation_automation.tools.langchain_tools import (
    DiscrepancyAnalysisTool, 
    TransactionCategorizationTool
)

def main():
    """Demonstrate the usage of langchain tools."""
    print("LangChain Tools Example")
    print("=" * 30)
    
    # Example 1: Discrepancy Analysis
    print("\n1. Discrepancy Analysis Tool")
    print("-" * 25)
    
    discrepancy_tool = DiscrepancyAnalysisTool()
    
    unmatched_items = """
    Transaction ID: T001, Amount: $1,250.00, Date: 2024-01-15
    Invoice ID: INV-2024-001, Amount: $1,125.00, Date: 2024-01-14
    
    Transaction ID: T002, Amount: $875.30, Date: 2024-01-16
    Invoice ID: INV-2024-002, Amount: $875.30, Date: 2024-01-20
    """
    
    context = "Q1 2024 financial period. Company experienced delays in invoice processing."
    
    print(f"Input - Unmatched Items:\n{unmatched_items}")
    print(f"Input - Context:\n{context}")
    
    # Note: This would actually call the LLM in a real scenario
    # For demonstration, we're just showing how to use the tool
    print("Note: In a real implementation, this would call an LLM to analyze the discrepancies.")
    
    # Example 2: Transaction Categorization
    print("\n2. Transaction Categorization Tool")
    print("-" * 30)
    
    categorization_tool = TransactionCategorizationTool()
    
    transactions = """
    - Transaction ID: T001, Amount: $50.00, Description: Office supplies
    - Transaction ID: T002, Amount: $250.00, Description: Software subscription
    - Transaction ID: T003, Amount: $150.00, Description: Team lunch
    - Transaction ID: T004, Amount: $400.00, Description: Airline tickets
    """
    
    categories = "Office Expenses, Software, Meals, Travel, Miscellaneous"
    
    print(f"Input - Transactions:\n{transactions}")
    print(f"Input - Categories:\n{categories}")
    
    # Note: This would actually call the LLM in a real scenario
    # For demonstration, we're just showing how to use the tool
    print("Note: In a real implementation, this would call an LLM to categorize the transactions.")
    
    print("\nBoth tools are now ready to be integrated into the financial reconciliation workflow!")

if __name__ == "__main__":
    main()