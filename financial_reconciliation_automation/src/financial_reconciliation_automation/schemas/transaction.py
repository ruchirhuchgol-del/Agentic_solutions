"""
Data schemas for financial transactions.
"""

from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class Transaction(BaseModel):
    """Schema for a financial transaction."""
    date: str
    amount: float
    description: str
    account: str
    category: Optional[str] = None
    vendor: Optional[str] = None
    
    @validator('date')
    def validate_date_format(cls, v):
        """Validate that date is in YYYY-MM-DD format."""
        if not isinstance(v, str):
            raise ValueError('Date must be a string')
            
        # Check if date matches YYYY-MM-DD format
        if not len(v) == 10 or v[4] != '-' or v[7] != '-':
            raise ValueError('Date must be in YYYY-MM-DD format')
            
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Invalid date value')
            
        return v
    
    @validator('amount')
    def validate_amount(cls, v):
        """Validate that amount is positive."""
        if v < 0:
            raise ValueError('Amount must be positive')
        return v


class Invoice(BaseModel):
    """Schema for a financial invoice."""
    date: str
    amount: float
    invoice_number: str
    vendor: str
    description: Optional[str] = None
    category: Optional[str] = None
    
    @validator('date')
    def validate_date_format(cls, v):
        """Validate that date is in YYYY-MM-DD format."""
        if not isinstance(v, str):
            raise ValueError('Date must be a string')
            
        # Check if date matches YYYY-MM-DD format
        if not len(v) == 10 or v[4] != '-' or v[7] != '-':
            raise ValueError('Date must be in YYYY-MM-DD format')
            
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Invalid date value')
            
        return v
    
    @validator('amount')
    def validate_amount(cls, v):
        """Validate that amount is positive."""
        if v < 0:
            raise ValueError('Amount must be positive')
        return v


class MatchResult(BaseModel):
    """Schema for a transaction-invoice match result."""
    transaction: Transaction
    invoice: Invoice
    confidence_score: float
    match_date: str
    
    @validator('confidence_score')
    def validate_confidence_score(cls, v):
        """Validate that confidence score is between 0 and 1."""
        if not 0 <= v <= 1:
            raise ValueError('Confidence score must be between 0 and 1')
        return v