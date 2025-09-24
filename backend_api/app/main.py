import logging
from logging.config import dictConfig
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging_config import LOGGING_CONFIG
from app.core.errors import register_exception_handlers
from app.routers import dashboards, datasources, alerts, users, health


def create_app() -> FastAPI:
    """
    Factory to create and configure the FastAPI app instance.
    """
    dictConfig(LOGGING_CONFIG)
    app = FastAPI(
        title="Grafana Integration API",
        description="FastAPI service providing secure endpoints to interact with Grafana REST API (Dashboards, Data Sources, Alerts, Users).",
        version="1.0.0",
        contact={"name": "API Support", "email": "support@example.com"},
        license_info={"name": "MIT"},
        openapi_tags=[
            {"name": "Health", "description": "Service health and metadata"},
            {"name": "Dashboards", "description": "Operations on Grafana dashboards"},
            {"name": "Data Sources", "description": "Operations on Grafana data sources"},
            {"name": "Alerts", "description": "Operations on Grafana alerts"},
            {"name": "Users", "description": "Operations on Grafana users"},
        ],
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(health.router, prefix="/api")
    app.include_router(dashboards.router, prefix="/api")
    app.include_router(datasources.router, prefix="/api")
    app.include_router(alerts.router, prefix="/api")
    app.include_router(users.router, prefix="/api")

    # Exceptions
    register_exception_handlers(app)

    logging.getLogger(__name__).info("Application initialized")
    return app


app = create_app()
