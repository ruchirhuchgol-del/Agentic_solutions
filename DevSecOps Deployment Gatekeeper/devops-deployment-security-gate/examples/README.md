# DevSecOps Deployment Gatekeeper Examples

This directory contains example scripts demonstrating how to use the DevSecOps Deployment Gatekeeper.

## Example Scripts

### 1. Basic Security Check
[security_check_example.py](file:///c%3A/Users/Ruchir/Desktop/DevSecOps%20Deployment%20Gatekeeper/devops-deployment-security-gate/examples/security_check_example.py) - Demonstrates how to run a security check on a pull request

```python
from devops_deployment_security_gate.core.orchestrator import SecurityGateOrchestrator

orchestrator = SecurityGateOrchestrator()
result = orchestrator.run_security_check(
    pr_number="123",
    repository="example-org/example-repo",
    branch_name="feature-security-fix"
)
```

### 2. Batch Security Checks
Example of running security checks on multiple pull requests:

```python
from devops_deployment_security_gate.core.orchestrator import SecurityGateOrchestrator

orchestrator = SecurityGateOrchestrator()
pr_list = [
    {
        "pr_number": "123",
        "repository": "example-org/example-repo",
        "branch_name": "feature-security-fix"
    },
    {
        "pr_number": "124",
        "repository": "example-org/example-repo",
        "branch_name": "bugfix-authentication"
    }
]

batch_result = orchestrator.run_batch_security_checks(pr_list)
```

### 3. Using the Main CLI
You can also use the command-line interface:

```bash
# Run security check on a pull request
python -m devops_deployment_security_gate run \
  --pr-number 123 \
  --repository example-org/example-repo \
  --branch feature-security-fix

# Run with output to file
python -m devops_deployment_security_gate run \
  --pr-number 123 \
  --repository example-org/example-repo \
  --branch feature-security-fix \
  --output result.json
```

## Prerequisites

Before running the examples, make sure you have:

1. Installed the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your environment variables in a `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

## Running the Examples

```bash
# Navigate to the project root
cd devops-deployment-security-gate

# Run the example script
python examples/security_check_example.py
```

## Configuration

The examples use the same configuration as the main application. See the main [README.md](file:///c%3A/Users/Ruchir/Desktop/DevSecOps%20Deployment%20Gatekeeper/devops-deployment-security-gate/README.md) for detailed configuration instructions.