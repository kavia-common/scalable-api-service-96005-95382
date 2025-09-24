import logging
from typing import Any, Dict, Optional

import httpx
from fastapi import HTTPException

from app.core.config import settings

logger = logging.getLogger(__name__)


class GrafanaClient:
    """
    Thin HTTP client to interact with Grafana REST API using API key authentication.
    """

    def __init__(self, base_url: str | None = None, api_key: str | None = None, timeout: float = 20.0):
        self.base_url = (base_url or str(settings.GRAFANA_URL)).rstrip("/")
        self.api_key = api_key or settings.GRAFANA_API_KEY
        self.timeout = timeout
        if not self.api_key:
            logger.warning("Grafana API key is not configured; outgoing calls will fail.")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _url(self, path: str) -> str:
        if not path.startswith("/"):
            path = "/" + path
        return f"{self.base_url}{path}"

    async def _request(self, method: str, path: str, params: Optional[Dict[str, Any]] = None, json: Any = None):
        url = self._url(path)
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.request(method, url, headers=self._headers(), params=params, json=json)
            if resp.status_code >= 400:
                logger.error("Grafana API error %s on %s %s: %s", resp.status_code, method, url, resp.text)
                raise HTTPException(status_code=resp.status_code, detail=resp.text)
            if resp.text:
                return resp.json()
            return None
        except httpx.RequestError as e:
            logger.exception("Grafana request error: %s", e)
            raise HTTPException(status_code=502, detail=f"Grafana request failed: {e}") from e

    # PUBLIC_INTERFACE
    async def get(self, path: str, params: Optional[Dict[str, Any]] = None):
        """Perform GET request to Grafana API."""
        return await self._request("GET", path, params=params)

    # PUBLIC_INTERFACE
    async def post(self, path: str, payload: Any):
        """Perform POST request to Grafana API."""
        return await self._request("POST", path, json=payload)

    # PUBLIC_INTERFACE
    async def put(self, path: str, payload: Any):
        """Perform PUT request to Grafana API."""
        return await self._request("PUT", path, json=payload)

    # PUBLIC_INTERFACE
    async def delete(self, path: str, params: Optional[Dict[str, Any]] = None):
        """Perform DELETE request to Grafana API."""
        return await self._request("DELETE", path, params=params)
