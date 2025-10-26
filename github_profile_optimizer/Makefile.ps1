# PowerShell script for GitHub Profile Optimizer (Windows equivalent of Makefile)

param(
    [string]$Task = "help"
)

function Show-Help {
    Write-Host "GitHub Profile Optimizer PowerShell Commands"
    Write-Host ""
    Write-Host "Usage:"
    Write-Host "  .\Makefile.ps1 install     Install dependencies"
    Write-Host "  .\Makefile.ps1 test        Run tests"
    Write-Host "  .\Makefile.ps1 lint        Run linters"
    Write-Host "  .\Makefile.ps1 typecheck   Run type checking"
    Write-Host "  .\Makefile.ps1 coverage    Run tests with coverage"
    Write-Host "  .\Makefile.ps1 clean       Clean build artifacts"
    Write-Host "  .\Makefile.ps1 docker      Build Docker image"
    Write-Host "  .\Makefile.ps1 run         Run the application"
    Write-Host "  .\Makefile.ps1 dev         Run in development mode"
}

function Install-Dependencies {
    Write-Host "Installing dependencies..."
    pip install -e ".[dev]"
}

function Run-Tests {
    Write-Host "Running tests..."
    python -m pytest
}

function Run-Linters {
    Write-Host "Running linters..."
    python -m flake8 src/ tests/
}

function Run-TypeCheck {
    Write-Host "Running type checking..."
    python -m mypy src/
}

function Run-Coverage {
    Write-Host "Running tests with coverage..."
    python -m pytest --cov=src/github_profile_optimizer --cov-report=html --cov-report=term
}

function Clean-Build {
    Write-Host "Cleaning build artifacts..."
    Remove-Item -Path "build/" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path "dist/" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path "*.egg-info/" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path ".pytest_cache/" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path ".mypy_cache/" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path "htmlcov/" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path "coverage.xml" -Force -ErrorAction SilentlyContinue
}

function Build-Docker {
    Write-Host "Building Docker image..."
    docker build -t github-profile-optimizer .
}

function Run-Application {
    Write-Host "Running the application..."
    python -m src.github_profile_optimizer.main run
}

function Run-Development {
    Write-Host "Running in development mode..."
    python -m src.github_profile_optimizer.api
}

function Test-Installation {
    Write-Host "Running installation test..."
    python scripts/test-installation.py
}

# Main execution
switch ($Task) {
    "help" { Show-Help }
    "install" { Install-Dependencies }
    "test" { Run-Tests }
    "lint" { Run-Linters }
    "typecheck" { Run-TypeCheck }
    "coverage" { Run-Coverage }
    "clean" { Clean-Build }
    "docker" { Build-Docker }
    "run" { Run-Application }
    "dev" { Run-Development }
    "test-install" { Test-Installation }
    default { 
        Write-Host "Unknown task: $Task"
        Show-Help
    }
}