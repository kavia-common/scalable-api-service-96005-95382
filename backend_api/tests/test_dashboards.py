from unittest.mock import patch

def test_list_dashboards(client, auth_headers):
    with patch("src.api.routers.dashboards.GrafanaClient") as MockClient:
        instance = MockClient.return_value
        instance.search_dashboards.return_value = [{"uid": "a"}]
        res = client.get("/dashboards", headers=auth_headers)
        assert res.status_code == 200
        assert res.json() == [{"uid": "a"}]

def test_get_dashboard_not_found(client, auth_headers):
    with patch("src.api.routers.dashboards.GrafanaClient") as MockClient:
        instance = MockClient.return_value
        instance.get_dashboard.side_effect = MockClient.NotFoundError()
        res = client.get("/dashboards/missing", headers=auth_headers)
        assert res.status_code == 404
