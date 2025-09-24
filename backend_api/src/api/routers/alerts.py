import logging
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Path, status
from pydantic import BaseModel, Field

from ..services.grafana_client import GrafanaClient

logger = logging.getLogger(__name__)
router = APIRouter()


class AlertRulePayload(BaseModel):
    title: str = Field(..., description="Alert rule name")
    condition: str = Field(..., description="Condition reference")
    data: List[Dict[str, Any]] = Field(..., description="Query data for the rule")
    annotations: Dict[str, str] = Field(default_factory=dict, description="Annotations")
    labels: Dict[str, str] = Field(default_factory=dict, description="Labels")
    orgId: int = Field(1, description="Org ID")


# PUBLIC_INTERFACE
@router.get("", summary="List Alert Rules", response_model=List[Dict[str, Any]])
def list_alerts():
    client = GrafanaClient()
    try:
        return client.list_alert_rules()
    except Exception as e:
        logger.exception("Failed to list alerts")
        raise HTTPException(status_code=500, detail=str(e))


# PUBLIC_INTERFACE
@router.get("/{uid}", summary="Get Alert Rule by UID", response_model=Dict[str, Any])
def get_alert(uid: str = Path(..., description="Alert rule UID")):
    client = GrafanaClient()
    try:
        return client.get_alert_rule(uid)
    except GrafanaClient.NotFoundError:
        raise HTTPException(status_code=404, detail="Alert rule not found")
    except Exception as e:
        logger.exception("Failed to get alert")
        raise HTTPException(status_code=500, detail=str(e))


# PUBLIC_INTERFACE
@router.post("", summary="Create Alert Rule", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any])
def create_alert(payload: AlertRulePayload):
    client = GrafanaClient()
    try:
        return client.create_alert_rule(payload.model_dump())
    except Exception as e:
        logger.exception("Failed to create alert rule")
        raise HTTPException(status_code=500, detail=str(e))


# PUBLIC_INTERFACE
@router.put("/{uid}", summary="Update Alert Rule", response_model=Dict[str, Any])
def update_alert(payload: AlertRulePayload, uid: str = Path(..., description="Alert rule UID")):
    client = GrafanaClient()
    try:
        return client.update_alert_rule(uid, payload.model_dump())
    except GrafanaClient.NotFoundError:
        raise HTTPException(status_code=404, detail="Alert rule not found")
    except Exception as e:
        logger.exception("Failed to update alert rule")
        raise HTTPException(status_code=500, detail=str(e))


# PUBLIC_INTERFACE
@router.delete("/{uid}", summary="Delete Alert Rule", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(uid: str = Path(..., description="Alert rule UID")):
    client = GrafanaClient()
    try:
        client.delete_alert_rule(uid)
        return
    except GrafanaClient.NotFoundError:
        raise HTTPException(status_code=404, detail="Alert rule not found")
    except Exception as e:
        logger.exception("Failed to delete alert rule")
        raise HTTPException(status_code=500, detail=str(e))
