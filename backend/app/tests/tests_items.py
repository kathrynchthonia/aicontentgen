import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.user import authentication_token_from_email


def create_item(client: TestClient, token: str, title: str, description: str):
    response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": title, "description": description},
    )
    assert response.status_code == 200
    return response.json()


def test_create_item(client: TestClient, db: Session):
    token = authentication_token_from_email(client, settings.EMAIL_TEST_USER, db)
    item = create_item(client, token, "Test Title", "Test Description")
    assert item["title"] == "Test Title"
    assert item["description"] == "Test Description"


def test_get_items(client: TestClient, db: Session):
    token = authentication_token_from_email(client, settings.EMAIL_TEST_USER, db)
    response = client.get(
        f"{settings.API_V1_STR}/items/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_item_success(client: TestClient, db: Session):
    token = authentication_token_from_email(client, settings.EMAIL_TEST_USER, db)
    item = create_item(client, token, "Old Title", "Old Description")
    item_id = item["id"]

    response = client.put(
        f"{settings.API_V1_STR}/items/{item_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "New Title", "description": "New Description"},
    )
    assert response.status_code == 200
    updated = response.json()
    assert updated["title"] == "New Title"
    assert updated["description"] == "New Description"


def test_update_item_unauthenticated(client: TestClient):
    response = client.put(
        f"{settings.API_V1_STR}/items/1",
        json={"title": "Unauthorized", "description": "No token"},
    )
    assert response.status_code == 401


def test_update_nonexistent_item(client: TestClient, db: Session):
    token = authentication_token_from_email(client, settings.EMAIL_TEST_USER, db)
    response = client.put(
        f"{settings.API_V1_STR}/items/999999",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Ghost Item", "description": "Should fail"},
    )
    assert response.status_code == 404


@pytest.mark.parametrize("invalid_data", [
    {},  # empty payload
    {"title": ""},  # missing description
    {"description": ""},  # missing title
])
def test_update_item_invalid_payload(client: TestClient, db: Session, invalid_data):
    token = authentication_token_from_email(client, settings.EMAIL_TEST_USER, db)
    item = create_item(client, token, "Valid Title", "Valid Description")

    response = client.put(
        f"{settings.API_V1_STR}/items/{item['id']}",
        headers={"Authorization": f"Bearer {token}"},
        json=invalid_data,
    )
    assert response.status_code == 422


def test_delete_item(client: TestClient, db: Session):
    token = authentication_token_from_email(client, settings.EMAIL_TEST_USER, db)
    item = create_item(client, token, "To Delete", "Temporary")

    response = client.delete(
        f"{settings.API_V1_STR}/items/{item['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    # Try getting the deleted item
    get_response = client.get(
        f"{settings.API_V1_STR}/items/{item['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_response.status_code in (404, 422)
