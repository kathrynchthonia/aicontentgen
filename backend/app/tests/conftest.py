from collections.abc import Generator
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.core.config import settings
from app.core.db import engine, init_db
from app.main import app
from app.models import Item, User
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    """
    Fixture to provide a session and initialize the test database once per test session.
    Cleans up all Items and Users after all tests complete.
    """
    with Session(engine) as session:
        init_db(session)
        yield session
        session.execute(delete(Item))
        session.execute(delete(User))
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """
    Fixture to provide a FastAPI TestClient instance.
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    """
    Fixture to provide authentication headers for the superuser.
    """
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    """
    Fixture to provide authentication headers for a regular user using a test email.
    """
    return authentication_token_from_email(
        client=client,
        email=settings.EMAIL_TEST_USER,
        db=db
    )
