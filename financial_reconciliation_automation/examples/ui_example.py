"""
Example script demonstrating how to use the UI components directly.
"""

import streamlit as st
import pandas as pd
import sys
import os

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from financial_reconciliation_automation.ui.components import metric_card, discrepancy_chart, trend_chart
from financial_reconciliation_automation.ui.utils import load_sample_data, generate_report

def main():
    st.title("Financial Reconciliation UI Components Example")
    
    # Load sample data
    transactions, invoices = load_sample_data()
    
    if transactions is not None and invoices is not None:
        st.success("Sample data loaded successfully!")
        
        # Display metrics
        st.header("Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            metric_card("Total Transactions", len(transactions))
        with col2:
            metric_card("Total Invoices", len(invoices))
        with col3:
            metric_card("Match Rate", "94.2%", "2.1%")
        with col4:
            metric_card("Processing Time", "1m 45s")
        
        # Display charts
        st.header("Data Visualization")
        
        # Sample discrepancy data
        discrepancy_data = pd.DataFrame({
            'category': ['Amount Mismatch', 'Date Mismatch', 'Missing Records', 'Duplicate Entries'],
            'count': [12, 8, 5, 3],
            'status': ['High', 'Medium', 'High', 'Low']
        })
        
        # Sample trend data
        trend_data = pd.DataFrame({
            'date': pd.date_range(start='2024-01-01', periods=30),
            'value': [85 + i*0.3 + (i % 4) for i in range(30)]
        })
        
        col1, col2 = st.columns(2)
        with col1:
            discrepancy_chart(discrepancy_data)
        with col2:
            trend_chart(trend_data)
            
        # Display sample data
        st.header("Sample Data Preview")
        tab1, tab2 = st.tabs(["Transactions", "Invoices"])
        
        with tab1:
            st.dataframe(transactions.head(10), use_container_width=True)
            
        with tab2:
            st.dataframe(invoices.head(10), use_container_width=True)
            
    else:
        st.error("Could not load sample data. Please check that the data files exist.")

if __name__ == "__main__":
    main()