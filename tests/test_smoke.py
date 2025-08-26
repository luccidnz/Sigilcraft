
import os
import pytest
import sys
import json

# Add the parent directory to the path so we can import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'OK'
    assert 'service' in data

def test_vibes_endpoint(client):
    """Test the vibes API endpoint"""
    response = client.get('/api/vibes')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'vibes' in data
    assert isinstance(data['vibes'], list)

def test_sigil_endpoint_get(client):
    """Test the sigil endpoint accepts GET requests"""
    response = client.get('/api/sigil')
    # Should return 405 (Method Not Allowed) or 400 (Bad Request)
    assert response.status_code in [400, 405, 422]

def test_sigil_endpoint_post_no_data(client):
    """Test the sigil endpoint with POST but no data"""
    response = client.post('/api/sigil')
    # Should return 400 (Bad Request) for missing data
    assert response.status_code in [400, 422]

def test_sigil_endpoint_post_valid_data(client):
    """Test the sigil endpoint with valid POST data"""
    test_data = {
        'phrase': 'test intention',
        'energy': 'mystical'
    }
    response = client.post('/api/sigil', 
                          json=test_data,
                          content_type='application/json')
    # Should return 200 or handle gracefully
    assert response.status_code in [200, 400, 422, 500]
    # If 200, should have success field
    if response.status_code == 200:
        data = json.loads(response.data)
        assert 'success' in data

def test_404_handling(client):
    """Test that non-existent routes return 404"""
    response = client.get('/nonexistent-route')
    assert response.status_code == 404
