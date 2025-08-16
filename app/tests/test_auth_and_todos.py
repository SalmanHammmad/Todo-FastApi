import pytest


@pytest.mark.asyncio
async def test_register_login_and_todo_flow(client):
    r = await client.post("/auth/register", json={"email": "a@example.com", "password": "secret123"})
    assert r.status_code == 201, r.text
    r = await client.post("/auth/login", json={"email": "a@example.com", "password": "secret123"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    r = await client.post("/todos", json={"title": "Task 1", "description": "Desc"}, headers=headers)
    assert r.status_code == 201, r.text
    todo_id = r.json()["id"]
    r = await client.get("/todos", headers=headers)
    assert r.status_code == 200
    assert r.json()["total"] == 1
    r = await client.patch(f"/todos/{todo_id}", json={"completed": True}, headers=headers)
    assert r.status_code == 200
    assert r.json()["completed"] is True
    r = await client.delete(f"/todos/{todo_id}", headers=headers)
    assert r.status_code == 204
    r = await client.get("/todos", headers=headers)
    assert r.json()["total"] == 0
