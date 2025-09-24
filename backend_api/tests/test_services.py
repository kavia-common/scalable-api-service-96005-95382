from unittest.mock import patch
from src.api.services.grafana_client import GrafanaClient

class MockResponse:
    def __init__(self, status_code=200, json_data=None, text=""):
        self.status_code = status_code
        self._json = json_data
        self.text = text

    def json(self):
        return self._json

@patch("httpx.Client")
def test_search_dashboards_ok(MockClient):
    client_instance = MockClient.return_value
    client_instance.get.return_value = MockResponse(200, [{"uid": "1"}])
    g = GrafanaClient()
    res = g.search_dashboards("q")
    assert res == [{"uid": "1"}]

@patch("httpx.Client")
def test_get_dashboard_not_found(MockClient):
    client_instance = MockClient.return_value
    client_instance.get.return_value = MockResponse(404, {"message": "not found"})
    g = GrafanaClient()
    try:
        g.get_dashboard("missing")
        assert False, "Should have raised"
    except GrafanaClient.NotFoundError:
        assert True
