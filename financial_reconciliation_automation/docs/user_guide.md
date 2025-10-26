# User Guide

## Getting Started

1. Prepare your data:
   - Place transaction data in `data/sample/transactions.csv`
   - Place invoice data in `data/sample/invoices.csv`

2. Configure the system:
   - Adjust agent configurations in `src/financial_reconciliation_automation/config/agents.yaml`
   - Modify task configurations in `src/financial_reconciliation_automation/config/tasks.yaml`

3. Run the application:
   ```
   poetry run python src/financial_reconciliation_automation/main.py
   ```

## Output

Results will be saved in the `data/processed/` directory:
- Reports: `data/processed/reports/`
- Logs: `data/processed/logs/`
- Exports: `data/processed/exports/`

## Customization

### Adding New Agents
Modify `src/financial_reconciliation_automation/config/agents.yaml` to add new agents.

### Adding New Tasks
Modify `src/financial_reconciliation_automation/config/tasks.yaml` to add new tasks.

### Extending Tools
Add new tools in the `src/financial_reconciliation_automation/tools/` directory.