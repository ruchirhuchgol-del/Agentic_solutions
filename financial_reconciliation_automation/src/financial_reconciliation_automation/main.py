#!/usr/bin/env python
import sys
import os
import subprocess
from dotenv import load_dotenv

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from financial_reconciliation_automation.crew import FinancialReconciliationCrew

# Load environment variables
load_dotenv()

def validate_inputs(inputs):
    """Validate that all required inputs are provided"""
    required_fields = [
        'data_source', 'reporting_system', 'alert_threshold', 
        'invoice_source', 'reporting_period', 'company_name',
        'escalation_team', 'date_tolerance', 'analysis_period'
    ]
    
    for field in required_fields:
        if field not in inputs or inputs[field] == 'sample_value':
            raise ValueError(f"Missing or invalid input for {field}. Please provide a valid value.")
    
    # Validate numeric inputs
    try:
        float(inputs['alert_threshold'])
        int(inputs['date_tolerance'])
    except ValueError:
        raise ValueError("alert_threshold must be a number and date_tolerance must be an integer")

def run():
    """Run the crew with real inputs."""
    print("Starting Financial Reconciliation Automation...")
    
    # Example inputs - replace with your actual data
    inputs = {
        'data_source': './data/financial_transactions.csv',
        'reporting_system': 'Google Sheets',
        'alert_threshold': '1000',  # Amount in dollars
        'invoice_source': './data/invoices.csv',
        'reporting_period': 'Q1 2024',
        'company_name': 'Acme Financial Services',
        'escalation_team': 'finance-team@company.com',
        'date_tolerance': '3',  # Days
        'analysis_period': '6 months'
    }
    
    try:
        validate_inputs(inputs)
        
        # Ensure data directories exist
        os.makedirs(os.path.dirname(inputs['data_source']), exist_ok=True)
        os.makedirs(os.path.dirname(inputs['invoice_source']), exist_ok=True)
        
        print(f"Running reconciliation with inputs: {inputs}")
        result = FinancialReconciliationCrew().crew().kickoff(inputs=inputs)
        
        print("\nReconciliation completed successfully!")
        print(f"Results: {result}")
        
        # Save results to a file
        with open('./reconciliation_report.md', 'w') as f:
            f.write("# Financial Reconciliation Report\n\n")
            f.write(str(result))
        
        print("Report saved to reconciliation_report.md")
        
    except Exception as e:
        print(f"Error during reconciliation: {str(e)}")
        sys.exit(1)

def train():
    """Train the crew for a given number of iterations."""
    if len(sys.argv) < 3:
        print("Usage: main.py train <iterations> <filename>")
        sys.exit(1)
    
    inputs = {
        'data_source': './data/financial_transactions.csv',
        'reporting_system': 'Google Sheets',
        'alert_threshold': '1000',
        'invoice_source': './data/invoices.csv',
        'reporting_period': 'Q1 2024',
        'company_name': 'Acme Financial Services',
        'escalation_team': 'finance-team@company.com',
        'date_tolerance': '3',
        'analysis_period': '6 months'
    }
    
    try:
        FinancialReconciliationCrew().crew().train(
            n_iterations=int(sys.argv[2]), 
            filename=sys.argv[3], 
            inputs=inputs
        )
        print(f"Training completed. Results saved to {sys.argv[3]}")
    except Exception as e:
        print(f"Error during training: {str(e)}")
        sys.exit(1)

def replay():
    """Replay the crew execution from a specific task."""
    if len(sys.argv) < 3:
        print("Usage: main.py replay <task_id>")
        sys.exit(1)
    
    try:
        FinancialReconciliationCrew().crew().replay(task_id=sys.argv[2])
        print(f"Replay of task {sys.argv[2]} completed")
    except Exception as e:
        print(f"Error during replay: {str(e)}")
        sys.exit(1)

def test():
    """Test the crew execution and returns the results."""
    if len(sys.argv) < 4:
        print("Usage: main.py test <iterations> <model_name>")
        sys.exit(1)
    
    inputs = {
        'data_source': './data/financial_transactions.csv',
        'reporting_system': 'Google Sheets',
        'alert_threshold': '1000',
        'invoice_source': './data/invoices.csv',
        'reporting_period': 'Q1 2024',
        'company_name': 'Acme Financial Services',
        'escalation_team': 'finance-team@company.com',
        'date_tolerance': '3',
        'analysis_period': '6 months'
    }
    
    try:
        result = FinancialReconciliationCrew().crew().test(
            n_iterations=int(sys.argv[2]), 
            openai_model_name=sys.argv[3], 
            inputs=inputs
        )
        print(f"Testing completed. Results: {result}")
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        sys.exit(1)

def run_ui():
    """Run the Streamlit UI"""
    try:
        # Get the absolute path to the streamlit app
        app_path = os.path.join(os.path.dirname(__file__), 'ui', 'streamlit_app.py')
        app_path = os.path.abspath(app_path)
        
        # Run the Streamlit app
        subprocess.run([
            "streamlit", 
            "run", 
            app_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit app: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Streamlit not found. Please install it with: pip install streamlit")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        print("Commands: run, train, replay, test, ui")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    elif command == "ui":
        run_ui()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)