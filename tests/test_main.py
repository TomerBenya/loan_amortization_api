from fastapi.testclient import TestClient
from loan_amortization_api.main import app
import pytest

client = TestClient(app)

def test_create_user():
    # Ensure the user does not already exist
    response = client.post("/users/", json={"username": "testuser", "email": "test@example.com"})
    assert response.status_code in [200, 400]  # 400 if user already exists
    if response.status_code == 200:
        assert response.json() == {"username": "testuser", "email": "test@example.com"}

def test_create_loan():
    response = client.post("/loans/", json={"amount": 1000, "annual_interest_rate": 5.0, "loan_term": 12})
    assert response.status_code == 200
    assert response.json() == {"amount": 1000, "annual_interest_rate": 5.0, "loan_term": 12}

def test_get_loan_schedule():
    response = client.get("/loans/schedule/1")
    assert response.status_code == 200
    assert len(response.json()) == 12

def test_get_loan_summary():
    response = client.get("/loans/summary/1/6")
    assert response.status_code == 200
    assert "current_principal_balance" in response.json()
    assert "principal_paid" in response.json()
    assert "interest_paid" in response.json()
