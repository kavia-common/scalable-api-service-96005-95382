import logging
from typing import Any, Dict, List, Optional

import httpx

from ..utils.config import settings

logger = logging.getLogger(__name__)


class GrafanaClient:
    """
    Thin client for Grafana REST API using API Key auth.
    Provides helper methods used by routers. Raises NotFoundError for 404s.
    """

    class NotFoundError(Exception):
        pass

    def __init__(self) -> None:
        self.base_url = settings.GRAFANA_BASE_URL.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {settings.GRAFANA_API_KEY}",
            "Content-Type": "application/json",
        }
        self._client = httpx.Client(base_url=self.base_url, headers=self.headers, timeout=30.0)

    def __del__(self):
        try:
            self._client.close()
        except Exception:  # pragma: no cover
            pass

    # Dashboards
    def search_dashboards(self, query: Optional[str] = None) -> List[Dict[str, Any]]:
        params = {}
        if query:
            params["query"] = query
        resp = self._client.get("/api/search", params=params)
        return self._handle_response(resp)

    def get_dashboard(self, uid: str) -> Dict[str, Any]:
        resp = self._client.get(f"/api/dashboards/uid/{uid}")
        return self._handle_response(resp)

    def create_or_update_dashboard(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        resp = self._client.post("/api/dashboards/db", json=payload)
        return self._handle_response(resp)

    def delete_dashboard(self, uid: str) -> None:
        resp = self._client.delete(f"/api/dashboards/uid/{uid}")
        self._handle_response(resp)
        return None

    # Data Sources
    def list_datasources(self) -> List[Dict[str, Any]]:
        resp = self._client.get("/api/datasources")
        return self._handle_response(resp)

    def get_datasource(self, id: int) -> Dict[str, Any]:
        resp = self._client.get(f"/api/datasources/{id}")
        return self._handle_response(resp)

    def create_datasource(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        resp = self._client.post("/api/datasources", json=payload)
        return self._handle_response(resp)

    def update_datasource(self, id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        resp = self._client.put(f"/api/datasources/{id}", json=payload)
        return self._handle_response(resp)

    def delete_datasource(self, id: int) -> None:
        resp = self._client.delete(f"/api/datasources/{id}")
        self._handle_response(resp)
        return None

    # Alerts (Unified alerting)
    def list_alert_rules(self) -> List[Dict[str, Any]]:
        resp = self._client.get("/api/ruler/grafana/api/v1/rules")
        return self._handle_response(resp)

    def get_alert_rule(self, uid: str) -> Dict[str, Any]:
        resp = self._client.get(f"/api/ruler/grafana/api/v1/rules/{uid}")
        return self._handle_response(resp)

    def create_alert_rule(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        resp = self._client.post("/api/ruler/grafana/api/v1/rules", json=payload)
        return self._handle_response(resp)

    def update_alert_rule(self, uid: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        resp = self._client.put(f"/api/ruler/grafana/api/v1/rules/{uid}", json=payload)
        return self._handle_response(resp)

    def delete_alert_rule(self, uid: str) -> None:
        resp = self._client.delete(f"/api/ruler/grafana/api/v1/rules/{uid}")
        self._handle_response(resp)
        return None

    # Users
    def list_users(self) -> List[Dict[str, Any]]:
        resp = self._client.get("/api/users")
        return self._handle_response(resp)

    def get_user(self, user_id: int) -> Dict[str, Any]:
        resp = self._client.get(f"/api/users/{user_id}")
        return self._handle_response(resp)

    def create_user(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        resp = self._client.post("/api/admin/users", json=payload)
        return self._handle_response(resp)

    def update_user(self, user_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        resp = self._client.put(f"/api/users/{user_id}", json=payload)
        return self._handle_response(resp)

    def delete_user(self, user_id: int) -> None:
        resp = self._client.delete(f"/api/admin/users/{user_id}")
        self._handle_response(resp)
        return None

    def _handle_response(self, resp: httpx.Response):
        if resp.status_code == 404:
            raise GrafanaClient.NotFoundError("Not Found")
        if 200 <= resp.status_code < 300:
            try:
                return resp.json()
            except Exception:
                return {}
        logger.error("Grafana API error %s: %s", resp.status_code, resp.text)
        try:
            data = resp.json()
        except Exception:
            data = {"message": resp.text}
        raise Exception(data.get("message") or data)
