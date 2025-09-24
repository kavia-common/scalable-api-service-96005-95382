from unittest.mock import patch

def test_list_datasources(client, auth_headers):
    with patch("src.api.routers.datasources.GrafanaClient") as MockClient:
        instance = MockClient.return_value
        instance.list_datasources.return_value = [{"id": 1}]
        res = client.get("/datasources", headers=auth_headers)
        assert res.status_code == 200
        assert res.json() == [{"id": 1}]
