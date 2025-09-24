from typing import Any, Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    grafana_url: str = Field(..., description="Configured Grafana URL")


class DashboardCreate(BaseModel):
    title: str = Field(..., description="Dashboard title", examples=["My Dashboard"])
    uid: Optional[str] = Field(None, description="Unique dashboard UID")
    tags: list[str] = Field(default_factory=list, description="List of tags")
    timezone: Optional[str] = Field(None, description="Dashboard timezone")
    payload: dict = Field(default_factory=dict, description="Additional dashboard JSON model")


class DashboardUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Dashboard title")
    tags: Optional[list[str]] = Field(None, description="List of tags")
    timezone: Optional[str] = Field(None, description="Dashboard timezone")
    payload: Optional[dict] = Field(None, description="Additional dashboard JSON model")


class DataSourceCreate(BaseModel):
    name: str = Field(..., description="Data source name")
    type: str = Field(..., description="Grafana data source type", examples=["prometheus", "elasticsearch"])
    url: Optional[str] = Field(None, description="Endpoint URL")
    access: Optional[str] = Field(default="proxy", description="Access mode")
    basicAuth: Optional[bool] = Field(default=False, description="Enable basic auth")
    jsonData: Optional[dict] = Field(default=None, description="JSON data")
    secureJsonData: Optional[dict] = Field(default=None, description="Secure JSON data")


class DataSourceUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Data source name")
    url: Optional[str] = Field(None, description="Endpoint URL")
    access: Optional[str] = Field(None, description="Access mode")
    jsonData: Optional[dict] = Field(default=None, description="JSON data")
    secureJsonData: Optional[dict] = Field(default=None, description="Secure JSON data")


class AlertCreate(BaseModel):
    title: str = Field(..., description="Alert rule title")
    condition: str = Field(..., description="Rule condition (legacy)", examples=["A>5"])
    data: list[dict] = Field(..., description="Query data for the alert rule")


class AlertUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Alert rule title")
    condition: Optional[str] = Field(None, description="Rule condition (legacy)")
    data: Optional[list[dict]] = Field(None, description="Query data for the alert rule")


class UserCreate(BaseModel):
    name: str = Field(..., description="User name")
    email: str = Field(..., description="User email")
    login: str = Field(..., description="Login/username")
    password: str = Field(..., description="Password")


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, description="User name")
    email: Optional[str] = Field(None, description="User email")
    login: Optional[str] = Field(None, description="Login/username")
    theme: Optional[str] = Field(None, description="User theme")


class GenericMessage(BaseModel):
    message: str = Field(..., description="Result message")
