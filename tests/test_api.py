from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Active", "message": "API is up and running."}

def test_missing_payload():
    response = client.post("/predict", json={})
    assert response.status_code == 422 # FastAPI automatic validation error