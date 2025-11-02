#!/bin/bash

# ==============================================================================
# HGA Development Environment Setup Script
#
# This script automates the setup of the development environment for the
# Hypothesis Generation Agent project.
#
# Usage:
#   chmod +x scripts/setup_dev_env.sh
#   ./scripts/setup_dev_env.sh
# ==============================================================================

set -e # Exit immediately if a command exits with a non-zero status.

# --- Configuration ---
PYTHON_VERSION="python3"
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
TEST_REQUIREMENTS_FILE="requirements-test.txt"
ENV_FILE=".env"

echo "--- HGA Development Environment Setup ---"
echo "This script will set up your local development environment."
echo ""

# 1. Check for Python
echo "[1/6] Checking for Python 3..."
if ! command -v $PYTHON_VERSION &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or newer."
    exit 1
else
    PYTHON_VERSION_FULL=$($PYTHON_VERSION --version)
    echo "Found: $PYTHON_VERSION_FULL"
fi

# 2. Create and activate virtual environment
echo ""
echo "[2/6] Setting up Python virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in '$VENV_DIR'..."
    $PYTHON_VERSION -m venv $VENV_DIR
else
    echo "Virtual environment '$VENV_DIR' already exists."
fi

echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# 3. Upgrade pip
echo ""
echo "[3/6] Upgrading pip..."
pip install --upgrade pip

# 4. Install dependencies
echo ""
echo "[4/6] Installing Python dependencies..."
if [ -f "$REQUIREMENTS_FILE" ]; then
    pip install -r $REQUIREMENTS_FILE
else
    echo "Warning: '$REQUIREMENTS_FILE' not found. Skipping main dependencies."
fi

if [ -f "$TEST_REQUIREMENTS_FILE" ]; then
    pip install -r $TEST_REQUIREMENTS_FILE
else
    echo "Warning: '$TEST_REQUIREMENTS_FILE' not found. Skipping test dependencies."
fi

# 5. Create necessary directories
echo ""
echo "[5/6] Creating necessary directories..."
mkdir -p logs
mkdir -p data/hypothesis_library
echo "Created 'logs/' and 'data/hypothesis_library/' directories."

# 6. Set up environment variables
echo ""
echo "[6/6] Setting up environment variables..."
if [ ! -f "$ENV_FILE" ]; then
    if [ -f ".env.example" ]; then
        echo "Creating '.env' file from '.env.example'..."
        cp .env.example $ENV_FILE
        echo "SUCCESS: '.env' file created."
        echo ""
        echo "!!! IMPORTANT !!!"
        echo "Please edit the '$ENV_FILE' file and add your API keys and other secrets."
        echo "You will not be able to run the project without it."
    else
        echo "Warning: '.env.example' not found. Please create a '$ENV_FILE' file manually."
    fi
else
    echo "Environment file '$ENV_FILE' already exists."
fi

# --- Completion ---
echo ""
echo "--- Setup Complete! ---"
echo "To activate the environment for your current shell session, run:"
echo "  source $VENV_DIR/bin/activate"
echo ""
echo "Once activated, you can run the project with:"
echo "  crewai run"
echo "Or run the test suite with:"
echo "  ./scripts/run_tests.sh"