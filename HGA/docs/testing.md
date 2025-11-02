# Testing and CI

This document explains how to run tests and generate coverage for the Hypothesis Generation Agent (HGA).

## Run Tests Locally
The project uses `pytest` for unit and integration tests.

```bash
# If not installed
pip install pytest pytest-cov

# Run tests with coverage
pytest \
  --cov=hypothesis_generation_agent \
  --cov-report=term-missing \
  --cov-report=html:htmlcov \
  --cov-report=xml \
  -v
```

Alternatively, use the helper script:
```bash
./scripts/run_tests.sh
```

## Test Layout
- Unit tests: `tests/unit/`
- Integration tests: `tests/integration/`
- Fixtures: `tests/fixtures/`

Key tests:
- `tests/integration/test_crew.py` — verifies crew orchestration
- `tests/integration/test_workflow.py` — verifies end-to-end workflow
- `tests/unit/test_agents.py` — verifies agent configurations
- `tests/unit/test_tasks.py` — verifies tasks behavior
- `tests/unit/test_tools.py` — verifies tools

## Coverage Reports
- Terminal report: printed after test run
- HTML report: `htmlcov/index.html`
- XML report: `coverage.xml` (for CI systems)

## CI Integration
- Use GitHub Actions or your preferred CI provider.
- Ensure the environment has Python 3.10+ and installs dependencies from `requirements.txt`.
- Run the same `pytest` command with coverage flags.