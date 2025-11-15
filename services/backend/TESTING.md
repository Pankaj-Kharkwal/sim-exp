# Testing Guide for Pankh.AI Backend

This document describes the testing strategy and how to run tests for the Pankh.AI backend service.

## 🎯 Testing Strategy

### Test Coverage
- **Unit Tests**: Individual functions and classes
- **Integration Tests**: Database models and API endpoints
- **Executor Tests**: Workflow execution engine
- **End-to-End Tests**: Full workflow execution scenarios

### Testing Stack
- **pytest**: Test framework
- **pytest-asyncio**: Async test support
- **pytest-cov**: Coverage reporting
- **httpx**: HTTP client for API testing
- **SQLAlchemy async**: Database testing

## 🚀 Quick Start

### Prerequisites
1. Python 3.11+
2. Poetry package manager
3. PostgreSQL 17 (for integration tests)
4. Redis (optional, for integration tests)

### Installation

```bash
cd services/backend

# Install dependencies
poetry install

# Or install with dev dependencies explicitly
poetry install --with dev
```

## 🧪 Running Tests

### All Tests

**Linux/Mac:**
```bash
chmod +x scripts/test.sh
./scripts/test.sh
```

**Windows:**
```powershell
.\scripts\test.ps1
```

**Manual:**
```bash
poetry run pytest tests/ -v
```

### Specific Test Files

```bash
# Test models only
poetry run pytest tests/test_models.py -v

# Test executor only
poetry run pytest tests/test_executor.py -v

# Test health check
poetry run pytest tests/test_health.py -v
```

### With Coverage

```bash
# Generate coverage report
poetry run pytest tests/ \
    --cov=app \
    --cov-report=term-missing \
    --cov-report=html \
    -v

# View HTML coverage report
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Watch Mode

```bash
# Auto-run tests on file changes
poetry run ptw tests/ app/
```

## 📊 Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures and configuration
├── test_health.py           # Health check endpoint tests
├── test_models.py           # Database model tests
├── test_executor.py         # Workflow executor tests
├── test_api/                # API endpoint tests (future)
│   ├── test_auth.py
│   ├── test_workflows.py
│   └── test_blocks.py
└── test_services/           # Service layer tests (future)
    └── test_workflow_execution.py
```

## 🔧 Test Configuration

### Database Setup

Tests use a separate test database to avoid polluting development data:

```python
# In conftest.py
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/pankhai_test"
```

**Create test database:**
```bash
createdb pankhai_test
```

### Environment Variables for Testing

```bash
# .env.test (optional)
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/pankhai_test
REDIS_URL=redis://localhost:6379/1
SECRET_KEY=test-secret-key
ENCRYPTION_KEY=test-encryption-key
LOG_LEVEL=WARNING
```

## 📝 Writing Tests

### Example: Testing a Model

```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.workflow import Workflow

@pytest.mark.asyncio
async def test_create_workflow(db_session: AsyncSession):
    workflow = Workflow(
        id="test-id",
        name="Test Workflow",
        user_id="user-123",
    )

    db_session.add(workflow)
    await db_session.commit()
    await db_session.refresh(workflow)

    assert workflow.id == "test-id"
    assert workflow.name == "Test Workflow"
```

### Example: Testing an API Endpoint

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_list_workflows(client: AsyncClient):
    response = await client.get("/api/v1/workflows")

    assert response.status_code == 200
    data = response.json()
    assert "workflows" in data
    assert isinstance(data["workflows"], list)
```

### Example: Testing the Executor

```python
import pytest
from app.executor.engine import WorkflowExecutor

@pytest.mark.asyncio
async def test_simple_workflow():
    executor = WorkflowExecutor()

    blocks = {
        "block-1": {
            "id": "block-1",
            "type": "response",
            "name": "Test",
            "enabled": True,
            "data": {"message": "Hello"},
        }
    }

    result = await executor.execute(
        workflow_id="test-wf",
        user_id="test-user",
        blocks=blocks,
        edges=[],
        input_data={},
    )

    assert result.status.value == "completed"
```

## 🔍 Code Quality Checks

### Black (Formatting)

```bash
# Check formatting
poetry run black --check app tests

# Auto-format code
poetry run black app tests
```

### Ruff (Linting)

```bash
# Check linting
poetry run ruff check app tests

# Auto-fix issues
poetry run ruff check --fix app tests
```

### MyPy (Type Checking)

```bash
# Run type checks
poetry run mypy app --ignore-missing-imports
```

## 🚦 CI/CD Integration

Tests run automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Changes to `services/backend/**` files

See [`.github/workflows/backend-ci.yml`](../../.github/workflows/backend-ci.yml)

## 📈 Coverage Goals

| Component | Target Coverage |
|-----------|----------------|
| Models | 90%+ |
| Executor | 85%+ |
| API Routes | 80%+ |
| Services | 85%+ |
| Overall | 80%+ |

## 🐛 Debugging Tests

### Run with Debug Output

```bash
# Verbose output
poetry run pytest tests/ -v

# Show print statements
poetry run pytest tests/ -s

# Stop on first failure
poetry run pytest tests/ -x

# Run specific test
poetry run pytest tests/test_models.py::test_create_user -v
```

### Use pdb for Debugging

```python
def test_something():
    import pdb; pdb.set_trace()  # Breakpoint
    # ... test code
```

### Check SQL Queries

```bash
# Enable SQL echo in tests
DB_ECHO=true poetry run pytest tests/ -v
```

## 🔄 Continuous Testing

For development, use pytest-watch:

```bash
# Install pytest-watch
poetry add --group dev pytest-watch

# Run in watch mode
poetry run ptw tests/ app/
```

## 📚 Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

## 🤝 Contributing

When adding new features:
1. Write tests first (TDD approach recommended)
2. Ensure all tests pass: `./scripts/test.sh`
3. Maintain or improve coverage
4. Follow existing test patterns

## 💡 Best Practices

1. **Isolation**: Each test should be independent
2. **Fixtures**: Use pytest fixtures for common setup
3. **Naming**: Use descriptive test names: `test_<what>_<condition>_<expected>`
4. **AAA Pattern**: Arrange, Act, Assert
5. **Async**: Always use `@pytest.mark.asyncio` for async tests
6. **Cleanup**: Use fixtures for database cleanup
7. **Mock**: Mock external services (APIs, email, etc.)

---

**Last Updated**: 2025-01-10
**Maintained by**: Pankh.AI Team
