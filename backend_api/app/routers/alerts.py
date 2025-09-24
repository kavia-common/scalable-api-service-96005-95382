from fastapi import APIRouter, Depends, Path
from app.core.auth import get_bearer_token
from app.models.schemas import AlertCreate, AlertUpdate
from app.services.grafana_client import GrafanaClient

router = APIRouter(prefix="/alerts", tags=["Alerts"])


def _client() -> GrafanaClient:
    return GrafanaClient()


@router.get("", summary="List alerts")
async def list_alerts(_: str = Depends(get_bearer_token)):
    """List Grafana legacy alert rules."""
    return await _client().get("/api/alerts")


@router.get("/{id}", summary="Get alert")
async def get_alert(id: int = Path(..., description="Alert rule ID"), _: str = Depends(get_bearer_token)):
    """Get alert rule by ID."""
    return await _client().get(f"/api/alerts/{id}")


@router.post("", summary="Create alert")
async def create_alert(payload: AlertCreate, _: str = Depends(get_bearer_token)):
    """Create legacy alert rule."""
    return await _client().post("/api/alerts", payload.model_dump(exclude_none=True))


@router.put("/{id}", summary="Update alert")
async def update_alert(id: int, payload: AlertUpdate, _: str = Depends(get_bearer_token)):
    """Update alert rule by ID."""
    return await _client().put(f"/api/alerts/{id}", payload.model_dump(exclude_none=True))


@router.delete("/{id}", summary="Delete alert")
async def delete_alert(id: int, _: str = Depends(get_bearer_token)):
    """Delete alert rule by ID."""
    return await _client().delete(f"/api/alerts/{id}")
