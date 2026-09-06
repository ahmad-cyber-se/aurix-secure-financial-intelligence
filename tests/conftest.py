import os
from pathlib import Path

TEST_DB = Path(__file__).parent / "aurix_test.db"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"
os.environ["JWT_SECRET"] = "test-secret-key-that-is-long-enough-for-tests-only"
os.environ["CORS_ORIGINS"] = "http://localhost:3000"

import pytest
from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.main import app
from app.seed import seed_reference_data


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_reference_data(db)
    yield


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def register_user(client, *, email="shahan@example.com", country="Germany", plan="FREE", name="Shahan"):
    response = client.post(
        "/auth/register",
        json={
            "name": name,
            "email": email,
            "password": "StrongPass123!",
            "country": country,
            "subscription_plan": plan,
        },
    )
    assert response.status_code == 201, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
