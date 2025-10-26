#!/bin/bash

# Test runner script

echo "Running tests for Financial Reconciliation Automation..."

# Run all tests
poetry run python -m pytest tests/ -v

echo "Tests completed!"