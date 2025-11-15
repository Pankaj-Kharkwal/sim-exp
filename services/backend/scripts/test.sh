#!/bin/bash
# Run tests for Pankh.AI Backend

set -e

echo "🧪 Running Pankh.AI Backend Tests..."
echo ""

# Activate poetry environment
cd "$(dirname "$0")/.."

# Check if poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed. Please install Poetry first:"
    echo "   curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# Install dependencies if needed
echo "📦 Installing dependencies..."
poetry install --no-root
echo ""

# Run linting
echo "🔍 Running code quality checks..."
echo "  - Black (formatting)"
poetry run black --check app tests
echo "  - Ruff (linting)"
poetry run ruff check app tests
echo ""

# Run type checking
echo "🔍 Running type checks..."
poetry run mypy app --ignore-missing-imports
echo ""

# Run tests with coverage
echo "🧪 Running tests..."
poetry run pytest tests/ \
    --cov=app \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-report=xml \
    -v

echo ""
echo "✅ All tests passed!"
echo ""
echo "📊 Coverage report generated:"
echo "   - Terminal: See above"
echo "   - HTML: htmlcov/index.html"
echo "   - XML: coverage.xml"
