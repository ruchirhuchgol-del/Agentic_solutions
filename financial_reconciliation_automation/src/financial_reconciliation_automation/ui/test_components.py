"""
Test script for UI components.
"""

import streamlit as st
import pandas as pd
from financial_reconciliation_automation.ui.components import metric_card, discrepancy_chart, trend_chart

def test_components():
    """Test UI components."""
    st.title("UI Components Test")
    
    # Test metric card
    st.header("Metric Card Component")
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Total Transactions", "1,250", "5.2%", "normal")
    with col2:
        metric_card("Discrepancies", "70", "-3", "inverse")
    with col3:
        metric_card("Processing Time", "2m 34s")
    
    # Test discrepancy chart
    st.header("Discrepancy Chart Component")
    discrepancy_data = pd.DataFrame({
        'category': ['Amount Mismatch', 'Date Mismatch', 'Missing Records', 'Duplicate Entries'],
        'count': [30, 20, 15, 5],
        'status': ['High', 'Medium', 'High', 'Low']
    })
    discrepancy_chart(discrepancy_data)
    
    # Test trend chart
    st.header("Trend Chart Component")
    trend_data = pd.DataFrame({
        'date': pd.date_range(start='2024-01-01', periods=30),
        'value': [90 + i*0.2 + (i % 5) for i in range(30)]
    })
    trend_chart(trend_data)

if __name__ == "__main__":
    test_components()