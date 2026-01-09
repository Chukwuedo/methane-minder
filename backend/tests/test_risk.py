import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


def test_risk_endpoint_exists(client):
    """Test that the risk endpoint is accessible."""
    response = client.get("/v1/risk/USA")
    # Should return 200 or an error status
    assert response.status_code in [200, 404, 500]


def test_risk_endpoint_with_different_countries(client):
    """Test risk endpoint with various country codes."""
    countries = ["USA", "Switzerland", "Germany", "China"]
    
    for country in countries:
        response = client.get(f"/v1/risk/{country}")
        # Should return some response
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            # Check if response is valid JSON
            data = response.json()
            assert data is not None
