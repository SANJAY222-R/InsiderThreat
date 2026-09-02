from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "insider-threat-backend"}
    print("Health check passed.")

def test_api_docs():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    docs = response.json()
    assert "Enterprise Insider Threat Detection API" in docs["info"]["title"]
    print("OpenAPI schema generated successfully.")
    
    # Check if all our expected routes exist
    paths = docs["paths"].keys()
    assert "/api/v1/auth/login" in paths
    assert "/api/v1/users/" in paths
    assert "/api/v1/predictions/predict" in paths
    assert "/api/v1/graph/neighborhood/{node_id}" in paths
    assert "/api/v1/xai/local/{user_id}" in paths
    assert "/api/v1/alerts/" in paths
    assert "/api/v1/reports/generate/{report_type}" in paths
    print("All domain routes are correctly registered!")

if __name__ == "__main__":
    print("Running FastAPI Backend tests...")
    test_health_check()
    test_api_docs()
    print("All tests passed successfully!")
