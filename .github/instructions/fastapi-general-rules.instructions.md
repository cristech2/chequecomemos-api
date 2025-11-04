---
description: 'FastAPI core rules, best practices, and architecture guidelines for building clean, maintainable APIs'
applyTo: '**/*.py'
---

# FastAPI Development Guidelines

Complete guide for developing FastAPI applications following industry best practices, clean code principles, and proven architectural patterns.

## Coding Foundations

- Focus on writing **clean and maintainable FastAPI code**
- Apply **Python best practices** and use **type hints** everywhere to improve IDE support and validation
- Leverage Python 3.12+ features for modern, efficient code
- Prioritize readability and maintainability over clever solutions

## Project Structure & Architecture

### Recommended Folder Structure

```
app/
├── api/
│   ├── v1/
│   │   ├── endpoints/
│   │   │   ├── users.py
│   │   │   └── items.py
│   │   └── dependencies.py
│   └── v2/
├── core/
│   ├── config.py
│   ├── security.py
│   └── database.py
├── models/
│   ├── user.py
│   └── item.py
├── services/
│   ├── user_service.py
│   └── item_service.py
└── main.py
```

### Architecture Principles

- **Separation of Concerns**: Clear boundaries between layers (API, business logic, data access)
- **Maintainability**: Organize code into logical modules that are easy to understand and modify
- **Scalability**: Design structure to support application growth without major refactoring
- **Reusability**: Create shared components (dependencies, utilities, services) to avoid duplication

### Directory Purposes

- **`app/api/`**: API endpoints and versioning (`v1/`, `v2/`)
- **`app/api/dependencies/`**: Reusable dependencies (authentication, database sessions)
- **`app/core/`**: Core modules (configuration, security, database sessions)
- **`app/models/`**: SQLModel definitions for ORM and Pydantic validation
- **`app/services/`**: Business logic layer
- **`main.py`**: Application entry point using the application factory pattern (`create_app()`)

## FastAPI Framework Rules

### Models and Schemas

#### SQLModel Usage

- Use SQLModel as the **single source of truth** for: database models, data validation, serialization, and API documentation
- Unify the domain model (database) and API schema in a single SQLModel class to avoid duplication (DRY principle)
- Create separate **DTO schemas** for input (Create/Update) and output (Read)
  - These can inherit from the base model or be Pydantic `BaseModel`
  - Prevents data leaks (e.g., hiding `password_hash`)
  - Use in `response_model` for proper serialization

#### Model Configuration

```python
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict

class User(SQLModel, table=True):
    """User database model"""
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    name: str
    password_hash: str
    is_active: bool = Field(default=True)

class UserRead(SQLModel):
    """User response schema - excludes sensitive data"""
    id: int
    email: str
    name: str
    is_active: bool

class UserCreate(SQLModel):
    """User creation schema"""
    email: str
    name: str
    password: str
```

### Path Operations & Routers

#### RESTful Principles

- Follow **RESTful design patterns** for all endpoints
- Always specify `response_model` for type validation and documentation
- Set appropriate `status_code` (200, 201, 204, etc.)
- Include `tags`, `summary`, and `description` for OpenAPI documentation

#### Good Example - Proper Endpoint Definition

```python
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserRead], status_code=status.HTTP_200_OK)
async def list_users(
    session: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = 10
):
    """Retrieve all users with pagination"""
    users = await UserService.get_users(session, skip, limit)
    return users

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create a new user"""
    user = await UserService.create_user(session, user_data)
    return user
```

#### Bad Example - Avoid These Patterns

```python
# ❌ Missing response_model - loses type validation
@router.get("/users")
async def get_users():
    return users

# ❌ Missing status_code
@router.post("/users", response_model=UserRead)
async def create_user(data: UserCreate):
    pass

# ❌ No documentation
@router.get("/users/{user_id}")
async def get(u: int):
    pass
```

#### Router Organization

- Organize large applications into **modular routers**
- Use `prefix` for URL grouping (e.g., `/api/v1/users`)
- Use `tags` for API documentation organization
- Include `include_in_schema` to hide internal endpoints if needed

```python
router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}}
)
```

### Dependencies and Asynchrony

#### Dependency Injection

- Use `Depends()` for database sessions, configuration, authentication, and reusable logic
- Make dependencies **async** for I/O-bound operations
- Design dependencies to be **testable** and easily replaceable during testing

#### Good Example - Dependency Pattern

```python
async def get_session() -> AsyncSession:
    """Provide database session for route handlers"""
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session)
) -> User:
    """Authenticate and return current user"""
    user = await verify_token(token, session)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@router.get("/profile", response_model=UserRead)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user
```

#### Asynchronous Functions

- Use `async def` for route handlers and I/O-bound dependencies
- Ensure proper use of `await` for async operations
- Avoid blocking the event loop with CPU-intensive tasks
- Offload heavy computations to background tasks or worker processes

#### Bad Example - Blocking Operations

```python
# ❌ Blocks the event loop
@router.post("/process")
async def process_data(data: DataModel):
    for i in range(1000000):  # CPU-intensive
        result = expensive_calculation(i)
    return result

# ✅ Better: Offload to background task
from fastapi import BackgroundTasks

@router.post("/process")
async def process_data(data: DataModel, background_tasks: BackgroundTasks):
    background_tasks.add_task(expensive_operation, data)
    return {"status": "Processing"}
```

### Lifecycle and Concurrency

#### Lifecycle Events

- Use `startup` and `shutdown` events for **resource initialization and cleanup**
- Examples: database connections, background task workers, external service connections

```python
@app.on_event("startup")
async def startup():
    """Initialize resources on application startup"""
    app.db_pool = create_connection_pool()
    app.redis = await aioredis.create_redis_pool()

@app.on_event("shutdown")
async def shutdown():
    """Clean up resources on application shutdown"""
    await app.db_pool.close()
    app.redis.close()
```

#### Background Tasks

- Use `BackgroundTasks` for **non-blocking operations** after sending response
- Examples: email sending, data processing, logging
- Avoid long-running tasks; use job queues (Celery, RQ) for complex workflows

```python
from fastapi import BackgroundTasks

@router.post("/notify")
async def send_notification(
    user_id: int,
    background_tasks: BackgroundTasks
):
    """Send notification in background"""
    background_tasks.add_task(send_email, user_id)
    return {"status": "Notification queued"}
```

## Common Patterns

### Service Layer Pattern

Implement business logic in dedicated service classes:

```python
class UserService:
    @staticmethod
    async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
        """Create user with proper validation and error handling"""
        existing = await session.execute(
            select(User).where(User.email == user_data.email)
        )
        if existing.scalars().first():
            raise ValueError("User already exists")

        user = User(**user_data.model_dump(), password_hash=hash_password(user_data.password))
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
```

### Error Handling

Implement consistent error handling with appropriate HTTP status codes:

```python
from fastapi import HTTPException, status

@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await UserService.get_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
```

## Validation and Verification

- Run tests: `pytest`
- Format code: `black app/`
- Type checking: `mypy app/`
- Linting: `ruff check app/`
