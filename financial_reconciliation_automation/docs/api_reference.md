# API Reference

## Core Modules

### main.py
Entry point for the application.

Functions:
- `main()`: Initializes and runs the financial reconciliation crew.

### crew.py
Defines the CrewAI agents and tasks.

Classes:
- `FinancialReconciliationCrew`: Main crew class that orchestrates the reconciliation process.

## Tools

### financial_tools.py
Custom financial tools for transaction processing.

Functions:
- `match_transactions()`: Matches transactions with invoices.
- `validate_data()`: Validates financial data formats.
- `generate_report()`: Generates reconciliation reports.

### langchain_tools.py
LangChain-integrated tools for enhanced AI capabilities.

Functions:
- `analyze_discrepancies()`: Uses LLM to analyze discrepancies.
- `categorize_transactions()`: Categorizes transactions using AI.

## Chains

### validation_chain.py
Data validation chains using LangChain.

### matching_chain.py
Transaction matching chains using LangChain.

### reporting_chain.py
Report generation chains using LangChain.