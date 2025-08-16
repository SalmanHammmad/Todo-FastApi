# Todo FastAPI Project

Async FastAPI Todo list using DAO pattern, PostgreSQL, JWT auth, pagination, rate limiting, and good practices.

## Features
- Async SQLAlchemy with PostgreSQL (`asyncpg`)
- DAO pattern for data access isolation
- JWT authentication (stateless access token)
- Simple password hashing (bcrypt via passlib)
- Pagination (page & size query params)
- Rate limiting (global + per-route possible) via `slowapi`
- CORS middleware
- Centralized custom exceptions
- Pydantic v2 schemas
- Simple startup table creation (replace with Alembic migrations in production)

## Quick Start

### 1. Environment
Create `.env` (optional overrides):
```
DATABASE_URL=postgresql+asyncpg://postgres:6902@localhost:5432/todo
JWT_SECRET=change_me
ENVIRONMENT=dev
```

### 2. Install deps
Using Poetry:
```
poetry install
poetry run uvicorn app.main:app --reload
```

Or with pip (fallback):
```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. Endpoints
- POST /auth/register
- POST /auth/login
- GET /todos?page=1&size=10 (auth)
- POST /todos (auth)
- GET /todos/{id} (auth)
- PATCH /todos/{id} (auth)
- DELETE /todos/{id} (auth)

Auth: Include header `Authorization: Bearer <token>` after login.

### 4. Rate Limiting
Global limiter currently set in code; customize in `middlewares/rate_limit.py` or apply per-route:
```
from app.middlewares.rate_limit import limiter

@router.get("/todos")
@limiter.limit("5/minute")
async def list_todos(...):
    ...
```

### 5. DAO Pattern
All DB access is encapsulated in `dao/*.py` keeping routes thin and testable.

### 6. Tests (add later)
Basic test skeleton can be added to `app/tests`.

## Notes
- For production use: add refresh tokens, revoke strategy, structured logging, Alembic migrations, and stricter CORS.
- This demo creates tables automatically; remove that for real deployments.
