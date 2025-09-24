from app.tests.conftest import auth_headers

def test_list_datasources(monkeypatch, client):
    async def fake_get(self, path, params=None):
        assert path == "/api/datasources"
        return [{"name":"ds"}]
    from app.services import grafana_client as gc
    monkeypatch.setattr(gc.GrafanaClient, "get", fake_get)
    r = client.get("/api/datasources", headers=auth_headers())
    assert r.status_code == 200

def test_get_datasource_by_name(monkeypatch, client):
    async def fake_get(self, path, params=None):
        assert path == "/api/datasources/name/prom"
        return {"name":"prom"}
    from app.services import grafana_client as gc
    monkeypatch.setattr(gc.GrafanaClient, "get", fake_get)
    r = client.get("/api/datasources/prom", headers=auth_headers())
    assert r.status_code == 200
