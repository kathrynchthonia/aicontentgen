from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.user import authentication_token_from_email


def test_access_protected_route_unauthenticated(client: TestClient) -> None:
    """
    Should reject access to protected endpoint when no token is provided.
    """
    response = client.get(f"{settings.API_V1_STR}/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_access_protected_route_authenticated(
    client: TestClient, db: Session
) -> None:
    """
    Should allow access to protected endpoint with valid token.
    """
    headers = authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )
    response = client.get(f"{settings.API_V1_STR}/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert data["email"] == settings.EMAIL_TEST_USER


def test_access_protected_route_invalid_token(client: TestClient) -> None:
    """
    Should reject access when token is invalid or expired.
    """
    fake_headers = {"Authorization": "Bearer invalidtoken"}
    response = client.get(f"{settings.API_V1_STR}/users/me", headers=fake_headers)
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}
