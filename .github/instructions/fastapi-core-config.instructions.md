---
description: 'FastAPI core configuration, security, exceptions, and middleware patterns'
applyTo: 'app/core/**/*.py'
---

## Core Module Structure

The `app/core` module must contain all global configurations, database management, security, and application-level exception handlers.

### 1. Global Configuration (`app/core/config.py`)

Use **Pydantic's `BaseSettings`** (Pydantic v2+: `pydantic-settings`) to load environment variables and separate configurations by environment (dev, test, prod).

**Requirements:**
- Import `BaseSettings` from `pydantic_settings` using absolute imports
- Implement environment variables for sensitive configurations
- Include: `APP_NAME`, `API_V1_STR`, `DEBUG`, `DATABASE_URL`, `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `ALGORITHM` as class constants
- Use `model_config = ConfigDict(env_file=".env")` for Pydantic 2.x
- Use UPPER_CASE for class constants (PEP 8)

**Pattern:**
```python
import pydantic_settings

class Settings(pydantic_settings.BaseSettings):
    """Application settings loaded from environment variables."""

    APP_NAME: str = "MyFastAPI"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

settings = Settings()
```

### 2. Asynchronous Database Configuration (`app/core/db.py`)

Implement asynchronous SQLAlchemy connection with `create_async_engine` and `sessionmaker` for session factory.

**Requirements:**
- Import from `sqlalchemy` and `sqlalchemy.ext.asyncio` using absolute imports
- Configure connection pool: `pool_size=5`, `max_overflow=10`, `pool_timeout=30`
- Use `pool_pre_ping=True` to validate connections
- Use `async_sessionmaker` for creating `AsyncSessionLocal` factory
- Set `expire_on_commit=False` and `autoflush=False`

**Example structure:**
```python
import sqlalchemy
import sqlalchemy.ext.asyncio
import sqlalchemy.orm
from app.core import config

engine = sqlalchemy.ext.asyncio.create_async_engine(
    config.settings.database_url,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)

async_session_maker = sqlalchemy.orm.sessionmaker(
    engine,
    class_=sqlalchemy.ext.asyncio.AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)
```

### 3. Global Exceptions (`app/core/exceptions.py`)

Define custom exception classes to ensure consistent error responses.

**Requirements:**
- Create `ErrorResponse` model with: `status_code`, `message`, `details`, `request_id`
- Define custom exceptions (e.g., `NotFoundError`)
- Implement corresponding exception handlers
- Register handlers in `app/main.py`

### 4. Security and Hashing (`app/core/security.py`)

Handle cryptographic operations: password hashing (bcrypt) and JWT token creation/verification.

**Requirements:**
- Use `bcrypt` for password hashing
- Bcrypt operations are synchronous and blocking: use `asyncio.to_thread()` in async contexts
- Use `python-jose` for JWT: `create_access_token()` and `decode_access_token()`
- Include `exp` and `iat` in JWT claims
- Use `datetime.now(timezone.utc)` for timestamps
- Handle `JWTError` exceptions appropriately

**Key Functions:**
- `hash_password(password: str) -> str`: Hash a password using bcrypt (synchronous, use `asyncio.to_thread()` in async contexts)
- `verify_password(plain_password: str, hashed_password: str) -> bool`: Verify password against stored hash
- `create_access_token(data: dict, expires_delta: datetime.timedelta | None = None) -> str`: Create JWT access token with `exp` and `iat` claims
- `decode_access_token(token: str) -> dict`: Decode and validate JWT token, handle `JWTError` appropriately

---

## Application Startup and Middleware (`app/main.py` and `app/middleware/`)

### Application Factory Pattern

Use the **factory** pattern to initialize the application and include routers, middleware, and exception handlers.

**Structure in `app/main.py`:**
```
create_application() -> FastAPI
├── Add Middleware (order matters)
│   ├── RequestIDMiddleware (first, to trace everything)
│   └── CORSMiddleware
├── Register Exception Handlers
├── Include Routers (with API_V1_STR prefix)
└── Register Lifecycle Events (startup/shutdown)

app = create_application()
```

### Custom Middleware

Implement middleware for cross-cutting concerns:

**Requirements:**
- Inherit from `starlette.middleware.base.BaseHTTPMiddleware`
- Implement `async def dispatch(self, request: starlette.requests.Request, call_next)` method
- Use `request.state` to store data (e.g., `request_id`)
- Include `request_id` in error responses
- Use absolute imports from standard library and third-party packages

**Example: `app/middleware/request_id.py`**
```python
import uuid
import starlette.middleware.base
import starlette.requests
import starlette.responses
import starlette.types


class RequestIDMiddleware(starlette.middleware.base.BaseHTTPMiddleware):
    """Add unique request ID to all requests and responses."""

    async def dispatch(
        self,
        request: starlette.requests.Request,
        call_next: starlette.types.ASGIApp,
    ) -> starlette.responses.Response:
        """Attach request ID to request and response headers."""
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        try:
            response = await call_next(request)
        except Exception:
            response = starlette.responses.JSONResponse(
                status_code=500,
                content={"message": "Internal Server Error", "request_id": request_id},
            )

        response.headers["X-Request-ID"] = request_id
        return response
```

---

## Dependencies and Configuration

**Required Packages:**
- `fastapi`
- `sqlalchemy` (async)
- `pydantic-settings` (Pydantic v2)
- `bcrypt`
- `python-jose[cryptography]`

**Environment Variables (.env):**
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Key for signing JWT tokens
- `DEBUG`: Debug mode flag
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration in minutes (default: 30)
