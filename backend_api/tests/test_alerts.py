from unittest.mock import patch

def test_list_alerts(client, auth_headers):
    with patch("src.api.routers.alerts.GrafanaClient") as MockClient:
        instance = MockClient.return_value
        instance.list_alert_rules.return_value = [{"uid": "rule1"}]
        res = client.get("/alerts", headers=auth_headers)
        assert res.status_code == 200
        assert res.json() == [{"uid": "rule1"}]
