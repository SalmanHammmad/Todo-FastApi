from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi import Request
from app.core.config import get_settings

settings = get_settings()

# Default global limit (configurable via env RATE_LIMIT like 20/minute)
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])

async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
