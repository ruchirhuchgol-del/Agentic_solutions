"""
Input validation utilities for the financial reconciliation automation system.
"""

from typing import List, Dict, Any
import re


def validate_transaction_data(transactions: List[Dict]) -> Dict[str, Any]:
    """
    Validate transaction data.
    
    Args:
        transactions (List[Dict]): List of transaction dictionaries
        
    Returns:
        Dict[str, Any]: Validation results
    """
    errors = []
    warnings = []
    
    for i, transaction in enumerate(transactions):
        # Check required fields
        required_fields = ['date', 'amount', 'description', 'account']
        for field in required_fields:
            if field not in transaction:
                errors.append(f"Transaction {i+1}: Missing required field '{field}'")
                
        # Validate date format (YYYY-MM-DD)
        if 'date' in transaction:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', transaction['date']):
                errors.append(f"Transaction {i+1}: Invalid date format '{transaction['date']}'. Expected YYYY-MM-DD.")
                
        # Validate amount is numeric
        if 'amount' in transaction:
            try:
                float(transaction['amount'])
            except (ValueError, TypeError):
                errors.append(f"Transaction {i+1}: Amount '{transaction['amount']}' is not a valid number.")
                
        # Check for unusually large amounts
        if 'amount' in transaction:
            try:
                amount = float(transaction['amount'])
                if amount > 100000:
                    warnings.append(f"Transaction {i+1}: Unusually large amount ${amount:,.2f}")
            except (ValueError, TypeError):
                pass  # Error already caught above
                
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }


def validate_invoice_data(invoices: List[Dict]) -> Dict[str, Any]:
    """
    Validate invoice data.
    
    Args:
        invoices (List[Dict]): List of invoice dictionaries
        
    Returns:
        Dict[str, Any]: Validation results
    """
    errors = []
    warnings = []
    
    for i, invoice in enumerate(invoices):
        # Check required fields
        required_fields = ['date', 'amount', 'invoice_number', 'vendor']
        for field in required_fields:
            if field not in invoice:
                errors.append(f"Invoice {i+1}: Missing required field '{field}'")
                
        # Validate date format (YYYY-MM-DD)
        if 'date' in invoice:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', invoice['date']):
                errors.append(f"Invoice {i+1}: Invalid date format '{invoice['date']}'. Expected YYYY-MM-DD.")
                
        # Validate amount is numeric
        if 'amount' in invoice:
            try:
                float(invoice['amount'])
            except (ValueError, TypeError):
                errors.append(f"Invoice {i+1}: Amount '{invoice['amount']}' is not a valid number.")
                
        # Check for unusually large amounts
        if 'amount' in invoice:
            try:
                amount = float(invoice['amount'])
                if amount > 100000:
                    warnings.append(f"Invoice {i+1}: Unusually large amount ${amount:,.2f}")
            except (ValueError, TypeError):
                pass  # Error already caught above
                
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }


def validate_file_paths(file_paths: List[str]) -> Dict[str, Any]:
    """
    Validate that file paths exist.
    
    Args:
        file_paths (List[str]): List of file paths to validate
        
    Returns:
        Dict[str, Any]: Validation results
    """
    import os
    
    errors = []
    
    for file_path in file_paths:
        if not os.path.exists(file_path):
            errors.append(f"File not found: {file_path}")
            
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }