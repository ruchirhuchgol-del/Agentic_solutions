"""
Test script for UI components.
"""

import streamlit as st
import sys
import os

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from financial_reconciliation_automation.ui.components import *
from financial_reconciliation_automation.ui.utils import *

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
    
    # Test data preview
    st.header("Data Preview Component")
    sample_data = generate_sample_discrepancies()
    data_preview(sample_data, "Sample Discrepancies")
    
    # Test discrepancy table
    st.header("Discrepancy Table Component")
    discrepancy_table(sample_data)
    
    # Test charts
    st.header("Chart Components")
    trend_data = generate_trend_data()
    
    col1, col2 = st.columns(2)
    with col1:
        trend_chart(trend_data, 'Date', 'Match Rate', 'Match Rate Trend')
    with col2:
        dual_axis_trend_chart(trend_data, 'Date', 'Match Rate', 'Discrepancies', 'Match Rate vs Discrepancies')
    
    # Test pie chart
    st.header("Status Distribution")
    status_pie_chart(sample_data, 'Status', 'Discrepancy Status Distribution')
    
    # Test report list
    st.header("Report List Component")
    reports = [
        {"name": "Reconciliation Summary", "date": "2024-01-15", "type": "PDF"},
        {"name": "Discrepancy Report", "date": "2024-01-15", "type": "Excel"},
    ]
    report_list(reports)
    
    # Test log viewer
    st.header("Log Viewer Component")
    sample_logs = [
        "2024-01-15 10:30:15 - Starting reconciliation process",
        "2024-01-15 10:30:16 - Loading data from CSV files",
        "2024-01-15 10:30:20 - Data validation completed",
        "2024-01-15 10:30:45 - Matching transactions with invoices",
        "2024-01-15 10:32:30 - Reconciliation completed successfully"
    ]
    log_viewer(sample_logs)

if __name__ == "__main__":
    test_components()