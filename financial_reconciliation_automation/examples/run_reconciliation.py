"""
Example script demonstrating how to run the financial reconciliation with the new structure.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from financial_reconciliation_automation.utils.data_loader import load_csv_data, create_sample_data
from financial_reconciliation_automation.tools.financial_tools import match_transactions, generate_report


def main():
    """Run financial reconciliation with the new structure."""
    print("Financial Reconciliation with New Structure")
    print("=" * 50)
    
    # Create sample data if it doesn't exist
    try:
        create_sample_data()
        print("Sample data created successfully.")
    except Exception as e:
        print(f"Warning: Could not create sample data: {e}")
    
    # Load sample data
    try:
        transactions = load_csv_data("data/sample/transactions.csv")
        invoices = load_csv_data("data/sample/invoices.csv")
        
        print(f"\nLoaded {len(transactions)} transactions and {len(invoices)} invoices.")
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        print("Please ensure the sample data files exist in data/sample/")
        return
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
    # Match transactions and invoices
    print("\nMatching transactions with invoices...")
    matching_results = match_transactions(transactions, invoices)
    
    # Generate report
    print("\nGenerating reconciliation report...")
    report = generate_report(matching_results)
    
    # Create output directory if it doesn't exist
    os.makedirs("data/processed/reports", exist_ok=True)
    
    # Save report
    report_path = "data/processed/reports/new_structure_reconciliation_report.txt"
    with open(report_path, "w") as f:
        f.write(report)
    
    print(f"Report saved to {report_path}")
    print("\nReconciliation Summary:")
    print(f"  Matched transactions: {len(matching_results['matched'])}")
    print(f"  Unmatched transactions: {len(matching_results['unmatched_transactions'])}")
    print(f"  Unmatched invoices: {len(matching_results['unmatched_invoices'])}")


if __name__ == "__main__":
    main()