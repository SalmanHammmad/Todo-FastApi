import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_and_login(monkeypatch):
    # Using in-memory DB would be better; here we just hit the running app assuming DB is available.
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/auth/register", json={"email": "user@example.com", "password": "secret123"})
        assert r.status_code in (201, 409)  # allow reruns
        r2 = await ac.post("/auth/login", json={"email": "user@example.com", "password": "secret123"})
        assert r2.status_code == 200
        token = r2.json()["access_token"]
        assert token
