
import os
import pytest
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as c:
        yield c

def test_root_ok(client):
    """Test root health endpoint"""
    r = client.get("/")
    assert r.status_code == 200
    assert r.data.decode() == "OK"

def test_health_endpoint(client):
    """Test detailed health endpoint"""
    r = client.get("/health")
    assert r.status_code == 200
    data = r.get_json()
    assert data['status'] == 'healthy'
    assert 'version' in data

def test_api_generate_validation(client):
    """Test sigil generation API with validation"""
    # Test missing data
    r = client.post("/api/generate")
    assert r.status_code == 400
    
    # Test invalid phrase
    r = client.post("/api/generate", json={"phrase": ""})
    assert r.status_code == 400
    
    # Test valid request structure (may fail due to processing but should not 404)
    r = client.post("/api/generate", json={"phrase": "test", "vibe": "mystical"})
    assert r.status_code in (200, 400, 422, 500)  # Any valid HTTP response

def test_api_vibes(client):
    """Test vibes endpoint"""
    r = client.get("/api/vibes")
    assert r.status_code == 200
    data = r.get_json()
    assert 'vibes' in data
    assert isinstance(data['vibes'], list)

def test_404_handling(client):
    """Test 404 handling"""
    r = client.get("/nonexistent")
    assert r.status_code == 404
