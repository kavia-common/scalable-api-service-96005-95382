import types
from app.tests.conftest import auth_headers

def test_list_dashboards(monkeypatch, client):
    async def fake_get(self, path, params=None):
        assert path == "/api/search"
        return [{"uid":"abc","title":"T"}]
    from app.services import grafana_client as gc
    monkeypatch.setattr(gc.GrafanaClient, "get", fake_get)
    r = client.get("/api/dashboards", headers=auth_headers())
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_get_dashboard(monkeypatch, client):
    async def fake_get(self, path, params=None):
        assert path == "/api/dashboards/uid/abc"
        return {"dashboard":{"uid":"abc"}}
    from app.services import grafana_client as gc
    monkeypatch.setattr(gc.GrafanaClient, "get", fake_get)
    r = client.get("/api/dashboards/abc", headers=auth_headers())
    assert r.status_code == 200
    assert r.json()["dashboard"]["uid"] == "abc"
