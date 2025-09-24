import logging

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

from .routers import dashboards, datasources, alerts, users
from .auth.dependencies import verify_bearer_token
from .utils.config import settings
from .utils.errors import register_exception_handlers
from .utils.logging_config import configure_logging

# Configure logging early
configure_logging()
logger = logging.getLogger(__name__)

openapi_tags = [
    {"name": "Health", "description": "Service health and metadata"},
    {"name": "Dashboards", "description": "CRUD operations for Grafana Dashboards"},
    {"name": "DataSources", "description": "CRUD operations for Grafana Data Sources"},
    {"name": "Alerts", "description": "CRUD operations for Grafana Alerts"},
    {"name": "Users", "description": "CRUD operations for Grafana Users"},
]

app = FastAPI(
    title="Grafana Proxy API",
    description=(
        "A secure, modular FastAPI backend that proxies CRUD operations to Grafana's REST API.\n\n"
        "Authentication: All endpoints require a Bearer token (configured via TOKEN_SECRET). "
        "Outbound requests to Grafana use the Grafana API Key from environment.\n\n"
        "Environment configuration: See .env.example for required variables."
    ),
    version="1.0.0",
    openapi_tags=openapi_tags,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Customize for your deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers (unified error responses)
register_exception_handlers(app)

# Root/health endpoint
class HealthResponse(BaseModel):
    status: str = Field(..., description="Service status string", examples=["ok"])
    grafana_base_url: str = Field(..., description="Configured Grafana base URL")
    docs_url: str = Field(..., description="Docs URL")

# PUBLIC_INTERFACE
@app.get("/", summary="Health Check", tags=["Health"], response_model=HealthResponse)
def health_check(_: HTTPAuthorizationCredentials = Depends(verify_bearer_token)):
    """Health check endpoint requiring Bearer auth to verify auth layer is active."""
    return HealthResponse(
        status="ok",
        grafana_base_url=settings.GRAFANA_BASE_URL,
        docs_url="/docs",
    )

# Include routers with global dependency for Bearer auth
app.include_router(
    dashboards.router,
    prefix="/dashboards",
    tags=["Dashboards"],
    dependencies=[Depends(verify_bearer_token)],
)
app.include_router(
    datasources.router,
    prefix="/datasources",
    tags=["DataSources"],
    dependencies=[Depends(verify_bearer_token)],
)
app.include_router(
    alerts.router,
    prefix="/alerts",
    tags=["Alerts"],
    dependencies=[Depends(verify_bearer_token)],
)
app.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(verify_bearer_token)],
)
