import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

from ..services.grafana_client import GrafanaClient
from ..utils.examples import example_dashboard_payload

logger = logging.getLogger(__name__)
router = APIRouter()


class DashboardPayload(BaseModel):
    dashboard: Dict[str, Any] = Field(..., description="Grafana dashboard JSON model")
    folderId: Optional[int] = Field(None, description="Folder ID to place the dashboard in")
    overwrite: bool = Field(False, description="Overwrite existing dashboard with same UID or title")

    class Config:
        json_schema_extra = {"example": example_dashboard_payload()}


class DashboardResponse(BaseModel):
    id: int = Field(..., description="Dashboard numeric ID")
    uid: str = Field(..., description="Dashboard UID")
    url: str = Field(..., description="Dashboard URL")
    status: str = Field(..., description="Result", examples=["success"])  # Grafana returns status in some responses


# PUBLIC_INTERFACE
@router.get("", summary="List Dashboards", response_model=List[Dict[str, Any]])
def list_dashboards(query: Optional[str] = Query(None, description="Search query")):
    """
    List dashboards via Grafana search API.
    """
    client = GrafanaClient()
    try:
        return client.search_dashboards(query=query)
    except Exception as e:
        logger.exception("Failed to list dashboards")
        raise HTTPException(status_code=500, detail=str(e))


# PUBLIC_INTERFACE
@router.get("/{uid}", summary="Get Dashboard by UID", response_model=Dict[str, Any])
def get_dashboard(uid: str = Path(..., description="Dashboard UID")):
    """
    Retrieve a dashboard by UID from Grafana.
    """
    client = GrafanaClient()
    try:
        return client.get_dashboard(uid)
    except GrafanaClient.NotFoundError:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    except Exception as e:
        logger.exception("Failed to get dashboard")
        raise HTTPException(status_code=500, detail=str(e))


# PUBLIC_INTERFACE
@router.post("", summary="Create/Update Dashboard", status_code=status.HTTP_201_CREATED, response_model=DashboardResponse)
def create_or_update_dashboard(payload: DashboardPayload):
    """
    Create or update a dashboard via Grafana /api/dashboards/db.
    """
    client = GrafanaClient()
    try:
        result = client.create_or_update_dashboard(payload.model_dump())
        return DashboardResponse(**result)
    except Exception as e:
        logger.exception("Failed to create/update dashboard")
        raise HTTPException(status_code=500, detail=str(e))


# PUBLIC_INTERFACE
@router.delete("/{uid}", summary="Delete Dashboard", status_code=status.HTTP_204_NO_CONTENT)
def delete_dashboard(uid: str = Path(..., description="Dashboard UID")):
    """
    Delete a dashboard by UID.
    """
    client = GrafanaClient()
    try:
        client.delete_dashboard(uid)
        return
    except GrafanaClient.NotFoundError:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    except Exception as e:
        logger.exception("Failed to delete dashboard")
        raise HTTPException(status_code=500, detail=str(e))
