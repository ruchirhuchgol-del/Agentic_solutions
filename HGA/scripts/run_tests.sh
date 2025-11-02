
# ==============================================================================
# HGA Test Runner Script
#
# This script runs the project's test suite using pytest and generates
# a coverage report.
#
# Usage:
#   chmod +x scripts/run_tests.sh
#   ./scripts/run_tests.sh
# ==============================================================================

set -e

echo "--- Running HGA Test Suite ---"

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "Error: pytest is not installed."
    echo "Please run the setup script first: ./scripts/setup_dev_env.sh"
    exit 1
fi

# Check if the virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Warning: It seems the virtual environment is not activated."
    echo "Attempting to activate it now..."
    source venv/bin/activate
    echo "Virtual environment activated."
fi

# Run pytest with coverage
echo "Running tests and generating coverage report..."
pytest \
    --cov=hypothesis_generation_agent \
    --cov-report=term-missing \
    --cov-report=html:htmlcov \
    --cov-report=xml \
    -v

echo ""
echo "--- Test Run Complete ---"
echo "Terminal coverage report is shown above."
echo "A detailed HTML report was generated in 'htmlcov/index.html'."
echo "An XML report was generated for CI/CD systems at 'coverage.xml'."