import streamlit as st
import os
import sys
import pandas as pd
from datetime import datetime

# Add the project root to the path so we can import the crew
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from financial_reconciliation_automation.ui.components import metric_card, discrepancy_chart, trend_chart
from financial_reconciliation_automation.ui.utils import load_configurations, save_configuration, load_sample_data, format_results, generate_report

# Page configuration
st.set_page_config(
    page_title="Financial Reconciliation Automation",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Header Styling */
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }

    /* Center the Tabs */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
    }

    /* Metric Card Base */
    .metric-card {
        background-color: #ffffff;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;

        /* Uniform sizing and layout */
        width: 100%;
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;

        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    /* Optional hover effect for interactivity */
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }

    /* Title Text */
    .metric-card h3 {
        margin: 0;
        font-size: 1.1rem;
        font-weight: 600;
        color: #555;
    }

    /* Metric Value */
    .metric-card h2 {
        margin: 0.3rem 0;
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E88E5;
        line-height: 1.2;
    }

    /* Subtitle or Description */
    .metric-card p {
        margin: 0;
        font-size: 0.95rem;
        font-weight: 500;
        color: #666;
    }

    /* Make cards consistent across columns */
    [data-testid="column"] > div {
        display: flex;
        justify-content: center;
    }

    /* Keep cards the same size in multi-column layouts */
    [data-testid="column"] .metric-card {
        width: 90%;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'running' not in st.session_state:
    st.session_state.running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'configurations' not in st.session_state:
    st.session_state.configurations = load_configurations()

def main():
    # Main header
    st.markdown('<h1 class="main-header">Financial Reconciliation Automation</h1>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Configuration selection
        config_names = ["Default"] + list(st.session_state.configurations.keys())
        selected_config = st.selectbox("Select Configuration", config_names)
        
        # Load configuration
        if selected_config == "Default":
            config = {
                'data_source': './data/sample/transactions.csv',
                'reporting_system': 'Google Sheets',
                'alert_threshold': 1000,
                'invoice_source': './data/sample/invoices.csv',
                'reporting_period': 'Q1 2024',
                'company_name': 'Acme Financial Services',
                'escalation_team': 'finance-team@company.com',
                'date_tolerance': 3,
                'analysis_period': '6 months'
            }
        else:
            config = st.session_state.configurations[selected_config]
        
        # Configuration form
        with st.form("config_form"):
            st.subheader("Reconciliation Parameters")
            
            config['data_source'] = st.text_input(
                "Data Source (CSV)", 
                value=config.get('data_source', './data/sample/transactions.csv')
            )
            config['invoice_source'] = st.text_input(
                "Invoice Source (CSV)", 
                value=config.get('invoice_source', './data/sample/invoices.csv')
            )
            config['alert_threshold'] = st.number_input(
                "Alert Threshold ($)", 
                value=float(config.get('alert_threshold', 1000)),
                min_value=0.0,
                step=100.0
            )
            config['date_tolerance'] = st.number_input(
                "Date Tolerance (days)", 
                value=int(config.get('date_tolerance', 3)),
                min_value=0,
                step=1
            )
            config['company_name'] = st.text_input(
                "Company Name", 
                value=config.get('company_name', 'Acme Financial Services')
            )
            config['escalation_team'] = st.text_input(
                "Escalation Team Email", 
                value=config.get('escalation_team', 'finance-team@company.com')
            )
            config['reporting_system'] = st.selectbox(
                "Reporting System", 
                options=["Google Sheets", "Local File", "Database"],
                index=0
            )
            config['reporting_period'] = st.text_input(
                "Reporting Period", 
                value=config.get('reporting_period', 'Q1 2024')
            )
            config['analysis_period'] = st.text_input(
                "Analysis Period", 
                value=config.get('analysis_period', '6 months')
            )
            
            # Save configuration option
            save_name = st.text_input("Save as new configuration")
            
            # Submit button
            submitted = st.form_submit_button("Run Reconciliation")
            if submitted:
                if save_name:
                    save_configuration(save_name, config)
                    st.success(f"Configuration '{save_name}' saved!")
                
                # Simulate running reconciliation with improved data
                st.session_state.running = True
                st.session_state.logs = [f"Starting reconciliation at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]
                st.session_state.logs.append("Loading data...")
                st.session_state.logs.append("Processing transactions...")
                st.session_state.logs.append("Matching with invoices...")
                st.session_state.logs.append("Generating report...")
                st.session_state.logs.append(f"Reconciliation completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                st.session_state.results = format_results({})
                st.session_state.running = False
    
    # Main content area
    if st.session_state.running:
        st.info("Reconciliation in progress...")
        with st.expander("View Logs"):
            for log in st.session_state.logs:
                st.text(log)
    
    elif st.session_state.results:
        # Display results
        st.header("Reconciliation Results")
        
        # Summary metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            metric_card("Total Transactions", f"{st.session_state.results['total_transactions']:,}")
            
        with col2:
            metric_card("Matched", f"{st.session_state.results['matched']:,}", f"{st.session_state.results['match_rate']}%")
            
        with col3:
            metric_card("Discrepancies", f"{st.session_state.results['discrepancies']:,}", None, delta_color="inverse")
            
        with col4:
            metric_card("Alerts", f"{st.session_state.results['alerts']:,}", None, delta_color="inverse")
            
        with col5:
            metric_card("Match Rate", f"{st.session_state.results['match_rate']}%")
        
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["Summary", "Discrepancies", "Reports"])
        
        with tab1:
            st.subheader("Reconciliation Summary")
            
            # Prepare chart data from results
            if 'discrepancy_details' in st.session_state.results:
                discrepancy_data = pd.DataFrame(st.session_state.results['discrepancy_details'])
            else:
                # Fallback to sample data
                discrepancy_data = pd.DataFrame({
                    'category': ['Amount Mismatch', 'Date Mismatch', 'Missing Records', 'Duplicate Entries'],
                    'count': [30, 20, 15, 5],
                    'status': ['High', 'Medium', 'High', 'Low']
                })
            
            if 'trend_data' in st.session_state.results:
                trend_data = pd.DataFrame(st.session_state.results['trend_data'])
            else:
                # Fallback to sample data
                trend_data = pd.DataFrame({
                    'date': pd.date_range(start='2024-01-01', periods=30),
                    'value': [90 + i*0.2 + (i % 5) for i in range(30)]
                })
            
            # Display charts
            col1, col2 = st.columns(2)
            with col1:
                discrepancy_chart(discrepancy_data)
            with col2:
                trend_chart(trend_data)
        
        with tab2:
            st.subheader("Discrepancy Details")
            
            # Display discrepancy records
            if 'discrepancy_records' in st.session_state.results:
                discrepancy_df = pd.DataFrame(st.session_state.results['discrepancy_records'])
                st.dataframe(discrepancy_df, width='stretch')
            else:
                # Sample discrepancy table
                discrepancy_table = pd.DataFrame({
                    'Transaction ID': ['T001', 'T002', 'T003', 'T004', 'T005'],
                    'Invoice ID': ['INV-2024-001', 'INV-2024-002', 'INV-2024-003', 'INV-2024-004', 'INV-2024-005'],
                    'Amount': ['$1,250.00', '$875.30', '$2,100.00', '$650.50', '$3,200.25'],
                    'Discrepancy': ['$125.00', '$0.00', '$50.00', '$0.00', '$320.00'],
                    'Status': ['Pending', 'Matched', 'Pending', 'Matched', 'Pending']
                })
                
                st.dataframe(discrepancy_table, width='stretch')
        
        with tab3:
            st.subheader("Generated Reports")
            
            # Generate and display report
            report = generate_report(st.session_state.results)
            st.markdown(report)
            
            # Create columns for download buttons
            col1, col2 = st.columns(2)
            
            with col1:
                # Download report as markdown
                st.download_button(
                    label="Download Detailed Report (Markdown)",
                    data=report,
                    file_name=f"reconciliation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )
            
            with col2:
                # Download report as text
                st.download_button(
                    label="Download Detailed Report (Text)",
                    data=report,
                    file_name=f"reconciliation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
            
            # Additional download options
            st.subheader("Additional Data Downloads")
            
            # Download discrepancy records as CSV
            if 'discrepancy_records' in st.session_state.results:
                df = pd.DataFrame(st.session_state.results['discrepancy_records'])
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Discrepancy Records (CSV)",
                    data=csv,
                    file_name=f"discrepancy_records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            # Download discrepancy details as CSV
            if 'discrepancy_details' in st.session_state.results:
                df = pd.DataFrame(st.session_state.results['discrepancy_details'])
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Discrepancy Details (CSV)",
                    data=csv,
                    file_name=f"discrepancy_details_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            # Download trend data as CSV
            if 'trend_data' in st.session_state.results:
                df = pd.DataFrame(st.session_state.results['trend_data'])
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Trend Data (CSV)",
                    data=csv,
                    file_name=f"trend_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            # Logs section
            with st.expander("Execution Logs"):
                for log in st.session_state.logs:
                    st.text(log)
                
                # Download logs
                if st.session_state.logs:
                    logs_text = "\n".join(st.session_state.logs)
                    st.download_button(
                        label="Download Logs",
                        data=logs_text,
                        file_name=f"reconciliation_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
    
    else:
        # Initial state
        st.info("Configure your reconciliation parameters in the sidebar and click 'Run Reconciliation' to begin.")
        
        # Sample data preview
        st.subheader("Sample Data Preview")
        transactions, invoices = load_sample_data()
        
        if transactions is not None and invoices is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("Transactions:")
                st.dataframe(transactions.head(), width='stretch')
            
            with col2:
                st.write("Invoices:")
                st.dataframe(invoices.head(), width='stretch')
        else:
            st.warning("Sample data not found. Please ensure the data directory exists and contains sample CSV files.")

if __name__ == "__main__":
    main()