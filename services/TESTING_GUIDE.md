# End-to-End Testing Guide - Pankh.AI Services

This guide provides comprehensive testing procedures for all implemented features.

---

## 🚀 Prerequisites

### Backend Setup
```bash
cd services/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://user:password@localhost:5432/pankhdb"
export REDIS_URL="redis://localhost:6379/0"
export SECRET_KEY="your-secret-key-here"
export CREDENTIAL_ENCRYPTION_KEY="$(python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')"

# Run database migrations (if Alembic is set up)
alembic upgrade head

# Start the backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd services/frontend

# Install dependencies
npm install --legacy-peer-deps

# Set environment variable
export VITE_API_URL="http://localhost:8000/api/v1"

# Start the frontend
npm run dev
```

### Worker Setup (separate terminal)
```bash
cd services/backend
source venv/bin/activate

# Start Celery worker
celery -A app.workers.celery_app worker --loglevel=info

# Start Celery Beat (scheduler) - optional
celery -A app.workers.celery_app beat --loglevel=info
```

---

## 📋 Test Plan

### 1. Backend API Health Check

**Test**: Verify backend is running
```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy"}

curl http://localhost:8000/api/v1/
# Expected: API documentation or service info
```

**Test**: Check OpenAPI documentation
```bash
# Open in browser
open http://localhost:8000/docs
# Should show interactive API documentation
```

---

### 2. Authentication Tests

**Test**: User registration (if endpoint exists)
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePassword123!",
    "name": "Test User"
  }'
```

**Test**: User login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePassword123!"
  }'
# Expected: {"access_token": "...", "token_type": "bearer"}

# Save the token
export AUTH_TOKEN="<token-from-response>"
```

---

### 3. Workflow API Tests

**Test**: List workflows
```bash
curl http://localhost:8000/api/v1/workflows/ \
  -H "Authorization: Bearer $AUTH_TOKEN"
# Expected: {"workflows": [...], "count": 0}
```

**Test**: Create a workflow
```bash
curl -X POST http://localhost:8000/api/v1/workflows/ \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Workflow",
    "description": "End-to-end test workflow",
    "blocks": [],
    "edges": []
  }'
# Expected: {"id": "...", "name": "Test Workflow", ...}

# Save workflow ID
export WORKFLOW_ID="<id-from-response>"
```

**Test**: Get workflow details
```bash
curl http://localhost:8000/api/v1/workflows/$WORKFLOW_ID \
  -H "Authorization: Bearer $AUTH_TOKEN"
```

**Test**: Update workflow
```bash
curl -X PATCH http://localhost:8000/api/v1/workflows/$WORKFLOW_ID \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Test Workflow",
    "blocks": [
      {
        "id": "block1",
        "type": "openai",
        "data": {
          "action": "chat",
          "model": "gpt-4",
          "messages": [{"role": "user", "content": "Hello"}]
        }
      }
    ]
  }'
```

---

### 4. Block Metadata Tests

**Test**: List all available blocks
```bash
curl http://localhost:8000/api/v1/blocks/ \
  -H "Authorization: Bearer $AUTH_TOKEN"
# Expected: List of 90+ block definitions
```

**Test**: Get specific block metadata
```bash
curl http://localhost:8000/api/v1/blocks/openai \
  -H "Authorization: Bearer $AUTH_TOKEN"
# Expected: OpenAI block metadata with fields, actions
```

**Test**: Get blocks by category
```bash
curl http://localhost:8000/api/v1/blocks/category/ai \
  -H "Authorization: Bearer $AUTH_TOKEN"
# Expected: AI-related blocks (openai, anthropic, etc.)
```

---

### 5. Credential Management Tests

**Test**: Store OpenAI credential
```bash
curl -X POST http://localhost:8000/api/v1/credentials/ \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "OpenAI Production Key",
    "service": "openai",
    "type": "api_key",
    "value": "sk-test-key-12345",
    "expiresInDays": 90
  }'
# Expected: {"id": "...", "service": "openai", "isExpired": false}

export CREDENTIAL_ID="<id-from-response>"
```

**Test**: List credentials
```bash
curl http://localhost:8000/api/v1/credentials/ \
  -H "Authorization: Bearer $AUTH_TOKEN"
# Expected: [{"id": "...", "service": "openai", ...}]
```

**Test**: Validate credential for service
```bash
curl http://localhost:8000/api/v1/credentials/validate/openai \
  -H "Authorization: Bearer $AUTH_TOKEN"
# Expected: {"isValid": true, "error": null}
```

**Test**: Update credential
```bash
curl -X PATCH http://localhost:8000/api/v1/credentials/$CREDENTIAL_ID \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {"environment": "production"}
  }'
```

**Test**: Delete credential
```bash
curl -X DELETE http://localhost:8000/api/v1/credentials/$CREDENTIAL_ID \
  -H "Authorization: Bearer $AUTH_TOKEN"
# Expected: {"id": "...", "deleted": true}
```

---

### 6. Chat API Tests

**Test**: Send chat message
```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, can you help me build a workflow?"
  }'
# Expected: {"conversationId": "...", "message": "...", "role": "assistant"}

export CONVERSATION_ID="<conversationId-from-response>"
```

**Test**: Continue conversation
```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to automate sending Slack messages",
    "conversationId": "'$CONVERSATION_ID'"
  }'
```

**Test**: Get conversation history
```bash
curl http://localhost:8000/api/v1/chat/$CONVERSATION_ID/history \
  -H "Authorization: Bearer $AUTH_TOKEN"
# Expected: {"conversationId": "...", "messages": [...]}
```

---

### 7. Copilot API Tests

**Test**: Get block suggestions
```bash
curl -X POST http://localhost:8000/api/v1/copilot/suggest \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Send a Slack message when a form is submitted",
    "action": "suggest"
  }'
# Expected: {"suggestions": [...], "explanation": "..."}
```

**Test**: Generate custom block
```bash
curl -X POST http://localhost:8000/api/v1/copilot/generate-block \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Convert JSON to CSV format",
    "inputs": ["jsonData"],
    "outputs": ["csvData"],
    "language": "python"
  }'
# Expected: {"type": "custom_code", "code": "...", "testCases": [...]}
```

**Test**: Explain workflow
```bash
curl -X POST "http://localhost:8000/api/v1/copilot/explain?workflow_id=$WORKFLOW_ID" \
  -H "Authorization: Bearer $AUTH_TOKEN"
# Expected: Explanation of what the workflow does
```

---

### 8. Workflow Execution Tests

**Test**: Execute workflow manually
```bash
curl -X POST http://localhost:8000/api/v1/workflows/$WORKFLOW_ID/execute \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "inputData": {
      "message": "Hello from test"
    }
  }'
# Expected: {"executionId": "...", "status": "running"}

export EXECUTION_ID="<executionId-from-response>"
```

**Test**: Get execution status
```bash
curl http://localhost:8000/api/v1/executions/$EXECUTION_ID \
  -H "Authorization: Bearer $AUTH_TOKEN"
# Expected: {"id": "...", "status": "completed|failed|running", "result": {...}}
```

**Test**: List workflow executions
```bash
curl http://localhost:8000/api/v1/workflows/$WORKFLOW_ID/executions \
  -H "Authorization: Bearer $AUTH_TOKEN"
# Expected: [{"id": "...", "status": "...", "createdAt": "..."}]
```

---

### 9. Integration Block Tests

#### OpenAI Block
```bash
# Test via workflow execution
curl -X POST http://localhost:8000/api/v1/workflows/ \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "OpenAI Test Workflow",
    "blocks": [
      {
        "id": "openai1",
        "type": "openai",
        "data": {
          "action": "chat",
          "model": "gpt-4",
          "messages": [
            {"role": "user", "content": "Say hello in 5 words"}
          ]
        }
      }
    ],
    "edges": []
  }'
# Then execute the workflow
```

#### Slack Block
```bash
# Create workflow with Slack block
curl -X POST http://localhost:8000/api/v1/workflows/ \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Slack Test Workflow",
    "blocks": [
      {
        "id": "slack1",
        "type": "slack",
        "data": {
          "action": "send_message",
          "channel": "#general",
          "text": "Test message from Pankh.AI"
        }
      }
    ]
  }'
```

#### GitHub Block
```bash
# Create workflow with GitHub block
curl -X POST http://localhost:8000/api/v1/workflows/ \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "GitHub Test Workflow",
    "blocks": [
      {
        "id": "github1",
        "type": "github",
        "data": {
          "action": "create_issue",
          "owner": "your-org",
          "repo": "your-repo",
          "title": "Test issue from Pankh.AI",
          "body": "This is a test issue"
        }
      }
    ]
  }'
```

---

### 10. Frontend Tests

**Test**: Open frontend in browser
```bash
# Navigate to http://localhost:5173
```

**Manual UI Tests**:
1. ✅ Login page loads
2. ✅ Dashboard shows workflows
3. ✅ Click "New Workflow" button
4. ✅ Workflow creation dialog appears
5. ✅ Enter workflow name and create
6. ✅ Workflow editor canvas loads
7. ✅ Block library panel shows on left
8. ✅ Drag block onto canvas
9. ✅ Click block to configure
10. ✅ Configuration panel opens on right
11. ✅ Connect blocks with edges
12. ✅ Save workflow
13. ✅ Execute workflow
14. ✅ View execution logs
15. ✅ Navigate to Chat page
16. ✅ Send message to AI
17. ✅ Receive response
18. ✅ Navigate to Settings (if exists)
19. ✅ Manage credentials

---

### 11. WebSocket/Real-time Tests

**Test**: Connect to WebSocket
```javascript
// In browser console at http://localhost:5173
const socket = io('http://localhost:8000');

socket.on('connect', () => {
  console.log('Connected to WebSocket');
});

socket.on('execution_update', (data) => {
  console.log('Execution update:', data);
});

socket.on('workflow_update', (data) => {
  console.log('Workflow update:', data);
});
```

**Test**: Execute workflow and watch real-time updates
```bash
# In one terminal, execute workflow
curl -X POST http://localhost:8000/api/v1/workflows/$WORKFLOW_ID/execute \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -d '{"inputData": {}}'

# In browser console, you should see execution_update events
```

---

### 12. Celery Worker Tests

**Test**: Check Celery worker is processing tasks
```bash
# In worker terminal, you should see:
# [INFO] Task app.workers.tasks.execute_workflow[...] received
# [INFO] Task app.workers.tasks.execute_workflow[...] succeeded

# Check Celery inspect
celery -A app.workers.celery_app inspect active
# Expected: List of active tasks

celery -A app.workers.celery_app inspect stats
# Expected: Worker statistics
```

---

## 🔍 Validation Checklist

### Backend Services
- [ ] FastAPI server starts without errors
- [ ] OpenAPI docs accessible at /docs
- [ ] All routers registered (auth, workflows, blocks, credentials, chat, copilot)
- [ ] Database connection successful
- [ ] Redis connection successful

### Frontend
- [ ] Vite dev server starts
- [ ] React app loads in browser
- [ ] No console errors
- [ ] API calls reach backend (check Network tab)
- [ ] WebSocket connection established

### Workers
- [ ] Celery worker starts
- [ ] Worker connects to Redis broker
- [ ] Tasks are discovered and registered
- [ ] Test task executes successfully

### Integration Executors
- [ ] OpenAI executor can make API calls
- [ ] Anthropic executor handles Claude requests
- [ ] Slack executor can send messages
- [ ] Gmail executor can send emails
- [ ] GitHub executor can create issues
- [ ] Notion executor can query databases
- [ ] Google Sheets executor can read/write

### Credential Management
- [ ] Can store credentials securely
- [ ] Credentials are encrypted at rest
- [ ] Can retrieve credentials
- [ ] Can update credentials
- [ ] Can delete credentials
- [ ] Expiration handling works

### Chat & Copilot
- [ ] Chat messages get AI responses
- [ ] Conversation context is maintained
- [ ] Copilot provides block suggestions
- [ ] Custom block generation works
- [ ] Workflow explanations are helpful

---

## 🐛 Common Issues & Solutions

### Issue: Database connection fails
**Solution**:
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Or with Docker
docker ps | grep postgres

# Verify connection string
export DATABASE_URL="postgresql://user:password@localhost:5432/pankhdb"
```

### Issue: Redis connection fails
**Solution**:
```bash
# Check Redis is running
sudo systemctl status redis

# Or with Docker
docker ps | grep redis

# Test connection
redis-cli ping
# Expected: PONG
```

### Issue: CORS errors in browser
**Solution**:
```python
# In services/backend/app/main.py, ensure CORS is configured:
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: Import errors in Python
**Solution**:
```bash
# Ensure you're in the correct directory
cd services/backend

# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Frontend build errors
**Solution**:
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

### Issue: Celery tasks not executing
**Solution**:
```bash
# Check worker is running
celery -A app.workers.celery_app inspect active

# Restart worker with debug logging
celery -A app.workers.celery_app worker --loglevel=debug

# Check Redis queue
redis-cli LLEN celery
```

---

## 📊 Performance Testing

### Load Test with Locust
```python
# Create locustfile.py
from locust import HttpUser, task, between

class WorkflowUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # Login and get token
        response = self.client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "password"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def list_workflows(self):
        self.client.get("/api/v1/workflows/", headers=self.headers)

    @task(2)
    def get_blocks(self):
        self.client.get("/api/v1/blocks/", headers=self.headers)

    @task(1)
    def execute_workflow(self):
        self.client.post("/api/v1/workflows/test-id/execute",
                        headers=self.headers,
                        json={"inputData": {}})
```

Run load test:
```bash
locust -f locustfile.py --host=http://localhost:8000
# Open http://localhost:8089 for UI
```

---

## 🎯 Success Criteria

The system passes end-to-end testing if:

1. ✅ All API endpoints return expected responses
2. ✅ Frontend loads and is interactive
3. ✅ Workflows can be created and edited
4. ✅ Workflow execution completes successfully
5. ✅ Integration blocks execute without errors
6. ✅ Credentials are stored and retrieved securely
7. ✅ Chat provides AI responses
8. ✅ Copilot suggests relevant blocks
9. ✅ Real-time updates work via WebSocket
10. ✅ No critical errors in logs

---

## 📝 Test Results Template

```markdown
## Test Results - [Date]

### Environment
- Backend: Running on port 8000
- Frontend: Running on port 5173
- Database: PostgreSQL 14
- Redis: 7.0
- Workers: 1 Celery worker

### Test Summary
- Total Tests: 50
- Passed: 48
- Failed: 2
- Skipped: 0

### Failed Tests
1. Test Name: GitHub integration executor
   - Error: Authentication failed
   - Fix: Need to add valid GitHub token to credentials

2. Test Name: WebSocket reconnection
   - Error: Connection drops after 30s
   - Fix: Adjust Socket.IO ping timeout

### Performance Metrics
- API Response Time (p95): 150ms
- Workflow Execution Time: 2.3s average
- Frontend Load Time: 1.2s
- WebSocket Latency: 50ms

### Notes
- All core features working correctly
- Minor issues with external API integrations (expected without real credentials)
- System is stable under moderate load
```

---

**Next Steps**: Run through this testing guide systematically and document any issues you encounter!
