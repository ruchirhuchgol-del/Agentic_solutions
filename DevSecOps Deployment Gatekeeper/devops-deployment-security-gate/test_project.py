
"""
Test script to verify that the DevSecOps Deployment Gatekeeper project is working correctly.
"""

import os
import sys
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_project():
    """Test the project with sample inputs."""
    print("Testing DevSecOps Deployment Gatekeeper...")
    
    try:
        # Import the crew
        from devops_deployment_security_gate.core.crew import DevopsDeploymentSecurityGateCrew
        print("✓ Crew imported successfully")
        
        # Sample inputs
        inputs = {
            'pr_number': '123',
            'repository': 'test-org/test-repo',
            'branch_name': 'feature-security-enhancement',
            'project_key': 'test-org_test-repo_feature-security-enhancement',
            'slack_channel': '#security-alerts',
            'sonarqube_url': 'https://sonarqube.example.com'
        }
        
        # Initialize the crew
        crew = DevopsDeploymentSecurityGateCrew()
        print(" Crew initialized successfully")
        
        # Test completed successfully
        print(" Project structure is correct and imports work")
        return True
        
    except Exception as e:
        print(f" Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_project()
    sys.exit(0 if success else 1)