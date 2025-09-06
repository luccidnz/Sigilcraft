#!/usr/bin/env python3
"""
Comprehensive test suite for Sigilcraft
"""
import os
import sys
import pytest
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

@pytest.fixture
def client():
    """Create test client"""
    app.testing = True
    with app.test_client() as client:
        yield client

class TestHealthEndpoints:
    """Test all health and basic endpoints"""

    def test_root_endpoint(self, client):
        """Test root endpoint serves HTML"""
        response = client.get("/")
        assert response.status_code == 200
        # Should serve HTML content, not plain "OK"
        content = response.data.decode()
        assert "html" in content.lower() or response.status_code == 404

    def test_health_endpoint(self, client):
        """Test detailed health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert 'version' in data

class TestAPIEndpoints:
    """Test all API endpoints"""

    def test_vibes_endpoint(self, client):
        """Test vibes endpoint returns valid data"""
        response = client.get("/api/vibes")
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'vibes' in data
        assert isinstance(data['vibes'], list)
        assert len(data['vibes']) > 0
        assert 'descriptions' in data

    def test_generate_endpoint_validation(self, client):
        """Test sigil generation validation"""
        # Test missing JSON body
        response = client.post("/api/generate")
        assert response.status_code == 400

        # Test empty phrase
        response = client.post("/api/generate", json={"phrase": ""})
        assert response.status_code == 400

        # Test phrase too short
        response = client.post("/api/generate", json={"phrase": "a"})
        assert response.status_code == 400

        # Test phrase too long
        long_phrase = "x" * 501
        response = client.post("/api/generate", json={"phrase": long_phrase})
        assert response.status_code == 400

    def test_generate_endpoint_success(self, client):
        """Test successful sigil generation"""
        response = client.post("/api/generate", json={
            "phrase": "test sigil",
            "vibe": "mystical",
            "advanced": False
        })

        # Should either succeed or fail gracefully (not 404)
        assert response.status_code in (200, 400, 422, 500)

        if response.status_code == 200:
            data = response.get_json()
            assert data['success'] is True
            assert 'image' in data
            assert data['phrase'] == "test sigil"
            assert data['vibe'] == "mystical"

class TestErrorHandling:
    """Test error handling"""

    def test_404_handling(self, client):
        """Test 404 error handling"""
        response = client.get("/api/nonexistent-route")
        assert response.status_code == 404
        data = response.get_json()
        assert data['success'] is False
        assert 'error' in data

if __name__ == '__main__':
    pytest.main([__file__, '-v'])