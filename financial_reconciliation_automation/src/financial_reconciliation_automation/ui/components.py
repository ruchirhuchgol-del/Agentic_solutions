"""
Reusable UI components for the Financial Reconciliation Automation app.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def metric_card(title, value, delta=None, delta_color="normal"):
    """Render a styled metric card"""
    # Define color mapping for delta
    color_mapping = {
        "normal": "#666666",
        "inverse": "red" if delta and (isinstance(delta, str) and delta.startswith('-')) or (isinstance(delta, (int, float)) and delta < 0) else "green",
        "off": "#666666"
    }
    color = color_mapping.get(delta_color, "#666666")
    
    delta_html = f'<p style="color: {color}; font-size: 1rem; font-weight: 500; margin: 0;">{delta}</p>' if delta else ''
    
    st.markdown(f"""
    <div class="metric-card">
        <h3>{title}</h3>
        <h2>{value}</h2>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def discrepancy_chart(data):
    """Render a discrepancy analysis chart"""
    if data is not None and not data.empty:
        # Ensure the required columns exist
        if 'category' in data.columns and 'count' in data.columns:
            fig = px.bar(
                data, 
                x='category', 
                y='count', 
                color='status' if 'status' in data.columns else None,
                title='Discrepancy Analysis'
            )
            fig.update_layout(
                xaxis_title="Discrepancy Type",
                yaxis_title="Count",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Insufficient data for discrepancy chart")
    else:
        st.info("No discrepancy data available")

def trend_chart(data):
    """Render a trend analysis chart"""
    if data is not None and not data.empty:
        # Check for required columns
        if 'date' in data.columns:
            # If we have match_rate column, use it
            if 'match_rate' in data.columns:
                fig = px.line(
                    data, 
                    x='date', 
                    y='match_rate', 
                    title='Reconciliation Trend Analysis',
                    markers=True
                )
                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Match Rate (%)",
                    yaxis=dict(tickformat=".1f"),
                    height=400
                )
            # If we have value column, use it
            elif 'value' in data.columns:
                fig = px.line(
                    data, 
                    x='date', 
                    y='value', 
                    title='Reconciliation Trend Analysis',
                    markers=True
                )
                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Value",
                    height=400
                )
            else:
                st.info("Insufficient data for trend chart")
                return
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Date column not found in trend data")
    else:
        st.info("No trend data available")

def data_preview(data, title, max_rows=10):
    """Display a preview of data in a dataframe."""
    st.subheader(title)
    if isinstance(data, pd.DataFrame):
        st.dataframe(data.head(max_rows), width='stretch')
    else:
        st.write(data)

def discrepancy_table(discrepancies_df):
    """Display discrepancies in a formatted table."""
    st.subheader("Discrepancy Details")
    if isinstance(discrepancies_df, pd.DataFrame):
        st.dataframe(discrepancies_df, width='stretch')
    else:
        st.write(discrepancies_df)

def dual_axis_trend_chart(data, x_col, y1_col, y2_col, title):
    """Display a trend chart with dual y-axes."""
    st.subheader(title)
    
    if isinstance(data, pd.DataFrame) and all(col in data.columns for col in [x_col, y1_col, y2_col]):
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data[x_col],
            y=data[y1_col],
            mode='lines+markers',
            name=y1_col,
            line=dict(color='green', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=data[x_col],
            y=data[y2_col],
            mode='lines+markers',
            name=y2_col,
            yaxis='y2',
            line=dict(color='red', width=3)
        ))
        
        fig.update_layout(
            title=title,
            xaxis=dict(title=x_col),
            yaxis=dict(title=y1_col, side="left"),
            yaxis2=dict(title=y2_col, overlaying="y", side="right"),
            legend=dict(x=0.1, y=0.9),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Insufficient data for dual axis chart")

def status_pie_chart(data, category_col, title):
    """Display a pie chart of status distribution."""
    st.subheader(title)
    if isinstance(data, pd.DataFrame) and category_col in data.columns:
        status_counts = data[category_col].value_counts().reset_index()
        status_counts.columns = [category_col, 'count']
        fig = px.pie(status_counts, values='count', names=category_col, title=title)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Insufficient data for pie chart")

def report_list(reports):
    """Display a list of reports with download buttons."""
    st.subheader("Generated Reports")
    
    if reports and isinstance(reports, list):
        for report in reports:
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            with col1:
                st.write(report.get("name", "Unknown Report"))
            with col2:
                st.write(report.get("date", "Unknown Date"))
            with col3:
                st.write(report.get("type", "Unknown Type"))
            with col4:
                st.download_button(
                    label="Download",
                    data=report.get("content", "Sample content"),
                    file_name=f"{report.get('name', 'report').replace(' ', '_')}.{report.get('type', 'txt').lower()}",
                    mime="application/octet-stream"
                )
    else:
        st.info("No reports available")

def log_viewer(logs):
    """Display execution logs."""
    with st.expander("Execution Logs"):
        if logs and isinstance(logs, list):
            for log in logs:
                st.text(log)
            
            # Download logs
            logs_text = "\n".join(logs)
            st.download_button(
                label="Download Logs",
                data=logs_text,
                file_name=f"reconciliation_logs_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        else:
            st.info("No logs available")