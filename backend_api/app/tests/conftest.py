import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="session", autouse=True)
def test_env():
    os.environ["API_BEARER_TOKEN"] = "test-token"
    os.environ["GRAFANA_URL"] = "http://grafana.test"
    os.environ["GRAFANA_API_KEY"] = "grafana-test-key"
    yield

@pytest.fixture()
def client():
    return TestClient(app)

def auth_headers():
    return {"Authorization": "Bearer test-token"}
