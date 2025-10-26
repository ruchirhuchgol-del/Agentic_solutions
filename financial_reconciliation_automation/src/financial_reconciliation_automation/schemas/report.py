"""
Data schemas for financial reports.
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .transaction import Transaction, Invoice, MatchResult


class ReconciliationSummary(BaseModel):
    """Schema for reconciliation summary statistics."""
    total_transactions: int
    total_invoices: int
    matched_pairs: int
    unmatched_transactions: int
    unmatched_invoices: int
    match_rate: float
    total_discrepancy_amount: float


class DiscrepancyItem(BaseModel):
    """Schema for a discrepancy item."""
    id: str
    type: str  # 'transaction' or 'invoice'
    date: str
    amount: float
    description: str
    reason: Optional[str] = None
    suggested_action: Optional[str] = None


class ReconciliationReport(BaseModel):
    """Schema for a complete reconciliation report."""
    report_id: str
    generated_date: datetime
    period_start: str
    period_end: str
    summary: ReconciliationSummary
    matched_results: List[MatchResult]
    unmatched_transactions: List[Transaction]
    unmatched_invoices: List[Invoice]
    discrepancies: List[DiscrepancyItem]
    recommendations: List[str]
    
    class Config:
        # Allow datetime objects to be serialized
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }