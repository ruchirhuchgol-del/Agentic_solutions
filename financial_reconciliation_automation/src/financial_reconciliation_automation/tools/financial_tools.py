"""
Financial-specific tools for the financial reconciliation automation system.
"""

import json
import os
from typing import List, Dict, Any

def match_transactions(transactions: List[Dict], invoices: List[Dict]) -> Dict[str, Any]:
    """
    Match transactions with invoices based on amount and date.
    
    Args:
        transactions (List[Dict]): List of transaction dictionaries
        invoices (List[Dict]): List of invoice dictionaries
        
    Returns:
        Dict[str, Any]: Matching results with matched and unmatched items
    """
    # Validate inputs
    if not isinstance(transactions, list) or not isinstance(invoices, list):
        raise ValueError("Transactions and invoices must be lists")
    
    matched = []
    unmatched_transactions = []
    unmatched_invoices = invoices.copy()
    
    for transaction in transactions:
        # Validate transaction structure
        if not isinstance(transaction, dict):
            unmatched_transactions.append(transaction)
            continue
            
        match_found = False
        for invoice in unmatched_invoices[:]:  # Create a copy to iterate over
            # Validate invoice structure
            if not isinstance(invoice, dict):
                continue
                
            # Simple matching logic based on amount (in a real system, this would be more complex)
            try:
                transaction_amount = float(transaction.get('amount', 0))
                invoice_amount = float(invoice.get('amount', 0))
                
                if abs(transaction_amount - invoice_amount) < 0.01:  # Allow for floating point differences
                    matched.append({
                        'transaction': transaction,
                        'invoice': invoice,
                        'match_type': 'amount_match',
                        'confidence': 0.9  # High confidence for exact amount matches
                    })
                    unmatched_invoices.remove(invoice)
                    match_found = True
                    break
            except (ValueError, TypeError):
                # If we can't convert amounts to float, skip this comparison
                continue
        
        if not match_found:
            unmatched_transactions.append(transaction)
    
    return {
        'matched': matched,
        'unmatched_transactions': unmatched_transactions,
        'unmatched_invoices': unmatched_invoices,
        'summary': {
            'total_transactions': len(transactions),
            'total_invoices': len(invoices),
            'matched_pairs': len(matched),
            'unmatched_transactions_count': len(unmatched_transactions),
            'unmatched_invoices_count': len(unmatched_invoices),
            'match_rate': len(matched) / len(transactions) if transactions else 0
        }
    }


def validate_data(data: List[Dict], data_type: str) -> Dict[str, Any]:
    """
    Validate financial data formats.
    
    Args:
        data (List[Dict]): List of data dictionaries
        data_type (str): Type of data ('transactions' or 'invoices')
        
    Returns:
        Dict[str, Any]: Validation results
    """
    # Validate inputs
    if not isinstance(data, list):
        return {
            'valid': False,
            'errors': ['Data must be a list'],
            'warnings': []
        }
    
    if data_type not in ['transactions', 'invoices']:
        return {
            'valid': False,
            'errors': [f"Unknown data type: {data_type}"],
            'warnings': []
        }
    
    errors = []
    warnings = []
    
    for i, item in enumerate(data):
        # Validate item structure
        if not isinstance(item, dict):
            errors.append(f"Row {i+1}: Item must be a dictionary")
            continue
            
        if data_type == 'transactions':
            required_fields = ['date', 'amount', 'description', 'account']
        elif data_type == 'invoices':
            required_fields = ['date', 'amount', 'invoice_number', 'vendor']
        else:
            errors.append(f"Row {i+1}: Unknown data type: {data_type}")
            continue
            
        for field in required_fields:
            if field not in item:
                errors.append(f"Row {i+1}: Missing required field '{field}'")
                
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }


def generate_report(matching_results: Dict[str, Any]) -> str:
    """
    Generate a reconciliation report.
    
    Args:
        matching_results (Dict[str, Any]): Results from match_transactions function
        
    Returns:
        str: Formatted report
    """
    # Validate input
    if not isinstance(matching_results, dict):
        return "Error: Invalid matching results format"
    
    report = "Financial Reconciliation Report\n"
    report += "=" * 40 + "\n\n"
    
    # Add summary statistics
    summary = matching_results.get('summary', {})
    if summary:
        report += "Summary:\n"
        report += f"  Total Transactions: {summary.get('total_transactions', 0)}\n"
        report += f"  Total Invoices: {summary.get('total_invoices', 0)}\n"
        report += f"  Matched Pairs: {summary.get('matched_pairs', 0)}\n"
        report += f"  Unmatched Transactions: {summary.get('unmatched_transactions_count', 0)}\n"
        report += f"  Unmatched Invoices: {summary.get('unmatched_invoices_count', 0)}\n"
        match_rate = summary.get('match_rate', 0)
        report += f"  Match Rate: {match_rate:.2%}\n\n"
    
    # Add matched transactions
    matched = matching_results.get('matched', [])
    if matched:
        report += "Matched Transactions:\n"
        for match in matched:
            transaction = match.get('transaction', {})
            invoice = match.get('invoice', {})
            report += f"  - Transaction ({transaction.get('date', 'N/A')}: ${transaction.get('amount', 0)}) "
            report += f"matched with Invoice ({invoice.get('date', 'N/A')}: ${invoice.get('amount', 0)})\n"
        report += "\n"
    
    # Add unmatched transactions
    unmatched_transactions = matching_results.get('unmatched_transactions', [])
    if unmatched_transactions:
        report += "Unmatched Transactions:\n"
        for transaction in unmatched_transactions:
            if isinstance(transaction, dict):
                report += f"  - {transaction.get('date', 'N/A')}: ${transaction.get('amount', 0)} ({transaction.get('description', 'No description')})\n"
            else:
                report += f"  - Invalid transaction format: {transaction}\n"
        report += "\n"
        
    # Add unmatched invoices
    unmatched_invoices = matching_results.get('unmatched_invoices', [])
    if unmatched_invoices:
        report += "Unmatched Invoices:\n"
        for invoice in unmatched_invoices:
            if isinstance(invoice, dict):
                report += f"  - {invoice.get('date', 'N/A')}: ${invoice.get('amount', 0)} ({invoice.get('invoice_number', 'No number')})\n"
            else:
                report += f"  - Invalid invoice format: {invoice}\n"
        report += "\n"
        
    return report


def save_matching_results(results: Dict[str, Any], file_path: str) -> None:
    """
    Save matching results to a JSON file.
    
    Args:
        results (Dict[str, Any]): Matching results
        file_path (str): Path to save the results
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Save results
    with open(file_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)