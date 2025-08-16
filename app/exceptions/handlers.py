from fastapi import Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger("errors")

async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
