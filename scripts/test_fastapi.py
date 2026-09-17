import sys
import os

# Add project root to path so backend.* imports resolve
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") in ("ok", "healthy")
    assert "service" in data
    print("Health check passed.")

def test_api_docs() -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    docs = response.json()
    assert "Insider Threat" in docs["info"]["title"]
    print("OpenAPI schema generated successfully.")
    
    # Check if all our expected routes exist
    paths = docs["paths"].keys()
    assert "/api/v1/auth/login" in paths
    assert "/api/v1/users/" in paths
    assert "/api/v1/predictions/predict" in paths
    assert "/api/v1/graphs/query" in paths
    assert "/api/v1/explain/{prediction_id}" in paths
    assert "/api/v1/alerts/" in paths
    assert "/api/v1/reports/generate" in paths
    print("All domain routes are correctly registered!")

if __name__ == "__main__":
    print("Running FastAPI Backend tests...")
    test_health_check()
    test_api_docs()
    print("All tests passed successfully!")
