"""
Integration tests for Player API endpoints
"""
import pytest
from httpx import AsyncClient
from uuid import uuid4

from c_api.src.main import app


@pytest.fixture
async def client():
    """Test client for API"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_endpoint(client):
    """Test health check endpoint"""
    response = await client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test root endpoint"""
    response = await client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Arcadia Insights" in data["message"]


@pytest.mark.asyncio
async def test_create_player_success(client):
    """Test successful player creation"""
    player_data = {
        "country": "BR",
        "platform": "PC",
        "game_version": "1.0.0"
    }
    
    response = await client.post("/api/v1/players/", json=player_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["country"] == "BR"
    assert data["platform"] == "PC"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_player_invalid_data(client):
    """Test player creation with invalid data"""
    player_data = {
        "country": "BRAZIL",  # Invalid - must be 2 chars
        "platform": "PC",
        "game_version": "1.0.0"
    }
    
    response = await client.post("/api/v1/players/", json=player_data)
    
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_get_player_not_found(client):
    """Test getting non-existent player"""
    random_id = str(uuid4())
    
    response = await client.get(f"/api/v1/players/{random_id}")
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


@pytest.mark.asyncio
async def test_list_players(client):
    """Test listing players"""
    response = await client.get("/api/v1/players/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_list_players_with_pagination(client):
    """Test listing players with pagination"""
    response = await client.get("/api/v1/players/?skip=0&limit=5")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5


@pytest.mark.asyncio
async def test_list_players_invalid_limit(client):
    """Test listing players with invalid limit"""
    response = await client.get("/api/v1/players/?limit=200")  # Max is 100
    
    assert response.status_code == 422
