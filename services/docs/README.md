# Comprehensive Comparison: Sim App (Original) vs Pankh.AI Services (New)

## Executive Summary

This document provides a detailed comparison between the original **Sim** monolithic Next.js/TypeScript application (`apps/sim`) and the new **Pankh.AI** microservices architecture (`services/backend` + `services/frontend`).

### Key Architectural Shift
- **Original**: Monolithic Next.js app with embedded backend logic, database models, and business logic all in one codebase
- **New**: Microservices approach - FastAPI backend (Python) + React frontend (TypeScript) + Workers/Realtime services

---

## 1. ARCHITECTURE COMPARISON

### Original Sim Architecture

```
apps/sim/
├── app/                          # Next.js App Router
│   ├── (auth)/                   # Authentication pages
│   ├── (landing)/                # Marketing/landing pages
│   ├── api/                       # Backend API routes (Node.js)
│   ├── workspace/                 # Main application pages
│   └── chat/                      # Chat interface
├── blocks/                        # Workflow block implementations
│   ├── blocks/                    # 100+ block types (TypeScript)
│   └── registry.ts
├── executor/                      # Workflow execution engine
│   ├── index.ts                   # Main executor (10,000+ lines)
│   ├── handlers/                  # Block handlers
│   └── tests/
├── components/                    # React components
├── lib/                           # Utilities and services
│   ├── auth.ts                    # Authentication logic
│   ├── copilot/                   # AI copilot tools
│   ├── billing/                   # Billing logic
│   ├── execution/                 # Execution utilities
│   └── ... many more
├── providers/                     # Context providers
├── stores/                        # Zustand stores
├── tools/                         # Tool integrations
├── triggers/                      # Event triggers
├── background/                    # Background tasks
├── socket-server/                 # Socket.IO server
└── services/                      # Business logic services

Database:
- Drizzle ORM (TypeScript)
- PostgreSQL (via packages/db)
- Schema in: packages/db/schema.ts
- Migrations in: packages/db/migrations/
```

**Characteristics:**
- ✅ Monolithic architecture - all code in one repo
- ✅ Full-stack JavaScript/TypeScript
- ✅ Single tech stack (Next.js, React, Node.js)
- ✅ Unified build and deployment
- ⚠️ Tightly coupled frontend and backend
- ⚠️ Complex dependency management
- ⚠️ Difficult to scale services independently

---

### New Pankh.AI Microservices Architecture

```
services/
├── backend/                       # FastAPI Python backend
│   ├── app/
│   │   ├── api/v1/                # REST API endpoints
│   │   ├── core/                  # Configuration & security
│   │   ├── db/                    # SQLAlchemy models
│   │   ├── executor/              # Workflow engine (Python/LangGraph)
│   │   ├── realtime/              # Socket.IO service ✨ NEW
│   │   ├── schemas/               # Pydantic models
│   │   ├── services/              # Business logic
│   │   └── workers/               # Celery background jobs ✨ NEW
│   ├── alembic/                   # Database migrations
│   ├── scripts/                   # Startup scripts
│   └── tests/
│
└── frontend/                      # React + Vite frontend
    ├── src/
    │   ├── components/            # React components
    │   ├── lib/                   # Utilities
    │   ├── pages/ (or routing)
    │   ├── App.tsx
    │   └── main.tsx
    ├── index.html
    ├── vite.config.ts
    └── package.json

Database:
- SQLAlchemy 2.0 (Python)
- PostgreSQL (async)
- Models in: app/db/models/
- Migrations in: alembic/versions/
```

**Characteristics:**
- ✅ Microservices architecture - independent services
- ✅ Polyglot (Python backend, TypeScript frontend)
- ✅ Separation of concerns - backend, frontend, workers, realtime
- ✅ Independent scaling capabilities
- ✅ Cleaner dependencies per service
- ✅ Production-ready workers and realtime services
- ✅ Better deployment flexibility (containers)

---

## Architectural Comparison Table

| Aspect | Original Sim | Pankh.AI Services |
|--------|--------------|-------------------|
| **Structure** | Monolithic | Microservices |
| **Backend Lang** | TypeScript/Node.js | Python (FastAPI) |
| **Frontend** | Next.js built-in | React + Vite (separate) |
| **Database ORM** | Drizzle (TypeScript) | SQLAlchemy (Python) |
| **API Framework** | Next.js API Routes | FastAPI |
| **Workers** | Background service (socket-server) | Celery + Redis ✨ NEW |
| **Realtime** | Socket.IO in main app | Socket.IO service ✨ NEW |
| **Build Tool** | Next.js | Vite (frontend), Poetry (backend) |
| **Package Manager** | Bun | npm (frontend), Poetry (backend) |
| **Executor** | TypeScript (10,000+ lines) | Python (LangGraph) |
| **Deployment** | Single container | Multiple containers |
| **Scaling** | Vertical only | Horizontal (each service) |

---

## 2. BACKEND COMPARISON

### Original Sim Backend (Node.js/TypeScript)

**Technology Stack:**
```json
{
  "runtime": "Node.js/Bun",
  "framework": "Next.js API Routes",
  "orm": "Drizzle ORM",
  "database": "PostgreSQL",
  "auth": "better-auth (Next.js)",
  "ai_sdk": ["OpenAI", "Anthropic", "Groq", "Cerebras"],
  "payment": "Stripe",
  "storage": ["AWS S3", "Azure Blob"],
  "realtime": "Socket.IO (built-in)",
  "workers": "Custom background service"
}
```

**API Routes Location:** `apps/sim/app/api/`

**API Endpoint Categories:**
```
/api/auth/              - Authentication (login, register, SSO, etc.)
/api/v1/workflows/      - Workflow CRUD operations
/api/v1/blocks/         - Block management
/api/v1/executions/     - Workflow execution
/api/v1/chat/           - Chat interface
/api/v1/knowledge/      - Knowledge base management
/api/billing/           - Billing and subscriptions
/api/usage/             - Usage tracking
/api/providers/         - AI provider management
/api/jobs/              - Job management
/api/cron/              - Scheduled tasks
/api/webhooks/          - Webhook management
/api/users/             - User management
/api/organizations/     - Organization management
... and more
```

**Database Model (Drizzle):**
- Schema file: `packages/db/schema.ts` (~5,000+ lines)
- Migrations: `packages/db/migrations/`
- Uses PostgreSQL with Drizzle query builder

**Key Backend Services in lib:**
- `lib/auth.ts` - JWT and session management
- `lib/execution/` - Execution utilities
- `lib/copilot/` - AI copilot functionality
- `lib/billing/` - Subscription and payment logic
- `lib/email/` - Email utilities
- `lib/storage/` - File storage (S3/Azure)
- `lib/guardrails/` - Safety and validation

**Executor (Workflow Engine):**
- **File**: `apps/sim/executor/index.ts` (~10,000 lines)
- **Language**: TypeScript
- **Features**:
  - 100+ block types implemented
  - Recursive execution
  - Loop and parallel support
  - Variable resolution
  - Error handling and retries
  - Test execution sandboxing

**Block Implementations:**
- **Location**: `apps/sim/blocks/blocks/`
- **Count**: 100+ blocks
- **Examples**:
  - `agent.ts` - AI agent execution
  - `api.ts` - REST API calls
  - `condition.ts` - Conditional logic
  - `database.ts` - Database operations
  - `email.ts` - Email sending
  - `http.ts` - HTTP requests
  - `loop.ts` - Looping
  - `parallel.ts` - Parallel execution
  - And many more...

**Authentication:**
- Framework: `better-auth` (Next.js native)
- Features: OAuth, SSO, JWT, Session-based
- Location: `lib/auth.ts` (~56KB)

---

### New Pankh.AI Backend (Python/FastAPI)

**Technology Stack:**
```toml
[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.115.0"
uvicorn = "^0.32.0"
sqlalchemy = "^2.0.36"
alembic = "^1.14.0"
psycopg2-binary = "^2.9.10"
asyncpg = "^0.30.0"
pydantic = "^2.10.0"
fastapi-users = "^13.0.0"
httpx = "^0.28.0"
redis = "^5.2.0"
celery = "^5.4.0"
python-socketio = "^5.11.0"
langgraph = "^0.2.60"
langchain = "^0.3.12"
openai = "^1.57.0"
anthropic = "^0.41.0"
stripe = "^11.2.0"
azure-storage-blob = "^12.24.0"
boto3 = "^1.35.76"
```

**API Routes Location:** `services/backend/app/api/v1/`

**API Endpoints (Implemented):**
```python
# Authentication
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
GET    /api/v1/auth/me

# Workflows
GET    /api/v1/workflows
POST   /api/v1/workflows
GET    /api/v1/workflows/{id}
PUT    /api/v1/workflows/{id}
DELETE /api/v1/workflows/{id}

# Blocks
GET    /api/v1/blocks
POST   /api/v1/blocks/generate        # AI-powered block generation

# Executions
POST   /api/v1/workflows/{id}/execute
GET    /api/v1/executions/{id}
GET    /api/v1/executions/{id}/logs

# Billing
GET    /api/v1/billing/plans
POST   /api/v1/billing/subscription

# Tasks (NEW)
GET    /api/v1/tasks
GET    /api/v1/tasks/{id}
POST   /api/v1/tasks/{id}/cancel
GET    /api/v1/tasks/stats/workers
GET    /api/v1/tasks/stats/queues
```

**Database Models (SQLAlchemy):**
- **Location**: `services/backend/app/db/models/`
- **Files**:
  - `user.py` - User model
  - `organization.py` - Organization model
  - `workflow.py` - Workflow and related models
  - `api_key.py` - API key management
  
**Key Models:**
```python
# Workflow models
- Workflow
- WorkflowFolder
- WorkflowBlock
- WorkflowEdge
- WorkflowSubflow
- WorkflowExecutionSnapshot
- WorkflowExecutionLog

# User models
- User
- Organization
- APIKey
```

**Executor (Workflow Engine):**
- **Framework**: LangGraph (LangChain's graph framework)
- **Location**: `services/backend/app/executor/`
- **Language**: Python
- **Features**:
  - Graph-based execution (more efficient than recursive)
  - Async/await support
  - Built-in error handling
  - State management
  - Variable resolution

**Block Implementations (Python):**
- **Location**: `services/backend/app/executor/blocks/`
- **Count**: 15 blocks (core implementations)
- **Blocks**:
  - `agent.py` - AI agent with 5 provider support
  - `api.py` - REST API calls
  - `condition.py` - Conditional branching
  - `database.py` - Database operations
  - `delay.py` - Delay/wait
  - `email.py` - Email sending
  - `function.py` - Custom functions
  - `http.py` - HTTP requests
  - `loop.py` - Loop iteration
  - `parallel.py` - Parallel execution
  - `response.py` - Response formatting
  - `transformer.py` - Data transformation
  - `variables.py` - Variable management
  - `webhook.py` - Webhook calls

**Authentication:**
- Framework: `fastapi-users` (FastAPI native)
- Features: JWT, OAuth, Email verification
- Location: `app/api/v1/auth.py`

**Services:**
- **Location**: `services/backend/app/services/`
- **Files**:
  - `workflow_service.py` - Workflow CRUD logic
  - `workflow_execution.py` - Execution logic
  - `ai/` - AI services (multi-provider)

---

### Backend Comparison Table

| Feature | Original Sim | Pankh.AI |
|---------|--------------|----------|
| **Language** | TypeScript | Python 3.11 |
| **Framework** | Next.js API Routes | FastAPI |
| **ORM** | Drizzle | SQLAlchemy 2.0 |
| **Database Driver** | postgres/mysql2 | asyncpg |
| **Block Count** | 100+ | 15 (core) |
| **Auth Framework** | better-auth | fastapi-users |
| **Workers** | Custom service | Celery + Redis |
| **Task Queue** | Redis-based | Celery (Redis backend) |
| **Realtime** | Socket.IO in main | Socket.IO service |
| **Executor** | TypeScript (10K lines) | LangGraph (Python) |
| **API Type** | Node.js routes | REST (FastAPI) |
| **Async** | Built-in (Node.js) | async/await (Python) |
| **Scalability** | Vertical | Horizontal (services) |

---

## 3. FRONTEND COMPARISON

### Original Sim Frontend (Next.js/React)

**Technology Stack:**
```json
{
  "framework": "Next.js 15",
  "ui_library": "React 19",
  "styling": "Tailwind CSS",
  "components": "shadcn/ui",
  "state_management": ["Zustand", "React Context"],
  "data_fetching": "React Server Components + fetch",
  "forms": "React Hook Form",
  "validation": "Zod",
  "flow_editor": "React Flow",
  "build_tool": "Next.js + Turbopack",
  "package_manager": "Bun",
  "deployment": "Vercel/Self-hosted"
}
```

**Directory Structure:**
```
apps/sim/
├── app/
│   ├── (auth)/                # Auth pages
│   │   ├── login/
│   │   ├── signup/
│   │   ├── verify/
│   │   └── reset-password/
│   ├── (landing)/             # Public pages
│   │   ├── blog/
│   │   ├── careers/
│   │   ├── privacy/
│   │   └── terms/
│   ├── workspace/             # Main app
│   │   ├── [workspaceId]/
│   │   │   ├── flows/
│   │   │   ├── chat/
│   │   │   └── settings/
│   │   └── layout.tsx
│   ├── api/                   # Backend routes
│   └── layout.tsx
├── components/                # React components (100+)
│   ├── ui/                    # shadcn components
│   ├── editor/                # Workflow editor
│   └── ... many feature components
├── blocks/blocks/             # 100+ block UIs
├── lib/                       # 200+ utilities
└── stores/                    # Zustand state
```

**Page Structure:**
- Auth pages: Login, Signup, Verification, Password reset
- Landing pages: Marketing, Blog, Careers
- Main app: Workspace, Workflows, Chat, Settings
- Uses App Router (Next.js 13+ paradigm)

**Components:**
- **Count**: 100+ React components
- **UI Components**: From shadcn/ui (Button, Card, Dialog, etc.)
- **Editor Components**: Workflow editor, node editor, flow canvas
- **Feature Components**: Workflow list, execution viewer, settings panels

**State Management:**
- Zustand stores for client state
- React Context for theme, auth context
- Server Components for server state

**Data Fetching:**
- Direct fetch in Server Components
- React Query would be used for client
- API endpoints via Next.js routes

**Styling:**
- Tailwind CSS (utility-first)
- CSS Modules where needed
- shadcn/ui for components

---

### New Pankh.AI Frontend (React + Vite)

**Technology Stack:**
```json
{
  "framework": "React 19 + Vite",
  "ui_library": "React",
  "styling": "Tailwind CSS",
  "components": "shadcn/ui (copied from Sim)",
  "state_management": "Zustand",
  "data_fetching": "TanStack Query + Axios",
  "forms": "React Hook Form",
  "validation": "Zod",
  "flow_editor": "React Flow",
  "routing": "React Router",
  "build_tool": "Vite",
  "package_manager": "npm",
  "deployment": "Docker/Self-hosted"
}
```

**Directory Structure:**
```
services/frontend/
├── src/
│   ├── App.tsx              # Main app component
│   ├── main.tsx             # Entry point
│   ├── components/          # React components
│   │   ├── ui/              # UI components (copied from Sim)
│   │   └── ... feature components
│   ├── lib/                 # Utilities
│   │   ├── api-key/         # API key management
│   │   ├── auth/            # Auth utilities
│   │   ├── billing/         # Billing logic (copied)
│   │   ├── copilot/         # Copilot tools (copied)
│   │   ├── branding/        # Branding utilities
│   │   ├── chunkers/        # Text chunking
│   │   └── ...
│   └── pages/ (or routes)   # Page components (WIP)
├── public/                  # Static assets
├── index.html               # HTML entry
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
└── package.json
```

**Key Differences from Sim:**
- ✅ React Client Components (not Next.js Server Components)
- ✅ Vite for faster dev experience
- ✅ React Router instead of Next.js routing
- ✅ TanStack Query instead of fetch
- ✅ axios for API calls instead of fetch
- ✅ Zustand instead of React Context
- ✅ Standalone app (not monolithic)

**Components Status:**
- ✅ UI components copied from Sim
- ✅ shadcn/ui components available
- ⚠️ Page components being built
- ⚠️ Feature components being ported

**Library Files Ported (from apps/sim/lib/):**
- ✅ `lib/billing/` - Billing logic
- ✅ `lib/copilot/` - Copilot tools
- ✅ `lib/branding/` - Brand utilities
- ✅ `lib/chunkers/` - Text chunking
- ⚠️ `lib/auth/` - Auth (adapted for client)
- ⚠️ `lib/api-key/` - API key management

---

### Frontend Comparison Table

| Feature | Original Sim | Pankh.AI Frontend |
|---------|--------------|-------------------|
| **Framework** | Next.js 15 | React 19 + Vite |
| **Rendering** | SSR + CSR | CSR only |
| **Routing** | Next.js App Router | React Router |
| **State** | Zustand + Context | Zustand |
| **Data Fetching** | fetch + React Query | TanStack Query + Axios |
| **Styling** | Tailwind CSS | Tailwind CSS |
| **Build Tool** | Next.js + Turbopack | Vite |
| **Package Manager** | Bun | npm |
| **Components** | 100+ | Built from Sim's UI kit |
| **Server Components** | Yes | No (Client only) |
| **API Communication** | fetch | Axios + React Query |
| **Production** | Vercel/Self | Docker/Self |

---

## 4. FEATURES COMPARISON

### Features in Original Sim

**Core Workflow Features:**
- ✅ Visual workflow editor with React Flow
- ✅ 100+ pre-built block types
- ✅ Block customization and configuration
- ✅ Workflow execution (local)
- ✅ Workflow scheduling via cron
- ✅ Webhook triggers
- ✅ API triggers
- ✅ Manual execution
- ✅ Chat-based triggers
- ✅ Execution logs and debugging
- ✅ Variable management
- ✅ Global variables
- ✅ Environment variables

**AI & Intelligence:**
- ✅ Multiple AI providers (OpenAI, Anthropic, Groq, etc.)
- ✅ AI copilot for workflow building
- ✅ AI block auto-generation (research-based)
- ✅ Function calling
- ✅ Structured output (Pydantic models)
- ✅ Knowledge base integration
- ✅ File uploads and parsing
- ✅ Browser automation (Stagehand)
- ✅ Web search (Exa)

**Collaboration & Sharing:**
- ✅ Workspace management
- ✅ Multi-user workspaces
- ✅ Workflow sharing
- ✅ Real-time collaborative editing
- ✅ Cursor sharing
- ✅ Comments and mentions

**Execution & Monitoring:**
- ✅ Workflow execution tracking
- ✅ Real-time execution progress
- ✅ Block-level logs
- ✅ Error tracking and debugging
- ✅ Execution history
- ✅ Performance metrics
- ✅ Rate limiting

**User Management:**
- ✅ User registration/login
- ✅ OAuth (GitHub, Google, etc.)
- ✅ SSO support
- ✅ Password reset
- ✅ Profile management
- ✅ Organization management

**Billing & Monetization:**
- ✅ Subscription plans
- ✅ Usage-based billing
- ✅ Stripe integration
- ✅ Billing history
- ✅ Invoice management

**Integrations:**
- ✅ 30+ third-party integrations
- ✅ API key management
- ✅ OAuth for integrations
- ✅ Webhook support (send/receive)
- ✅ Database connections
- ✅ File storage (S3, Azure)

**Chat Interface:**
- ✅ Chat UI with workflow interaction
- ✅ File uploads in chat
- ✅ Real-time messaging
- ✅ Chat history

---

### Features in Pankh.AI (New)

**Core Workflow Features:**
- ✅ Visual workflow editor (planned - using React Flow from Sim)
- ✅ 15 core block types (Python implementations)
- ✅ Workflow execution (Python-based)
- ✅ Workflow scheduling (Celery Beat)
- ⚠️ API triggers (planned)
- ⚠️ Webhook triggers (planned)
- ⚠️ Chat triggers (planned)
- ✅ Execution logs (database-backed)
- ✅ Variable management
- ✅ Structured data support (Pydantic)

**AI & Intelligence:**
- ✅ Multiple AI providers (OpenAI, Anthropic, LangChain)
- ⚠️ AI copilot (planned)
- ✅ Agent block with tool use
- ⚠️ AI block generation (planned for FastAPI backend)
- ✅ Function calling
- ✅ LangGraph-based AI orchestration

**Workers & Background Jobs:**
- ✅ Celery task queue (NEW)
- ✅ 5 main background tasks
- ✅ 5 scheduled tasks
- ✅ Task monitoring API
- ✅ Rate limiting per task type

**Real-time Services:**
- ✅ Socket.IO server (NEW)
- ✅ Execution progress updates
- ✅ Multi-user collaboration
- ✅ Room-based broadcasting

**User Management:**
- ✅ User registration/login (basic)
- ⚠️ OAuth (planned)
- ⚠️ SSO (planned)

**Billing:**
- ⚠️ Basic billing endpoints (stubbed)

**Integrations:**
- ⚠️ Planned for future

**Frontend UI:**
- ⚠️ Basic dashboard (App.tsx)
- ⚠️ Pages/routes being built
- ✅ UI components copied from Sim
- ⚠️ Workflow editor (planned)

---

### Features Comparison Table

| Feature | Sim | Pankh.AI | Status |
|---------|-----|----------|--------|
| **Workflow Editor** | ✅ Full | ⚠️ Building | In Progress |
| **Blocks** | 100+ | 15 core | Core implemented |
| **AI Providers** | 5+ | 3+ | Working |
| **Execution** | ✅ Full | ✅ Full | Completed |
| **Scheduling** | ✅ Full | ✅ Celery | Completed |
| **Workers** | Custom | ✅ Celery | Completed |
| **Realtime** | Socket.IO | ✅ Socket.IO | Completed |
| **Authentication** | ✅ Full | ⚠️ Basic | In Progress |
| **Collaboration** | ✅ Yes | ✅ Yes | Completed |
| **Billing** | ✅ Full | ⚠️ Stubbed | Planned |
| **Integrations** | 30+ | ⚠️ Planned | Planned |
| **API** | 40+ endpoints | 20+ endpoints | Core only |

---

## 5. KEY FILES COMPARISON

### Database Schema

**Original Sim (Drizzle):**
```
Location: packages/db/schema.ts
Lines: 5,000+
Format: TypeScript (Drizzle dialect)
Key Tables:
- users
- organizations/workspaces
- workflows
- workflow_blocks
- workflow_edges
- workflow_executions
- workflow_execution_logs
- integrations
- knowledge_bases
- api_keys
- subscriptions
- billings
- ... and more
```

**New Pankh.AI (SQLAlchemy):**
```
Location: services/backend/app/db/models/
Files: 5 files (user.py, organization.py, workflow.py, api_key.py, __init__.py)
Format: Python (SQLAlchemy 2.0)
Models:
- User
- Organization
- Workspace
- Workflow
- WorkflowFolder
- WorkflowBlock
- WorkflowEdge
- WorkflowSubflow
- WorkflowExecutionSnapshot
- WorkflowExecutionLog
- APIKey
```

---

### Authentication

**Original Sim:**
```
Location: apps/sim/lib/auth.ts (56 KB)
Framework: better-auth
Features:
- JWT tokens
- Session management
- OAuth providers
- SSO
- Email verification
- Password reset
```

**New Pankh.AI:**
```
Location: services/backend/app/api/v1/auth.py
Framework: fastapi-users
Features:
- JWT tokens
- Basic auth endpoints (TODO)
- OAuth (planned)
- Email verification (planned)
```

---

### Executor/Workflow Engine

**Original Sim:**
```
Location: apps/sim/executor/index.ts
Size: 10,000+ lines
Language: TypeScript
Approach: Recursive execution
Features:
- 100+ block types
- Dynamic block loading
- Variable resolution
- Error handling
- Retry logic
- Test sandboxing
```

**New Pankh.AI:**
```
Location: services/backend/app/executor/
Language: Python
Framework: LangGraph
Approach: Graph-based execution
Features:
- 15 core block types
- Async execution
- State management
- Variable resolution
- Error handling
- Async-friendly design
```

---

### Configuration Files

**Original Sim:**
```
apps/sim/package.json
apps/sim/tsconfig.json
apps/sim/next.config.ts
apps/sim/tailwind.config.ts
apps/sim/vitest.config.ts
apps/sim/drizzle.config.ts
apps/sim/middleware.ts
```

**New Pankh.AI Backend:**
```
services/backend/pyproject.toml
services/backend/alembic.ini
services/backend/.env
services/backend/Dockerfile
services/backend/check_env.py
```

**New Pankh.AI Frontend:**
```
services/frontend/package.json
services/frontend/vite.config.ts
services/frontend/tailwind.config.js
services/frontend/tsconfig.json
services/frontend/Dockerfile
services/frontend/.env
```

---

### Key Services Comparison

#### Billing Service

**Original Sim:**
```
apps/sim/lib/billing/
├── calculations/
├── core/
├── storage/
├── subscriptions/
├── types/
├── validation/
├── webhooks/
└── index.ts
```

**New Pankh.AI:**
```
services/frontend/src/lib/billing/
(Copied from Sim for frontend logic)

services/backend/app/api/v1/billing.py
(Stub endpoints - to be implemented)
```

#### API Key Management

**Original Sim:**
```
apps/sim/lib/api-key/
└── utilities
```

**New Pankh.AI:**
```
services/frontend/src/lib/api-key/

services/backend/app/db/models/api_key.py
(SQLAlchemy model)

services/backend/app/api/v1/
(API endpoints - to be implemented)
```

#### Copilot/AI Tools

**Original Sim:**
```
apps/sim/lib/copilot/
├── auth/
├── tools/
│   ├── client/
│   │   ├── blocks/
│   │   ├── examples/
│   │   ├── gdrive/
│   │   ├── google/
│   │   ├── other/
│   │   ├── user/
│   │   └── workflow/
│   └── server/
└── ... more
```

**New Pankh.AI:**
```
services/frontend/src/lib/copilot/
(Copied from Sim)

services/backend/app/services/ai/
(AI service implementations)
```

---

## 6. MIGRATION SUMMARY

### What Was Migrated

#### ✅ Successfully Migrated
1. **Database Schema**
   - From Drizzle (TS) to SQLAlchemy (Python)
   - Core models ported
   - Alembic migrations set up

2. **Executor Engine**
   - From TypeScript to Python + LangGraph
   - 15 core blocks implemented
   - Async/await architecture
   - Variable resolution system

3. **Block Implementations**
   - 15 Python blocks created
   - Agent, API, HTTP, Email, Database, Loop, Parallel, etc.

4. **Frontend Components**
   - UI library copied to new frontend
   - shadcn/ui components available
   - Tailwind CSS configured

5. **Workers Service**
   - Celery + Redis setup
   - 5 main tasks + 5 scheduled tasks
   - Task monitoring API
   - Rate limiting

6. **Realtime Service**
   - Socket.IO server
   - Room management
   - Event broadcasting
   - Execution notifications

#### ⚠️ Partially Migrated
1. **Authentication**
   - Basic endpoints implemented
   - OAuth/SSO planned

2. **Frontend Pages**
   - Basic App.tsx template
   - Routes being built
   - Pages in progress

3. **Billing**
   - Stub endpoints created
   - Full implementation planned

#### ❌ Not Yet Migrated
1. **Advanced AI Features**
   - AI block generation
   - AI copilot
   - Knowledge bases

2. **Integrations**
   - 30+ third-party integrations
   - Scheduled for future

3. **Chat Interface**
   - Planned for future phases

4. **Advanced Collaboration**
   - Cursor sharing
   - Comments/mentions
   - Planned for future

---

## 7. TECHNOLOGY STACK COMPARISON

### Original Sim Stack

```
Frontend:
- React 19
- Next.js 15
- TypeScript 5.7
- Tailwind CSS 3.4
- React Flow 11
- Zustand
- TanStack Query
- React Hook Form

Backend (Node.js):
- TypeScript 5.7
- Next.js API Routes
- Drizzle ORM
- PostgreSQL
- Socket.IO
- Redis
- Various AI SDKs

Infrastructure:
- Vercel (deployment)
- PostgreSQL (database)
- Redis (caching)
- AWS S3 / Azure Blob (storage)

Package Manager: Bun
```

### New Pankh.AI Stack

```
Frontend:
- React 19
- Vite 7
- TypeScript ~5.9
- Tailwind CSS 4
- React Flow 11
- Zustand
- TanStack Query
- React Hook Form
- Axios
- React Router

Backend (Python):
- Python 3.11
- FastAPI 0.115
- SQLAlchemy 2.0
- PostgreSQL 17
- Async (asyncpg)
- Socket.IO 5.11
- Celery 5.4
- Redis 5.2
- LangGraph 0.2
- LangChain 0.3
- Pydantic 2.10

Infrastructure:
- Docker (containers)
- PostgreSQL 17 (database)
- Redis 5 (broker & cache)
- Azure Blob / AWS S3 (storage)

Package Managers: 
- Frontend: npm
- Backend: Poetry
```

---

## 8. PERFORMANCE & SCALABILITY

### Original Sim

**Pros:**
- Fast client-side rendering
- Server-side optimizations (Next.js)
- Built-in caching
- Turbopack for faster builds

**Cons:**
- Monolithic deployment
- Can't scale services independently
- TypeScript compilation overhead
- Bun runtime (less mature)

**Scalability:**
- Vertical scaling only
- Single-instance or load balancer
- Tightly coupled services

---

### New Pankh.AI

**Pros:**
- Independent service scaling
- Efficient async Python (asyncpg, asyncio)
- LangGraph for efficient execution
- Celery for distributed task processing
- Separate frontend (CDN-friendly)
- Container-based (Kubernetes-ready)

**Cons:**
- Inter-service network overhead
- Added complexity
- Dual language ecosystem

**Scalability:**
- Horizontal scaling per service
- Kubernetes-native architecture
- Load balancing at service level
- Independent database connections
- Distributed task processing

---

## 9. DEPLOYMENT COMPARISON

### Original Sim Deployment

```
Option 1: Vercel
- Auto-deploys from Git
- Built-in CDN
- Serverless functions
- Environment management

Option 2: Self-hosted
- Single Node.js container
- Bun runtime
- Database migrations
- Redis instance

Single Deployment Unit:
- app (frontend + backend)
- database (PostgreSQL)
- cache (Redis)
```

### New Pankh.AI Deployment

```
Multiple Deployment Units:

1. Backend Service
   - FastAPI + Uvicorn
   - Async workers
   - Environment variables
   - Database migrations (Alembic)

2. Frontend Service
   - Static SPA built with Vite
   - CDN-friendly
   - Environment configuration

3. Worker Service
   - Celery workers
   - Multiple instances
   - Task queue (Redis)

4. Realtime Service
   - Socket.IO server
   - WebSocket connections
   - Session management

Infrastructure:
- PostgreSQL 17
- Redis 5
- Docker containers
- Kubernetes (or Docker Compose)
- Load balancer (nginx, etc.)
```

**Docker Compose Example:**
```yaml
services:
  postgres:
    image: postgres:17
  redis:
    image: redis:7
  backend:
    build: services/backend
    ports: [8000]
  frontend:
    build: services/frontend
    ports: [5173]
  worker:
    build: services/backend
    command: celery -A app.workers.celery_app worker
  beat:
    build: services/backend
    command: celery -A app.workers.celery_app beat
```

---

## 10. DEVELOPMENT EXPERIENCE

### Original Sim

**Setup:**
```bash
bun install
bun run dev
# Single command, everything starts
```

**Development Mode:**
- Hot Module Replacement (HMR) works well
- TypeScript errors shown immediately
- Single port (3000)
- Server and client hot reload
- Integrated Socket.IO server

**Debugging:**
- Chrome DevTools for frontend
- Node.js debugger for backend
- Server logs in console
- Single stack trace

---

### New Pankh.AI

**Setup:**
```bash
# Backend
cd services/backend
poetry install
poetry run uvicorn app.main:app --reload

# Frontend (another terminal)
cd services/frontend
npm install
npm run dev

# Workers (another terminal)
poetry run celery -A app.workers.celery_app worker

# Beat (another terminal)
poetry run celery -A app.workers.celery_app beat
```

**Development Mode:**
- Fast HMR (Vite)
- Python hot reload
- Multiple ports needed
- Clear service separation
- Socket.IO realtime development

**Debugging:**
- Python debugger for backend
- Chrome DevTools for frontend
- Separate console outputs
- Network calls visible
- Celery task monitoring
- Redis CLI for inspection

---

## 11. SUMMARY TABLE

| Aspect | Sim (Original) | Pankh.AI (New) |
|--------|---|---|
| **Architecture** | Monolithic | Microservices |
| **Backend Language** | TypeScript | Python |
| **Frontend Framework** | Next.js | React + Vite |
| **Database ORM** | Drizzle | SQLAlchemy |
| **Executor** | TypeScript (10K lines) | LangGraph (Python) |
| **Blocks** | 100+ TS | 15 Python (core) |
| **Workers** | Custom Socket.IO | Celery |
| **Realtime** | Built-in | Socket.IO service |
| **Authentication** | better-auth | fastapi-users |
| **API Endpoints** | 40+ | 20+ (core) |
| **Deployment** | Single container | Multi-container |
| **Scalability** | Vertical | Horizontal |
| **Package Manager** | Bun | Poetry + npm |
| **Build Tool** | Next.js | Vite + Poetry |
| **Development** | 1 process | 4+ processes |
| **Maturity** | Production-ready | MVP with extensions |

---

## 12. IMPLEMENTATION STATUS & GAPS

### Fully Implemented Features ✅
1. **Core Backend Services**
   - FastAPI REST API with 20+ endpoints
   - SQLAlchemy database models and migrations
   - JWT authentication (basic)
   - Workflow CRUD operations
   - Workflow execution engine (LangGraph)
   - 15 core block implementations

2. **Worker System**
   - Celery task queue with Redis
   - 5 main background tasks
   - 5 scheduled tasks (Celery Beat)
   - Task monitoring API endpoints

3. **Realtime Services**
   - Socket.IO server implementation
   - Room-based broadcasting
   - Execution progress updates
   - Multi-user collaboration support

4. **Development Infrastructure**
   - Docker Compose setup (dev & production)
   - Hot reload for development
   - Health checks for all services
   - Volume mounts for development

### Partially Implemented (Stubs/Placeholders) ⚠️

1. **Authentication System** - `services/backend/app/api/v1/auth.py`
   - ✅ Basic JWT login/register
   - ❌ OAuth providers (GitHub, Google, etc.)
   - ❌ SSO integration
   - ❌ Email verification flow
   - ❌ Password reset with email
   - **Status**: Stub endpoints exist, need full implementation

2. **Billing System** - `services/backend/app/api/v1/billing.py`
   - ❌ Stripe integration
   - ❌ Subscription management
   - ❌ Usage tracking
   - ❌ Invoice generation
   - **Status**: Endpoints defined but not implemented

3. **Frontend Pages** - `services/frontend/src/`
   - ✅ Basic App.tsx structure
   - ✅ UI component library (shadcn)
   - ❌ Workflow editor page
   - ❌ Authentication pages (login/signup)
   - ❌ Dashboard page
   - ❌ Settings pages
   - **Status**: Components available, pages need assembly

4. **AI Features**
   - ✅ Basic agent block with 3 providers
   - ❌ AI block generation from user description
   - ❌ AI copilot for workflow building
   - ❌ Knowledge base integration
   - **Status**: Core agent works, advanced features planned

### Not Yet Started ❌

1. **Chat Interface**
   - Chat UI component
   - Chat API endpoints
   - Chat history storage
   - File uploads in chat
   - **Location**: Would be in `services/backend/app/api/v1/chat.py` and `services/frontend/src/pages/chat/`

2. **Third-Party Integrations**
   - 30+ integration blocks from original Sim
   - OAuth connection management
   - Integration marketplace
   - **Location**: Would be in `services/backend/app/integrations/`

3. **Advanced Collaboration**
   - Cursor sharing
   - Comments and mentions
   - Activity feed
   - **Location**: Realtime service exists, features need implementation

4. **Knowledge Base**
   - Document storage
   - Vector embeddings
   - Semantic search
   - **Location**: Would be in `services/backend/app/services/knowledge/`

---

## 13. QUICK START GUIDE

### Prerequisites
- Docker and Docker Compose installed
- 8GB RAM minimum
- Ports available: 5173 (frontend), 8000 (backend), 5432 (postgres), 6379 (redis)

### Development Setup

**Option 1: Using Docker Compose (Recommended)**
```bash
# Start all services in development mode with hot reload
docker-compose -f docker-compose.dev.yml up --build

# Services will be available at:
# - Frontend: http://localhost:5173
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379
```

**Option 2: Manual Setup**
```bash
# Terminal 1: Backend
cd services/backend
poetry install
poetry run uvicorn app.main:app --reload

# Terminal 2: Worker
cd services/backend
poetry run celery -A app.workers.celery_app worker --loglevel=info

# Terminal 3: Beat Scheduler
cd services/backend
poetry run celery -A app.workers.celery_app beat --loglevel=info

# Terminal 4: Frontend
cd services/frontend
npm install
npm run dev
```

### Testing the Setup
```bash
# Check backend health
curl http://localhost:8000/health

# Check API documentation
open http://localhost:8000/docs

# Check frontend
open http://localhost:5173
```

---

## 14. KNOWN ISSUES & TROUBLESHOOTING

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   netstat -ano | findstr :8000  # Windows
   lsof -i :8000                 # Mac/Linux

   # Kill the process or change ports in docker-compose.dev.yml
   ```

2. **Database Connection Refused**
   - Ensure PostgreSQL container is healthy
   - Check DATABASE_URL environment variable
   - Verify network connectivity: `docker-compose ps`

3. **Frontend Can't Connect to Backend**
   - Verify VITE_API_BASE_URL in frontend environment
   - Check CORS settings in backend
   - Ensure backend is running: `curl http://localhost:8000/health`

4. **Celery Worker Not Processing Tasks**
   - Check Redis connection
   - Verify CELERY_BROKER_URL is correct
   - Check worker logs: `docker-compose logs worker`

5. **Hot Reload Not Working**
   - Verify volume mounts in docker-compose.dev.yml
   - On Windows, ensure file sharing is enabled in Docker Desktop
   - Check file permissions

### Getting Help
- Check logs: `docker-compose -f docker-compose.dev.yml logs [service-name]`
- View all containers: `docker-compose -f docker-compose.dev.yml ps`
- Restart specific service: `docker-compose -f docker-compose.dev.yml restart [service-name]`

---

## Conclusion

The migration from Sim to Pankh.AI represents a shift from a feature-complete monolithic application to a modern microservices architecture. While the original Sim includes 100+ block types and full feature set, Pankh.AI establishes a solid foundation with:

### Pankh.AI Advantages
- ✅ Cleaner separation of concerns
- ✅ Independent service scaling
- ✅ Production-ready workers and realtime
- ✅ Python for better AI/ML integration
- ✅ Container-native architecture
- ✅ Modern async patterns
- ✅ Docker-based deployment ready

### Missing from Pankh.AI (Planned)
- ⚠️ Full block library (100+ vs 15) - 85% remaining
- ⚠️ Advanced AI features (generation, copilot) - In planning
- ⚠️ Complete authentication (OAuth/SSO) - Stubs exist
- ⚠️ Integrations (30+ third-party) - Not started
- ⚠️ Chat interface - Not started
- ⚠️ Billing system - Stubs exist
- ⚠️ Frontend pages - Components ready, assembly needed

### Next Steps
1. Complete frontend page assembly using existing UI components
2. Implement authentication OAuth/SSO flows
3. Complete billing integration with Stripe
4. Port remaining 85+ block types from original Sim
5. Add AI block generation and copilot features
6. Build chat interface and knowledge base
7. Add third-party integrations

The new architecture is more maintainable, scalable, and follows modern cloud-native patterns, making it ideal for growth and feature expansion.
