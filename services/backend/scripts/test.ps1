# Run tests for Pankh.AI Backend (Windows PowerShell)

$ErrorActionPreference = "Stop"

Write-Host "🧪 Running Pankh.AI Backend Tests..." -ForegroundColor Cyan
Write-Host ""

# Change to backend directory
Set-Location "$PSScriptRoot\.."

# Check if poetry is installed
if (!(Get-Command poetry -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Poetry is not installed. Please install Poetry first:" -ForegroundColor Red
    Write-Host "   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -" -ForegroundColor Yellow
    exit 1
}

# Install dependencies if needed
Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan
poetry install --no-root
Write-Host ""

# Run linting
Write-Host "🔍 Running code quality checks..." -ForegroundColor Cyan
Write-Host "  - Black (formatting)" -ForegroundColor Gray
poetry run black --check app tests
Write-Host "  - Ruff (linting)" -ForegroundColor Gray
poetry run ruff check app tests
Write-Host ""

# Run type checking
Write-Host "🔍 Running type checks..." -ForegroundColor Cyan
poetry run mypy app --ignore-missing-imports
Write-Host ""

# Run tests with coverage
Write-Host "🧪 Running tests..." -ForegroundColor Cyan
poetry run pytest tests/ `
    --cov=app `
    --cov-report=term-missing `
    --cov-report=html `
    --cov-report=xml `
    -v

Write-Host ""
Write-Host "✅ All tests passed!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Coverage report generated:" -ForegroundColor Cyan
Write-Host "   - Terminal: See above" -ForegroundColor Gray
Write-Host "   - HTML: htmlcov/index.html" -ForegroundColor Gray
Write-Host "   - XML: coverage.xml" -ForegroundColor Gray
