# API Reference

This document provides a reference for the API endpoints used in the Pankh.AI platform.

## Base URL

-   **Development:** `http://localhost:8000`
-   **Production:** `https://api.pankh.ai` (example)

## API Version

-   `/api/v1`

---

## Authentication Endpoints

### POST `/api/v1/auth/login`

Login user and get JWT tokens.

**Request:**

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "organization_id": "org_123",
    "is_active": true
  }
}
```

### POST `/api/v1/auth/register`

Register new user.

**Request:**

```json
{
  "email": "newuser@example.com",
  "password": "securepass123",
  "name": "Jane Smith",
  "organization_name": "My Company"
}
```

### POST `/api/v1/auth/refresh`

Refresh access token.

**Request:**

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### POST `/api/v1/auth/logout`

Logout user (invalidate tokens).

**Headers:**

```
Authorization: Bearer {access_token}
```

### GET `/api/v1/auth/me`

Get current user info.

**Headers:**

```
Authorization: Bearer {access_token}
```

---

## Workflow Endpoints

### GET `/api/v1/workflows`

List all workflows with pagination.

**Query Parameters:**

-   `page`: number (default: 1)
-   `limit`: number (default: 20)
-   `search`: string (optional)
-   `is_deployed`: boolean (optional)

### POST `/api/v1/workflows`

Create new workflow.

**Request:**

```json
{
  "name": "New Workflow",
  "description": "My new workflow",
  "blocks": [],
  "edges": [],
  "variables": {}
}
```

### PUT `/api/v1/workflows/{workflow_id}`

Update workflow.

### DELETE `/api/v1/workflows/{workflow_id}`

Delete workflow.

### POST `/api/v1/workflows/{workflow_id}/deploy`

Deploy workflow to production.

---

## Execution Endpoints

### POST `/api/v1/workflows/{workflow_id}/execute`

Execute workflow synchronously.

**Request:**

```json
{
  "input": {
    "user": {
      "name": "John Doe",
      "email": "john@example.com"
    }
  },
  "stream": false
}
```

### POST `/api/v1/workflows/{workflow_id}/execute-async`

Execute workflow asynchronously.

### GET `/api/v1/executions`

List executions with filters.

### GET `/api/v1/executions/{execution_id}`

Get execution details.

### GET `/api/v1/executions/{execution_id}/logs`

Get execution logs.

### POST `/api/v1/executions/{execution_id}/cancel`

Cancel running execution.

---

## Background Tasks Endpoints

### GET `/api/v1/tasks`

List active background tasks.

### GET `/api/v1/tasks/{task_id}`

Get task status.

### POST `/api/v1/tasks/{task_id}/cancel`

Cancel background task.

### GET `/api/v1/tasks/stats/workers`

Get worker statistics.

### GET `/api/v1/tasks/stats/queues`

Get queue statistics.

---

## Blocks Endpoints

### GET `/api/v1/blocks`

List available block types.

### GET `/api/v1/blocks/{block_type}`

Get block type details and schema.

---

## Socket.IO Events

### Connection

-   **Client → Server:** `socket.connect({ auth: { token: 'jwt_access_token_here' } });`
-   **Server → Client:** `connect`, `disconnect`, `error`

### Workflow Collaboration

-   **Join Workflow:** `join_workflow`
-   **Leave Workflow:** `leave_workflow`
-   **Cursor Movement:** `cursor_move`
-   **Selection Changes:** `selection_change`

### Execution Monitoring

-   **Join Execution:** `join_execution`
-   **Execution Events:** `execution_started`, `execution_progress`, `execution_completed`

### System Notifications

-   `system_notification`

---

## Additional API Content

### Migration Quick Reference

Content from `MIGRATION_QUICK_REFERENCE.md`.

### Progress Updates

Content from `MIGRATION_PROGRESS_UPDATE.md`.
