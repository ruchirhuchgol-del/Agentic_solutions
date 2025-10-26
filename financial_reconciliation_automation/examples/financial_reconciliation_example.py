"""
Example script demonstrating how to use the financial reconciliation tools directly.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from financial_reconciliation_automation.utils.data_loader import load_csv_data
from financial_reconciliation_automation.tools.financial_tools import match_transactions, validate_data, generate_report
from financial_reconciliation_automation.utils.validators import validate_transaction_data, validate_invoice_data


def main():
    """Run a simple example of financial reconciliation."""
    print("Financial Reconciliation Example")
    print("=" * 40)
    
    # Load sample data
    try:
        transactions = load_csv_data("data/sample/transactions.csv")
        invoices = load_csv_data("data/sample/invoices.csv")
        
        print(f"Loaded {len(transactions)} transactions and {len(invoices)} invoices.")
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        print("Please ensure the sample data files exist in data/sample/")
        return
    
    # Validate data
    print("\nValidating data...")
    transaction_validation = validate_transaction_data(transactions)
    invoice_validation = validate_invoice_data(invoices)
    
    if not transaction_validation['valid']:
        print("Transaction validation errors:")
        for error in transaction_validation['errors']:
            print(f"  - {error}")
    
    if not invoice_validation['valid']:
        print("Invoice validation errors:")
        for error in invoice_validation['errors']:
            print(f"  - {error}")
    
    if not transaction_validation['valid'] or not invoice_validation['valid']:
        print("Data validation failed. Please fix the errors before proceeding.")
        return
    
    print("Data validation passed.")
    
    # Match transactions and invoices
    print("\nMatching transactions with invoices...")
    matching_results = match_transactions(transactions, invoices)
    
    # Generate report
    print("\nGenerating reconciliation report...")
    report = generate_report(matching_results)
    
    # Save report
    with open("data/processed/reports/example_reconciliation_report.txt", "w") as f:
        f.write(report)
    
    print("Report saved to data/processed/reports/example_reconciliation_report.txt")
    print("\nReconciliation Summary:")
    print(f"  Matched transactions: {len(matching_results['matched'])}")
    print(f"  Unmatched transactions: {len(matching_results['unmatched_transactions'])}")
    print(f"  Unmatched invoices: {len(matching_results['unmatched_invoices'])}")
    
    # Print report to console
    print("\nReconciliation Report:")
    print("-" * 40)
    print(report)


if __name__ == "__main__":
    main()