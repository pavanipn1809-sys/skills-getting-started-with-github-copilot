import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity():
    response = client.post("/activities/Chess Club/signup?email=testuser@mergington.edu")
    assert response.status_code == 200
    assert "Signed up testuser@mergington.edu for Chess Club" in response.json()["message"]

    # Duplicate signup should fail
    response = client.post("/activities/Chess Club/signup?email=testuser@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_unregister_from_activity():
    # Register first
    client.post("/activities/Programming Class/signup?email=deleteuser@mergington.edu")
    # Unregister
    response = client.delete("/activities/Programming Class/unregister?email=deleteuser@mergington.edu")
    assert response.status_code == 200
    assert "Unregistered deleteuser@mergington.edu from Programming Class" in response.json()["message"]

    # Unregister again should fail
    response = client.delete("/activities/Programming Class/unregister?email=deleteuser@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not registered"
