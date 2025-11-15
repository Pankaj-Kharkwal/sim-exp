# PowerShell development startup script

Write-Host "🚀 Starting Pankh.AI Backend Development Server..." -ForegroundColor Green

# Check if .env exists
if (!(Test-Path .env)) {
    Write-Host "📝 Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "⚠️  Please update .env with your actual credentials" -ForegroundColor Yellow
}

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan
poetry install

# Run migrations
Write-Host "🗄️  Running database migrations..." -ForegroundColor Cyan
poetry run alembic upgrade head

# Start server
Write-Host "✨ Starting server on http://localhost:8000..." -ForegroundColor Green
Write-Host "📚 API docs available at http://localhost:8000/docs" -ForegroundColor Green
poetry run uvicorn app.main:app --reload --port 8000
