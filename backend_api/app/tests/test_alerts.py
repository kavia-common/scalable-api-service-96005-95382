from app.tests.conftest import auth_headers

def test_list_alerts(monkeypatch, client):
    async def fake_get(self, path, params=None):
        assert path == "/api/alerts"
        return []
    from app.services import grafana_client as gc
    monkeypatch.setattr(gc.GrafanaClient, "get", fake_get)
    r = client.get("/api/alerts", headers=auth_headers())
    assert r.status_code == 200
