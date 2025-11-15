#!/bin/bash

echo "🚀 Starting Pankh.AI Services..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    echo "Please install Docker Desktop: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Error: Docker Compose is not available"
    echo "Please install Docker Compose"
    exit 1
fi

# Use docker compose or docker-compose depending on what's available
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

echo "✅ Docker found"
echo "📦 Using: $COMPOSE_CMD"
echo ""

# Create backend .env if it doesn't exist
if [ ! -f services/backend/.env ]; then
    echo "📝 Creating backend .env file..."
    cp services/backend/.env.example services/backend/.env
    echo "✅ Created services/backend/.env"
fi

# Start services
echo "🐳 Starting Docker services..."
echo ""

$COMPOSE_CMD -f docker-compose.services.yml up -d --build

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo ""
echo "🔍 Checking service health..."

# Check PostgreSQL
if docker exec pankh-postgres pg_isready -U postgres &> /dev/null; then
    echo "✅ PostgreSQL is ready"
else
    echo "⚠️  PostgreSQL is not ready yet"
fi

# Check Redis
if docker exec pankh-redis redis-cli ping &> /dev/null; then
    echo "✅ Redis is ready"
else
    echo "⚠️  Redis is not ready yet"
fi

# Wait a bit more for backend
sleep 5

# Check Backend
if curl -s http://localhost:8000/health &> /dev/null; then
    echo "✅ Backend is ready"
else
    echo "⚠️  Backend is starting... (this may take a minute)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Services are starting!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 Access Points:"
echo "   Frontend:    http://localhost:5173"
echo "   Backend API: http://localhost:8000"
echo "   API Docs:    http://localhost:8000/docs"
echo "   Health:      http://localhost:8000/health"
echo ""
echo "📊 Database:"
echo "   PostgreSQL:  localhost:5432"
echo "   Redis:       localhost:6379"
echo ""
echo "📝 View Logs:"
echo "   $COMPOSE_CMD -f docker-compose.services.yml logs -f"
echo ""
echo "🛑 Stop Services:"
echo "   $COMPOSE_CMD -f docker-compose.services.yml down"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
