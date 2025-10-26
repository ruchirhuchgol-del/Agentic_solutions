# Makefile for GitHub Profile Optimizer

# Variables
PYTHON := python3
PIP := pip
TEST_FLAGS := 

# Default target
.PHONY: help
help:
	@echo "GitHub Profile Optimizer Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make install     Install dependencies"
	@echo "  make test        Run tests"
	@echo "  make lint        Run linters"
	@echo "  make typecheck   Run type checking"
	@echo "  make coverage    Run tests with coverage"
	@echo "  make clean       Clean build artifacts"
	@echo "  make docker      Build Docker image"
	@echo "  make run         Run the application"
	@echo "  make dev         Run in development mode"

# Install dependencies
.PHONY: install
install:
	$(PIP) install -e ".[dev]"

# Run tests
.PHONY: test
test:
	$(PYTHON) -m pytest $(TEST_FLAGS)

# Run linters
.PHONY: lint
lint:
	$(PYTHON) -m flake8 src/ tests/

# Run type checking
.PHONY: typecheck
typecheck:
	$(PYTHON) -m mypy src/

# Run tests with coverage
.PHONY: coverage
coverage:
	$(PYTHON) -m pytest --cov=src/github_profile_optimizer --cov-report=html --cov-report=term

# Clean build artifacts
.PHONY: clean
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf coverage.xml

# Build Docker image
.PHONY: docker
docker:
	docker build -t github-profile-optimizer .

# Run the application
.PHONY: run
run:
	$(PYTHON) -m src.github_profile_optimizer.main run

# Run in development mode
.PHONY: dev
dev:
	$(PYTHON) -m src.github_profile_optimizer.api

# Run setup script
.PHONY: setup
setup:
	./scripts/setup-dev.sh

# Run installation test
.PHONY: test-install
test-install:
	$(PYTHON) scripts/test-installation.py