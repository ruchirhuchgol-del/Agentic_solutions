
"""
Streamlit Dashboard Runner for GitHub Profile Optimizer
This script provides a convenient way to launch the Streamlit dashboard
for the GitHub Profile Optimizer project.
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Run the Streamlit dashboard."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    dashboard_path = project_root / "src" / "github_profile_optimizer" / "ui" / "dashboard.py"
    
    # Check if dashboard file exists
    if not dashboard_path.exists():
        print(f"Error: Dashboard file not found at {dashboard_path}")
        sys.exit(1)
    
    # Run Streamlit with the dashboard
    try:
        subprocess.run([
            "streamlit", 
            "run", 
            str(dashboard_path)
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit dashboard: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: Streamlit not found. Please install it with: pip install streamlit")
        sys.exit(1)

if __name__ == "__main__":
    main()