import os
import asyncio
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.models import base
from app.db import session as session_module

# Switch to in-memory SQLite for tests
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from app.core.config import get_settings  # noqa: E402

settings = get_settings()

test_engine = create_async_engine(settings.database_url, echo=False, future=True)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False, autoflush=False)

session_module.engine = test_engine  # type: ignore
session_module.AsyncSessionLocal = TestSessionLocal  # type: ignore

from app.main import app  # noqa: E402
from app.db.session import get_session as original_get_session  # noqa: E402

async def override_get_session():
    async with TestSessionLocal() as session:  # type: ignore
        yield session

app.dependency_overrides[original_get_session] = override_get_session

@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_test_db():
    async with test_engine.begin() as conn:  # type: ignore
        await conn.run_sync(base.Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:  # type: ignore
        await conn.run_sync(base.Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client():
    from httpx import AsyncClient, ASGITransport
    from app.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
