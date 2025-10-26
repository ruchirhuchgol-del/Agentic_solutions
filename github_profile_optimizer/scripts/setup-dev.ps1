# Setup development environment for GitHub Profile Optimizer

Write-Host "Setting up development environment..."

# Check if Python 3.10+ is available
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Python is not installed. Please install Python 3.10 or higher."
        exit 1
    }
} catch {
    Write-Host "Python is not installed. Please install Python 3.10 or higher."
    exit 1
}

# Check Python version
$versionMatch = [regex]::Match($pythonVersion, 'Python (\d+)\.(\d+)')
if ($versionMatch.Success) {
    $major = [int]$versionMatch.Groups[1].Value
    $minor = [int]$versionMatch.Groups[2].Value
    
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 10)) {
        Write-Host "Python 3.10 or higher is required. Current version: $pythonVersion"
        exit 1
    }
} else {
    Write-Host "Could not determine Python version: $pythonVersion"
    exit 1
}

Write-Host "Python version: $pythonVersion"

# Create virtual environment
Write-Host "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing dependencies..."
pip install -e ".[dev]"

# Copy environment file
if (!(Test-Path .env)) {
    Write-Host "Copying .env.example to .env..."
    Copy-Item .env.example .env
    Write-Host "Please edit .env to add your API keys"
}

Write-Host "Development environment setup complete!"
Write-Host ""
Write-Host "To activate the virtual environment, run:"
Write-Host "  .\venv\Scripts\Activate.ps1"
Write-Host ""
Write-Host "To run tests:"
Write-Host "  pytest"
Write-Host ""
Write-Host "To start the API server:"
Write-Host "  python -m src.github_profile_optimizer.api"