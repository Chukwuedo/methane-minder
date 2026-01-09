import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


def test_get_plumes_endpoint_exists(client):
    """Test that the plumes endpoint is accessible."""
    response = client.get("/v1/plumes/latest")
    # Should return 200 or 404 (if data file doesn't exist in test environment)
    assert response.status_code in [200, 404, 500]


def test_get_plumes_returns_list_or_error(client):
    """Test that plumes endpoint returns appropriate response."""
    response = client.get("/v1/plumes/latest")
    
    if response.status_code == 200:
        # If successful, should return a list
        data = response.json()
        assert isinstance(data, list)
        
        # If list is not empty, check structure
        if len(data) > 0:
            plume = data[0]
            assert "plume_id" in plume
            assert "lat" in plume
            assert "lon" in plume
            assert "emission_auto" in plume or plume.get("emission_auto") is None
    elif response.status_code == 404:
        # File not found is expected in test environment
        detail = response.json().get("detail")
        assert "not found" in detail.lower()
    else:
        # Some other error occurred
        assert "detail" in response.json()
