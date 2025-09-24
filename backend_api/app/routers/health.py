from fastapi import APIRouter, Depends
from app.core.auth import get_bearer_token
from app.core.config import settings
from app.models.schemas import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Health check", response_model=HealthResponse)
async def health(_: str = Depends(get_bearer_token)):
    """
    Health check endpoint secured with Bearer token.
    Returns service status, API version and configured Grafana URL.
    """
    return HealthResponse(status="ok", version="1.0.0", grafana_url=str(settings.GRAFANA_URL))
