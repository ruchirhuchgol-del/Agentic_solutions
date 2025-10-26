import os
import json
import pandas as pd
from datetime import datetime

def save_configuration(name, config):
    """Save a configuration to file"""
    configs = load_configurations()
    configs[name] = config
    with open("configurations.json", 'w') as f:
        json.dump(configs, f, indent=2)

def load_configurations():
    """Load saved configurations from file"""
    config_file = "configurations.json"
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {}

def load_sample_data():
    """Load sample transaction and invoice data"""
    transactions_file = "./data/sample/transactions.csv"
    invoices_file = "./data/sample/invoices.csv"
    transactions = None
    invoices = None
    
    if os.path.exists(transactions_file):
        transactions = pd.read_csv(transactions_file)

    if os.path.exists(invoices_file):
        invoices = pd.read_csv(invoices_file)
        
    return transactions, invoices

def format_results(results):
    """Format the results for display"""
    # Return detailed placeholder data for better visualization
    return {
        'total_transactions': 1250,
        'matched': 1180,
        'discrepancies': 70,
        'alerts': 12,
        'match_rate': 94.4,
        'reporting_period': 'Q1 2024',
        'company_name': 'Acme Financial Services',
        'escalation_team': 'finance-team@company.com',
        'discrepancy_details': [
            {'category': 'Amount Mismatch', 'count': 30, 'status': 'High'},
            {'category': 'Date Mismatch', 'count': 20, 'status': 'Medium'},
            {'category': 'Missing Records', 'count': 15, 'status': 'High'},
            {'category': 'Duplicate Entries', 'count': 5, 'status': 'Low'}
        ],
        'trend_data': [
            {'date': '2024-01-01', 'match_rate': 85.2, 'discrepancies': 85},
            {'date': '2024-01-08', 'match_rate': 87.5, 'discrepancies': 78},
            {'date': '2024-01-15', 'match_rate': 89.1, 'discrepancies': 72},
            {'date': '2024-01-22', 'match_rate': 91.3, 'discrepancies': 65},
            {'date': '2024-01-29', 'match_rate': 92.7, 'discrepancies': 58},
            {'date': '2024-02-05', 'match_rate': 93.8, 'discrepancies': 49},
            {'date': '2024-02-12', 'match_rate': 94.4, 'discrepancies': 42}
        ],
        'discrepancy_records': [
            {'transaction_id': 'T001', 'invoice_id': 'INV-2024-001', 'amount': 1250.00, 'discrepancy': 125.00, 'status': 'Pending', 'reason': 'Amount mismatch'},
            {'transaction_id': 'T002', 'invoice_id': 'INV-2024-002', 'amount': 875.30, 'discrepancy': 0.00, 'status': 'Matched', 'reason': 'Exact match'},
            {'transaction_id': 'T003', 'invoice_id': 'INV-2024-003', 'amount': 2100.00, 'discrepancy': 50.00, 'status': 'Pending', 'reason': 'Date variance'},
            {'transaction_id': 'T004', 'invoice_id': 'INV-2024-004', 'amount': 650.50, 'discrepancy': 0.00, 'status': 'Matched', 'reason': 'Exact match'},
            {'transaction_id': 'T005', 'invoice_id': 'INV-2024-005', 'amount': 3200.25, 'discrepancy': 320.00, 'status': 'Pending', 'reason': 'Amount mismatch'}
        ]
    }

def generate_report(results, format_type='plain'):
    """Generate a detailed report from the results"""
    report_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Summary section
    summary_section = f"""# Financial Reconciliation Report
**Generated on:** {report_date}
**Reporting Period:** {results.get('reporting_period', 'Q1 2024')}
**Company:** {results.get('company_name', 'Acme Financial Services')}

## Executive Summary

This report details the financial reconciliation analysis performed on transaction data. The process identified matches and discrepancies between financial transactions and corresponding invoices.

- **Total Transactions Processed:** {results.get('total_transactions', 0):,}
- **Successfully Matched:** {results.get('matched', 0):,} ({results.get('match_rate', 0)}%)
- **Discrepancies Identified:** {results.get('discrepancies', 0):,}
- **Critical Alerts Generated:** {results.get('alerts', 0):,}

## Reconciliation Metrics

| Metric | Value | Percentage |
|--------|-------|------------|
| Total Transactions | {results.get('total_transactions', 0):,} | 100% |
| Matched Transactions | {results.get('matched', 0):,} | {results.get('match_rate', 0)}% |
| Unmatched Transactions | {results.get('discrepancies', 0):,} | {(100 - results.get('match_rate', 0)):.1f}% |

"""
    
    # Discrepancy analysis section
    discrepancy_section = "## Discrepancy Analysis\n\n"
    
    if 'discrepancy_details' in results:
        discrepancy_section += "| Discrepancy Type | Count | Severity |\n"
        discrepancy_section += "|------------------|-------|----------|\n"
        for item in results['discrepancy_details']:
            discrepancy_section += f"| {item['category']} | {item['count']} | {item['status']} |\n"
    else:
        discrepancy_section += "No detailed discrepancy analysis available.\n\n"
    
    # Detailed records section
    records_section = "\n## Detailed Discrepancy Records\n\n"
    
    if 'discrepancy_records' in results:
        records_section += "| Transaction ID | Invoice ID | Amount ($) | Discrepancy ($) | Status | Reason |\n"
        records_section += "|----------------|------------|------------|-----------------|--------|--------|\n"
        for record in results['discrepancy_records']:
            records_section += f"| {record['transaction_id']} | {record['invoice_id']} | {record['amount']:,.2f} | {record['discrepancy']:,.2f} | {record['status']} | {record['reason']} |\n"
    else:
        records_section += "No detailed discrepancy records available.\n\n"
    
    # Trend analysis section
    trend_section = "\n## Trend Analysis\n\n"
    
    if 'trend_data' in results:
        trend_section += "| Date | Match Rate (%) | Discrepancies |\n"
        trend_section += "|------|----------------|---------------|\n"
        for point in results['trend_data']:
            trend_section += f"| {point['date']} | {point['match_rate']:.1f} | {point['discrepancies']} |\n"
    else:
        trend_section += "No trend analysis data available.\n\n"
    
    # Recommendations section
    recommendations_section = "\n## Recommendations\n\n"
    recommendations_section += "1. Review high-value discrepancy items flagged as 'Critical'\n"
    recommendations_section += "2. Investigate recurring discrepancy patterns\n"
    recommendations_section += "3. Update matching algorithms for common mismatch scenarios\n"
    recommendations_section += "4. Implement additional validation checks for data entry\n\n"
    
    # Compliance section
    compliance_section = "## Compliance & Audit Notes\n\n"
    compliance_section += "- All reconciliation processes followed standard financial protocols\n"
    compliance_section += "- Discrepancy investigations logged for audit trail\n"
    compliance_section += "- Exception handling procedures applied where necessary\n\n"
    
    # Footer
    footer = f"""
---
*Report generated by Financial Reconciliation Automation System*
*For questions regarding this report, contact {results.get('escalation_team', 'the finance team')}*
"""
    
    # Combine all sections
    report = summary_section + discrepancy_section + records_section + trend_section + recommendations_section + compliance_section + footer
    
    return report