# tests/test_auth.py

from app.schemas import UserCreate
from app.utils import verify_password

def test_register_user(client, db_session):
    response = client.post(
        "/register",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"

def test_login_user(client, db_session):
    # First, register a user
    client.post(
        "/register",
        json={"email": "test@example.com", "password": "password123"}
    )
    # Then, attempt to log in
    response = client.post(
        "/login",
        data={"username": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
