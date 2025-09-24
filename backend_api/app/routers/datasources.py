from fastapi import APIRouter, Depends, Path
from app.core.auth import get_bearer_token
from app.models.schemas import DataSourceCreate, DataSourceUpdate
from app.services.grafana_client import GrafanaClient

router = APIRouter(prefix="/datasources", tags=["Data Sources"])


def _client() -> GrafanaClient:
    return GrafanaClient()


@router.get("", summary="List data sources")
async def list_datasources(_: str = Depends(get_bearer_token)):
    """List all Grafana data sources."""
    return await _client().get("/api/datasources")


@router.get("/{id_or_name}", summary="Get data source by ID or Name")
async def get_datasource(id_or_name: str = Path(..., description="Data source ID (number) or name"), _: str = Depends(get_bearer_token)):
    """Get a data source by ID or Name."""
    client = _client()
    if id_or_name.isdigit():
        return await client.get(f"/api/datasources/{id_or_name}")
    return await client.get(f"/api/datasources/name/{id_or_name}")


@router.post("", summary="Create data source")
async def create_datasource(payload: DataSourceCreate, _: str = Depends(get_bearer_token)):
    """Create a data source."""
    return await _client().post("/api/datasources", payload.model_dump(exclude_none=True))


@router.put("/{id}", summary="Update data source by ID")
async def update_datasource(id: int, payload: DataSourceUpdate, _: str = Depends(get_bearer_token)):
    """Update a data source."""
    return await _client().put(f"/api/datasources/{id}", payload.model_dump(exclude_none=True))


@router.delete("/{id}", summary="Delete data source by ID")
async def delete_datasource(id: int, _: str = Depends(get_bearer_token)):
    """Delete a data source."""
    return await _client().delete(f"/api/datasources/{id}")
