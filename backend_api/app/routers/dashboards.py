from fastapi import APIRouter, Depends, Path, Query
from app.core.auth import get_bearer_token
from app.models.schemas import DashboardCreate, DashboardUpdate
from app.services.grafana_client import GrafanaClient

router = APIRouter(prefix="/dashboards", tags=["Dashboards"])


def _client() -> GrafanaClient:
    return GrafanaClient()


@router.get("", summary="List dashboards")
async def list_dashboards(_: str = Depends(get_bearer_token), query: str | None = Query(None, description="Search query")):
    """
    Returns a list of dashboards matching the search query.
    """
    client = _client()
    params = {"query": query} if query else None
    return await client.get("/api/search", params=params)


@router.get("/{uid}", summary="Get dashboard by UID")
async def get_dashboard(uid: str = Path(..., description="Dashboard UID"), _: str = Depends(get_bearer_token)):
    """
    Get a dashboard by UID. Wraps Grafana GET /api/dashboards/uid/{uid}.
    """
    client = _client()
    return await client.get(f"/api/dashboards/uid/{uid}")


@router.post("", summary="Create dashboard")
async def create_dashboard(payload: DashboardCreate, _: str = Depends(get_bearer_token)):
    """
    Create dashboard using Grafana POST /api/dashboards/db.
    """
    client = _client()
    grafana_payload = {
        "dashboard": {
            "title": payload.title,
            "tags": payload.tags,
            "timezone": payload.timezone,
            **(payload.payload or {}),
        },
        "folderId": 0,
        "overwrite": False,
    }
    if payload.uid:
        grafana_payload["dashboard"]["uid"] = payload.uid
    return await client.post("/api/dashboards/db", grafana_payload)


@router.put("/{uid}", summary="Update dashboard")
async def update_dashboard(uid: str, payload: DashboardUpdate, _: str = Depends(get_bearer_token)):
    """
    Update dashboard by UID using Grafana POST /api/dashboards/db with overwrite.
    """
    client = _client()
    current = await client.get(f"/api/dashboards/uid/{uid}")
    db = current.get("dashboard", {})
    if payload.title is not None:
        db["title"] = payload.title
    if payload.tags is not None:
        db["tags"] = payload.tags
    if payload.timezone is not None:
        db["timezone"] = payload.timezone
    if payload.payload:
        db.update(payload.payload)
    out = {"dashboard": db, "folderId": current.get("meta", {}).get("folderId", 0), "overwrite": True}
    return await client.post("/api/dashboards/db", out)


@router.delete("/{uid}", summary="Delete dashboard")
async def delete_dashboard(uid: str, _: str = Depends(get_bearer_token)):
    """
    Delete dashboard by UID using Grafana DELETE /api/dashboards/uid/{uid}.
    """
    client = _client()
    return await client.delete(f"/api/dashboards/uid/{uid}")
