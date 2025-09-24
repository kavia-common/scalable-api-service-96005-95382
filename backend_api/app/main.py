from typing import Dict, Any
import os

from fastapi import FastAPI
from pydantic import BaseModel, Field

# App-level OpenAPI metadata and tags
app = FastAPI(
    title="Scalable API Service - Backend API",
    description=(
        "FastAPI backend providing RESTful endpoints. "
        "This service is designed to be scalable and easily extendable."
    ),
    version="1.0.0",
    openapi_tags=[
        {"name": "health", "description": "Service health and readiness checks."},
        {"name": "docs", "description": "Documentation and usage help endpoints."},
    ],
)

# Models
class HealthStatus(BaseModel):
    """Represents basic health information of the service."""
    status: str = Field(..., description="Overall service status, e.g. 'ok'.")
    name: str = Field(..., description="Service name.")
    version: str = Field(..., description="Service version.")
    environment: str = Field(..., description="Deployment environment (from ENV or 'unknown').")

# PUBLIC_INTERFACE
@app.get("/health", response_model=HealthStatus, tags=["health"], summary="Health check", description="Returns basic service health and metadata.")
def health() -> HealthStatus:
    """Health endpoint to verify the service is running and responsive.

    Returns:
        HealthStatus: Current health information including service name, version, and environment.
    """
    env = os.getenv("ENVIRONMENT") or os.getenv("ENV") or "unknown"
    return HealthStatus(
        status="ok",
        name="backend_api",
        version="1.0.0",
        environment=env,
    )

# PUBLIC_INTERFACE
@app.get(
    "/websocket-usage",
    tags=["docs"],
    summary="WebSocket usage help",
    description=(
        "This project currently does not expose WebSocket endpoints. "
        "If you add one, document the connection URL, supported events, and authentication here. "
        "Example: ws://<host>/ws and messages are JSON objects with 'type' and 'payload' fields."
    ),
)
def websocket_usage_help() -> Dict[str, Any]:
    """Provides guidance about WebSocket usage for this API.

    Returns:
        Dict[str, Any]: Basic instructions and a placeholder explaining expected WebSocket usage.
    """
    return {
        "websocket": {
            "available": False,
            "note": "No WebSocket endpoints are currently implemented.",
            "how_to_add": "Create a websocket route using FastAPI's WebSocket, add operation_id, tags, and docstrings.",
        }
    }


# PUBLIC_INTERFACE
def get_app() -> FastAPI:
    """Expose the FastAPI app instance.

    Returns:
        FastAPI: The FastAPI application instance for ASGI servers.
    """
    return app
