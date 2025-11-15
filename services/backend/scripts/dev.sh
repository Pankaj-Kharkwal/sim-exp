#!/bin/bash
# Development startup script

echo "🚀 Starting Pankh.AI Backend Development Server..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your actual credentials"
fi

# Install dependencies
echo "📦 Installing dependencies..."
poetry install

# Run migrations
echo "🗄️  Running database migrations..."
poetry run alembic upgrade head

# Start server
echo "✨ Starting server on http://localhost:8000..."
echo "📚 API docs available at http://localhost:8000/docs"
poetry run uvicorn app.main:app --reload --port 8000
