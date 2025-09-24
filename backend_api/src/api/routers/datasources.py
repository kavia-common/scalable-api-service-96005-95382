import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Path, status
from pydantic import BaseModel, Field

from ..services.grafana_client import GrafanaClient

logger = logging.getLogger(__name__)
router = APIRouter()


class DataSourcePayload(BaseModel):
    name: str = Field(..., description="Data source name", examples=["Prometheus"])
    type: str = Field(..., description="Grafana data source type", examples=["prometheus"])
    url: str = Field(..., description="Endpoint URL", examples=["http://prometheus:9090"])
    access: str = Field("proxy", description="Access method", examples=["proxy", "direct"])
    isDefault: bool = Field(False, description="Set as default data source")
    jsonData: Optional[Dict[str, Any]] = Field(None, description="JSON data config")
    secureJsonData: Optional[Dict[str, Any]] = Field(None, description="Sensitive config")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Prometheus",
                "type": "prometheus",
                "url": "http://prometheus:9090",
                "access": "proxy",
                "isDefault": True,
                "jsonData": {},
                "secureJsonData": {},
            }
        }


# PUBLIC_INTERFACE
@router.get("", summary="List Data Sources", response_model=List[Dict[str, Any]])
def list_data_sources():
    client = GrafanaClient()
    try:
        return client.list_datasources()
    except Exception as e:
        logger.exception("Failed to list data sources")
        raise HTTPException(status_code=500, detail=str(e))


# PUBLIC_INTERFACE
@router.get("/{id}", summary="Get Data Source by ID", response_model=Dict[str, Any])
def get_data_source(id: int = Path(..., description="Data source ID")):
    client = GrafanaClient()
    try:
        return client.get_datasource(id)
    except GrafanaClient.NotFoundError:
        raise HTTPException(status_code=404, detail="Data source not found")
    except Exception as e:
        logger.exception("Failed to get data source")
        raise HTTPException(status_code=500, detail=str(e))


# PUBLIC_INTERFACE
@router.post("", summary="Create Data Source", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any])
def create_data_source(payload: DataSourcePayload):
    client = GrafanaClient()
    try:
        return client.create_datasource(payload.model_dump())
    except Exception as e:
        logger.exception("Failed to create data source")
        raise HTTPException(status_code=500, detail=str(e))


# PUBLIC_INTERFACE
@router.put("/{id}", summary="Update Data Source", response_model=Dict[str, Any])
def update_data_source(payload: DataSourcePayload, id: int = Path(..., description="Data source ID")):
    client = GrafanaClient()
    try:
        return client.update_datasource(id, payload.model_dump())
    except GrafanaClient.NotFoundError:
        raise HTTPException(status_code=404, detail="Data source not found")
    except Exception as e:
        logger.exception("Failed to update data source")
        raise HTTPException(status_code=500, detail=str(e))


# PUBLIC_INTERFACE
@router.delete("/{id}", summary="Delete Data Source", status_code=status.HTTP_204_NO_CONTENT)
def delete_data_source(id: int = Path(..., description="Data source ID")):
    client = GrafanaClient()
    try:
        client.delete_datasource(id)
        return
    except GrafanaClient.NotFoundError:
        raise HTTPException(status_code=404, detail="Data source not found")
    except Exception as e:
        logger.exception("Failed to delete data source")
        raise HTTPException(status_code=500, detail=str(e))
