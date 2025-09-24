import os
import pytest
from fastapi.testclient import TestClient

from src.api.main import app

@pytest.fixture(scope="session", autouse=True)
def set_env():
    os.environ.setdefault("GRAFANA_BASE_URL", "http://grafana.example")
    os.environ.setdefault("GRAFANA_API_KEY", "fake-key")
    os.environ.setdefault("TOKEN_SECRET", "test-secret")

@pytest.fixture()
def client():
    return TestClient(app)

@pytest.fixture()
def auth_headers():
    return {"Authorization": "Bearer test-secret"}
