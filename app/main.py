from fastapi import FastAPI
from app.core.config import get_settings
from app.api.routes import auth, todos
from app.middlewares.rate_limit import limiter, rate_limit_exceeded_handler
from app.middlewares.timing import TimingMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.models import base, user, todo  # noqa: F401
from app.exceptions.handlers import unhandled_exception_handler
from app.db.session import engine

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(TimingMiddleware)

# CORS (allow all for simplicity; adjust in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(todos.router)

# Global fallback handler
app.add_exception_handler(Exception, unhandled_exception_handler)

@app.get("/health")
async def health():
    return {"status": "ok"}

# Simple lifespan event to create tables (for demo; prefer Alembic in real apps)
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(base.Base.metadata.create_all)
