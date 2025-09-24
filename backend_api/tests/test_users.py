from unittest.mock import patch

def test_list_users(client, auth_headers):
    with patch("src.api.routers.users.GrafanaClient") as MockClient:
        instance = MockClient.return_value
        instance.list_users.return_value = [{"id": 10}]
        res = client.get("/users", headers=auth_headers)
        assert res.status_code == 200
        assert res.json() == [{"id": 10}]
