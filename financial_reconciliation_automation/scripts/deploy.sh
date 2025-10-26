#!/bin/bash

# Deployment script

echo "Deploying Financial Reconciliation Automation..."

# Build the project
echo "Building the project..."
poetry build

# Publish to PyPI (uncomment when ready)
# poetry publish

echo "Deployment complete!"