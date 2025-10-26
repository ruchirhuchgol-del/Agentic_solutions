"""
Data loading utilities for the financial reconciliation automation system.
"""

import pandas as pd
import os
from typing import List, Dict, Any

def load_csv_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Load data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        List[Dict[str, Any]]: List of dictionaries representing the CSV data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        pd.errors.EmptyDataError: If the file is empty
        pd.errors.ParserError: If the file can't be parsed
    """
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    try:
        # Load CSV data
        df = pd.read_csv(file_path)
        
        # Convert to list of dictionaries
        return df.to_dict('records')
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError(f"CSV file is empty: {file_path}")
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError(f"Error parsing CSV file {file_path}: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error loading CSV file {file_path}: {str(e)}")


def save_csv_data(data: List[Dict[str, Any]], file_path: str) -> None:
    """
    Save data to a CSV file.
    
    Args:
        data (List[Dict[str, Any]]): Data to save
        file_path (str): Path to the output CSV file
        
    Raises:
        Exception: If there's an error saving the file
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Convert to DataFrame and save
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
    except Exception as e:
        raise Exception(f"Error saving data to CSV file {file_path}: {str(e)}")


def load_sample_data(data_type: str) -> List[Dict[str, Any]]:
    """
    Load sample data for testing.
    
    Args:
        data_type (str): Type of data to load ('transactions' or 'invoices')
        
    Returns:
        List[Dict[str, Any]]: Sample data
        
    Raises:
        ValueError: If data_type is invalid
        FileNotFoundError: If sample data files don't exist
    """
    sample_dir = "data/sample"
    
    if data_type == "transactions":
        file_path = os.path.join(sample_dir, "transactions.csv")
    elif data_type == "invoices":
        file_path = os.path.join(sample_dir, "invoices.csv")
    else:
        raise ValueError(f"Unknown data type: {data_type}")
        
    return load_csv_data(file_path)


def create_sample_data() -> None:
    """
    Create sample data files for testing.
    """
    # Sample transactions
    transactions = [
        {"date": "2023-01-01", "amount": 100.00, "description": "Office supplies", "account": "Expense"},
        {"date": "2023-01-02", "amount": 250.00, "description": "Software subscription", "account": "Expense"},
        {"date": "2023-01-03", "amount": 1000.00, "description": "Consulting services", "account": "Expense"},
    ]
    
    # Sample invoices
    invoices = [
        {"date": "2023-01-01", "amount": 100.00, "invoice_number": "INV-001", "vendor": "Office Supply Co"},
        {"date": "2023-01-02", "amount": 250.00, "invoice_number": "INV-002", "vendor": "Software Inc"},
        {"date": "2023-01-03", "amount": 1000.00, "invoice_number": "INV-003", "vendor": "Consulting Group"},
    ]
    
    # Save sample data
    sample_dir = "data/sample"
    os.makedirs(sample_dir, exist_ok=True)
    
    save_csv_data(transactions, os.path.join(sample_dir, "transactions.csv"))
    save_csv_data(invoices, os.path.join(sample_dir, "invoices.csv"))