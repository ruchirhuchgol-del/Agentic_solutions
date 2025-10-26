# Setup Instructions

## Prerequisites

- Python 3.9 or higher
- pip package manager

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd financial_reconciliation_automation
   ```

3. Install dependencies using Poetry:
   ```
   poetry install
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your API keys

## Running the Application

```
poetry run python src/financial_reconciliation_automation/main.py
```