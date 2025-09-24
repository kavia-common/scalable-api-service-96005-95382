from app.tests.conftest import auth_headers

def test_search_users(monkeypatch, client):
    async def fake_get(self, path, params=None):
        assert path == "/api/users/search"
        return {"totalCount": 0, "users": []}
    from app.services import grafana_client as gc
    monkeypatch.setattr(gc.GrafanaClient, "get", fake_get)
    r = client.get("/api/users?query=abc", headers=auth_headers())
    assert r.status_code == 200

def test_get_user(monkeypatch, client):
    async def fake_get(self, path, params=None):
        assert path == "/api/users/42"
        return {"id":42}
    from app.services import grafana_client as gc
    monkeypatch.setattr(gc.GrafanaClient, "get", fake_get)
    r = client.get("/api/users/42", headers=auth_headers())
    assert r.status_code == 200
