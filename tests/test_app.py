import pytest
from httpx import AsyncClient
from src.app import app

@pytest.mark.asyncio
async def test_get_activities():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert "participants" in data["Chess Club"]

@pytest.mark.asyncio
async def test_root_redirect():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/")
        assert response.status_code == 307  # Redirect
        assert response.headers["location"] == "/static/index.html"

@pytest.mark.asyncio
async def test_signup_success():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
        assert response.status_code == 200
        data = response.json()
        assert "Signed up" in data["message"]

@pytest.mark.asyncio
async def test_signup_already_signed():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        # First signup
        await client.post("/activities/Chess%20Club/signup?email=test2@mergington.edu")
        # Second
        response = await client.post("/activities/Chess%20Club/signup?email=test2@mergington.edu")
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

@pytest.mark.asyncio
async def test_signup_activity_not_found():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post("/activities/NonExistent/signup?email=test@mergington.edu")
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

@pytest.mark.asyncio
async def test_unregister_success():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        # Signup first
        await client.post("/activities/Chess%20Club/signup?email=unreg@mergington.edu")
        # Unregister
        response = await client.delete("/activities/Chess%20Club/unregister?email=unreg@mergington.edu")
        assert response.status_code == 200
        data = response.json()
        assert "Unregistered" in data["message"]

@pytest.mark.asyncio
async def test_unregister_not_signed():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.delete("/activities/Chess%20Club/unregister?email=notsigned@mergington.edu")
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"]

@pytest.mark.asyncio
async def test_unregister_activity_not_found():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.delete("/activities/NonExistent/unregister?email=test@mergington.edu")
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]