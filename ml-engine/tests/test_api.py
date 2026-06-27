# pyrefly: ignore [missing-import]
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint_returns_200():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"

def test_predict_endpoint_validates_input():
    # Missing required fields
    response = client.post("/predict", json={"age": 40})
    assert response.status_code == 422

def test_predict_endpoint_returns_valid_response():
    valid_payload = {
        "age": 45,
        "gender": "male",
        "bmi": 27.5,
        "smoking_status": "former",
        "alcohol_consumption": "moderate",
        "physical_activity": "moderate",
        "family_history": True,
        "diabetes": False,
        "systolic_bp": 135,
        "diastolic_bp": 85,
        "cholesterol_level": "borderline"
    }
    
    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 200
    data = response.json()
    
    assert "risk_level" in data
    assert "confidence_score" in data
    assert "feature_importance" in data
