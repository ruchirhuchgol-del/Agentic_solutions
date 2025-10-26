
"""
Example script to run the Streamlit UI for financial reconciliation.
"""

import subprocess
import sys
import os

def run_ui():
    """Run the Streamlit UI."""
    try:
        # Get the absolute path to the streamlit app
        app_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'financial_reconciliation_automation', 'ui', 'streamlit_app.py')
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
    run_ui()