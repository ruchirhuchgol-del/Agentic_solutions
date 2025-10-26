#!/bin/bash

# Environment setup script

echo "Setting up environment for Financial Reconciliation Automation..."

# Check if Poetry is installed
if ! command -v poetry &> /dev/null
then
    echo "Poetry could not be found. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Install dependencies
echo "Installing dependencies..."
poetry install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please update the .env file with your API keys."
fi

echo "Environment setup complete!"