"""
Output formatting utilities for the financial reconciliation automation system.
"""

import json
from typing import Dict, List


def format_matching_results_as_json(results: Dict) -> str:
    """
    Format matching results as JSON.
    
    Args:
        results (Dict): Matching results
        
    Returns:
        str: JSON formatted results
    """
    return json.dumps(results, indent=2)


def format_matching_results_as_text(results: Dict) -> str:
    """
    Format matching results as human-readable text.
    
    Args:
        results (Dict): Matching results
        
    Returns:
        str: Text formatted results
    """
    output = "Financial Reconciliation Results\n"
    output += "=" * 40 + "\n\n"
    
    output += f"Matched Pairs: {len(results.get('matched', []))}\n"
    output += f"Unmatched Transactions: {len(results.get('unmatched_transactions', []))}\n"
    output += f"Unmatched Invoices: {len(results.get('unmatched_invoices', []))}\n\n"
    
    if results.get('matched'):
        output += "Matched Transactions:\n"
        for match in results['matched']:
            transaction = match['transaction']
            invoice = match['invoice']
            output += f"  - Transaction ({transaction['date']}: ${transaction['amount']}) "
            output += f"matched with Invoice ({invoice['date']}: ${invoice['amount']})\n"
        output += "\n"
    
    if results.get('unmatched_transactions'):
        output += "Unmatched Transactions:\n"
        for transaction in results['unmatched_transactions']:
            output += f"  - {transaction['date']}: ${transaction['amount']} ({transaction['description']})\n"
        output += "\n"
    
    if results.get('unmatched_invoices'):
        output += "Unmatched Invoices:\n"
        for invoice in results['unmatched_invoices']:
            output += f"  - {invoice['date']}: ${invoice['amount']} ({invoice['invoice_number']})\n"
        output += "\n"
    
    return output


def format_report_as_text(report_data: Dict) -> str:
    """
    Format report data as human-readable text.
    
    Args:
        report_data (Dict): Report data
        
    Returns:
        str: Text formatted report
    """
    output = "Financial Reconciliation Report\n"
    output += "=" * 40 + "\n\n"
    
    for key, value in report_data.items():
        output += f"{key.replace('_', ' ').title()}: {value}\n"
    
    return output


def format_discrepancies_as_text(discrepancies: List[Dict]) -> str:
    """
    Format discrepancies as human-readable text.
    
    Args:
        discrepancies (List[Dict]): List of discrepancy dictionaries
        
    Returns:
        str: Text formatted discrepancies
    """
    if not discrepancies:
        return "No discrepancies found.\n"
    
    output = "Identified Discrepancies:\n"
    output += "-" * 25 + "\n\n"
    
    for i, discrepancy in enumerate(discrepancies, 1):
        output += f"{i}. {discrepancy.get('description', 'Unnamed discrepancy')}\n"
        output += f"   Amount: ${discrepancy.get('amount', 0.0)}\n"
        output += f"   Date: {discrepancy.get('date', 'N/A')}\n"
        output += f"   Status: {discrepancy.get('status', 'Unknown')}\n"
        output += f"   Notes: {discrepancy.get('notes', 'No notes')}\n\n"
    
    return output