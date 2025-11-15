# Pankh.AI Microservices

Complete microservices architecture for the Pankh.AI workflow orchestration platform.

## Quick Start

### Prerequisites
- Docker & Docker Compose
- 8GB RAM minimum
- Ports available: 5173, 8000, 5432, 6379

### Start All Services

```bash
# From project root
docker-compose -f docker-compose.services.yml up --build
```

This starts:
- **PostgreSQL** (port 5432) - Database with pgvector extension
- **Redis** (port 6379) - Cache & message broker
- **Backend** (port 8000) - FastAPI application
- **Celery Worker** - Background job processor
- **Celery Beat** - Task scheduler
- **Frontend** (port 5173) - React + Vite application

### Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## Services Overview

### 🐘 PostgreSQL
- **Image**: pgvector/pgvector:pg17
- **Port**: 5432
- **Database**: pankh_ai
- **User**: postgres / postgres
- **Extensions**: pgvector (for embeddings)

### 🔴 Redis
- **Image**: redis:7-alpine
- **Port**: 6379
- **Usage**: Cache, Celery broker, Celery results

### 🚀 Backend (FastAPI)
- **Framework**: FastAPI + Uvicorn
- **Language**: Python 3.11
- **Port**: 8000
- **Features**:
  - 80+ REST API endpoints
  - JWT authentication
  - SQLAlchemy ORM
  - LangGraph workflow engine
  - Socket.IO real-time updates
  - 90 workflow blocks

### 👷 Celery Worker
- **Purpose**: Background job processing
- **Tasks**:
  - Workflow execution
  - Email sending
  - Data processing
  - File uploads
  - Batch operations

### ⏰ Celery Beat
- **Purpose**: Task scheduling
- **Tasks**:
  - Cleanup jobs
  - Scheduled workflows
  - Monitoring
  - Health checks
  - Statistics aggregation

### ⚛️ Frontend (React + Vite)
- **Framework**: React 19 + Vite
- **Language**: TypeScript
- **Port**: 5173
- **Features**:
  - Workflow editor (React Flow)
  - AI Copilot integration
  - Real-time collaboration
  - Block library
  - Knowledge base

---

## Development

### Run Backend Only

```bash
cd services/backend

# Install dependencies
pip install -e .

# Run migrations
alembic upgrade head

# Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Run Frontend Only

```bash
cd services/frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

### Run Workers

```bash
cd services/backend

# Start Celery worker
celery -A app.workers.celery_app worker --loglevel=info

# Start Celery beat (in another terminal)
celery -A app.workers.celery_app beat --loglevel=info
```

---

## Environment Configuration

### Backend (.env)
Located at: `services/backend/.env`

**Required**:
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/pankh_ai
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
```

**Optional AI Providers**:
```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
```

### Frontend (.env)
Create: `services/frontend/.env`

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

---

## Database Migrations

### Create Migration

```bash
cd services/backend
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback

```bash
alembic downgrade -1
```

---

## API Documentation

### Interactive API Docs
Visit: http://localhost:8000/docs

### Key Endpoints

**Workflows**:
- `GET /api/v1/workflows` - List all workflows
- `POST /api/v1/workflows` - Create workflow
- `GET /api/v1/workflows/{id}` - Get workflow
- `PUT /api/v1/workflows/{id}` - Update workflow
- `DELETE /api/v1/workflows/{id}` - Delete workflow
- `POST /api/v1/workflows/{id}/execute` - Execute workflow

**Blocks**:
- `GET /api/v1/blocks` - List all blocks
- `GET /api/v1/blocks/{type}` - Get block details
- `GET /api/v1/blocks/category/{category}` - Get blocks by category
- `POST /api/v1/blocks/generate` - Generate block with AI

**Executions**:
- `GET /api/v1/executions/{id}` - Get execution details
- `GET /api/v1/executions/{id}/logs` - Get execution logs

**Tasks**:
- `GET /api/v1/tasks` - List tasks
- `GET /api/v1/tasks/stats/workers` - Worker stats
- `GET /api/v1/tasks/stats/queues` - Queue stats

---

## Testing

### Backend Tests

```bash
cd services/backend
pytest
pytest --cov=app tests/
pytest tests/api/test_workflows.py -v
```

### Frontend Tests

```bash
cd services/frontend
npm test
npm run test:coverage
```

---

## Monitoring

### View Logs

```bash
# All services
docker-compose -f docker-compose.services.yml logs -f

# Specific service
docker-compose -f docker-compose.services.yml logs -f backend
docker-compose -f docker-compose.services.yml logs -f celery-worker

# Last 100 lines
docker-compose -f docker-compose.services.yml logs --tail=100 backend
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Database connection
docker exec pankh-postgres pg_isready -U postgres

# Redis connection
docker exec pankh-redis redis-cli ping
```

### Worker Monitoring

```bash
# Flower (Celery monitoring) - TODO: Add to docker-compose
celery -A app.workers.celery_app flower --port=5555
# Visit: http://localhost:5555
```

---

## Troubleshooting

### Port Already in Use

```bash
# Check what's using the port
lsof -i :8000
lsof -i :5173

# Kill the process
kill -9 <PID>
```

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Check database logs
docker-compose -f docker-compose.services.yml logs postgres

# Connect to database
docker exec -it pankh-postgres psql -U postgres -d pankh_ai
```

### Frontend Can't Connect to Backend

1. Check CORS settings in backend
2. Verify `VITE_API_BASE_URL` in frontend `.env`
3. Check backend is running: `curl http://localhost:8000/health`
4. Check browser console for errors

### Celery Tasks Not Processing

```bash
# Check worker logs
docker-compose -f docker-compose.services.yml logs -f celery-worker

# Check Redis connection
docker exec pankh-redis redis-cli ping

# Verify broker URL in backend .env
# Should be: CELERY_BROKER_URL=redis://redis:6379/1
```

### Hot Reload Not Working

```bash
# Backend: Check volume mounts in docker-compose
volumes:
  - ./services/backend:/app  # Should be present

# Frontend: Restart frontend service
docker-compose -f docker-compose.services.yml restart frontend
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                       Frontend (React)                  │
│                     http://localhost:5173               │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP/WebSocket
                      ↓
┌─────────────────────────────────────────────────────────┐
│                  Backend (FastAPI)                      │
│                  http://localhost:8000                  │
│  ┌──────────────┐  ┌─────────────┐  ┌──────────────┐  │
│  │ REST API     │  │ Socket.IO   │  │ Auth         │  │
│  └──────────────┘  └─────────────┘  └──────────────┘  │
└──────┬────────────────┬─────────────────┬──────────────┘
       │                │                 │
       ↓                ↓                 ↓
┌─────────────┐  ┌─────────────┐  ┌──────────────┐
│ PostgreSQL  │  │   Redis     │  │ Celery       │
│ (Database)  │  │  (Cache)    │  │ Workers      │
│   :5432     │  │   :6379     │  │              │
└─────────────┘  └─────────────┘  └──────────────┘
```

---

## Migration from Monolith

See detailed migration plan: `services/MIGRATION_PLAN.md`

### Migration Status: 95% Complete

**✅ Complete**:
- Backend API (100%)
- Database models (100%)
- Workers & scheduling (100%)
- Real-time service (100%)
- Frontend scaffold (100%)
- Basic pages (85%)

**⏳ In Progress**:
- Workflow canvas components
- Block palette
- Copilot integration

**📋 TODO**:
- Advanced collaboration features
- Full chat integration
- Complete template system

---

## Performance Tips

### Backend
- Use async endpoints for I/O operations
- Enable database connection pooling
- Use Redis caching for frequently accessed data
- Batch database operations

### Frontend
- Lazy load components
- Use React.memo for expensive components
- Virtualize long lists
- Optimize React Flow rendering

### Database
- Add indexes on frequently queried columns
- Use database migrations properly
- Monitor query performance
- Regular vacuum and analyze

---

## Production Deployment

### Build for Production

```bash
# Build all services
docker-compose -f docker-compose.services.yml build

# Or individually
cd services/backend && docker build -t pankh-backend .
cd services/frontend && docker build -t pankh-frontend .
```

### Environment Variables

Create production `.env` files with:
- Strong SECRET_KEY (32+ characters)
- Production database URL
- Real API keys
- Proper CORS origins
- Enable HTTPS

### Scaling

```bash
# Scale workers
docker-compose -f docker-compose.services.yml up --scale celery-worker=4

# Scale backend (with load balancer)
docker-compose -f docker-compose.services.yml up --scale backend=3
```

---

## Resources

- **Documentation**: `services/docs/`
- **Migration Plan**: `services/MIGRATION_PLAN.md`
- **Backend README**: `services/backend/README.md`
- **Frontend Source**: `services/frontend/src/`
- **Original Monolith**: `apps/sim/`

---

## Support

For issues, questions, or feature requests:
1. Check the troubleshooting section above
2. Review the docs in `services/docs/`
3. Check logs: `docker-compose logs`
4. Review migration plan: `MIGRATION_PLAN.md`

---

**Last Updated**: November 15, 2025
**Version**: 0.1.0
**Status**: Migration In Progress
