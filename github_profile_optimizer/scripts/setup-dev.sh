#!/bin/bash

# Setup development environment for GitHub Profile Optimizer

set -e  # Exit on any error

echo "Setting up development environment..."

# Check if Python 3.10+ is available
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
MAJOR_VERSION=$(echo $PYTHON_VERSION | cut -d'.' -f1)
MINOR_VERSION=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$MAJOR_VERSION" -lt "3" ] || [ "$MAJOR_VERSION" -eq "3" ] && [ "$MINOR_VERSION" -lt "10" ]; then
    echo "Python 3.10 or higher is required. Current version: $PYTHON_VERSION"
    exit 1
fi

echo "Python version: $PYTHON_VERSION"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -e ".[dev]"

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install

# Copy environment file
if [ ! -f .env ]; then
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo "Please edit .env to add your API keys"
fi

echo "Development environment setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run tests:"
echo "  pytest"
echo ""
echo "To start the API server:"
echo "  python -m src.github_profile_optimizer.api"