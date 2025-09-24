from app.tests.conftest import auth_headers

def test_health(client):
    r = client.get("/api/health", headers=auth_headers())
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "version" in data
