import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Path, status
from pydantic import BaseModel, EmailStr, Field

from ..services.grafana_client import GrafanaClient

logger = logging.getLogger(__name__)
router = APIRouter()


class CreateUserPayload(BaseModel):
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email")
    login: str = Field(..., description="Username/login")
    password: str = Field(..., description="Password")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jane@example.com",
                "login": "jane",
                "password": "S3cureP@ss!",
            }
        }


class UpdateUserPayload(BaseModel):
    name: Optional[str] = Field(None, description="Full name")
    email: Optional[EmailStr] = Field(None, description="Email")
    login: Optional[str] = Field(None, description="Username/login")


# PUBLIC_INTERFACE
@router.get("", summary="List Users", response_model=List[Dict[str, Any]])
def list_users():
    client = GrafanaClient()
    try:
        return client.list_users()
    except Exception as e:
        logger.exception("Failed to list users")
        raise HTTPException(status_code=500, detail=str(e))


# PUBLIC_INTERFACE
@router.get("/{user_id}", summary="Get User by ID", response_model=Dict[str, Any])
def get_user(user_id: int = Path(..., description="User ID")):
    client = GrafanaClient()
    try:
        return client.get_user(user_id)
    except GrafanaClient.NotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.exception("Failed to get user")
        raise HTTPException(status_code=500, detail=str(e))


# PUBLIC_INTERFACE
@router.post("", summary="Create User", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any])
def create_user(payload: CreateUserPayload):
    client = GrafanaClient()
    try:
        return client.create_user(payload.model_dump())
    except Exception as e:
        logger.exception("Failed to create user")
        raise HTTPException(status_code=500, detail=str(e))


# PUBLIC_INTERFACE
@router.put("/{user_id}", summary="Update User", response_model=Dict[str, Any])
def update_user(payload: UpdateUserPayload, user_id: int = Path(..., description="User ID")):
    client = GrafanaClient()
    try:
        return client.update_user(user_id, payload.model_dump(exclude_none=True))
    except GrafanaClient.NotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.exception("Failed to update user")
        raise HTTPException(status_code=500, detail=str(e))


# PUBLIC_INTERFACE
@router.delete("/{user_id}", summary="Delete User", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int = Path(..., description="User ID")):
    client = GrafanaClient()
    try:
        client.delete_user(user_id)
        return
    except GrafanaClient.NotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.exception("Failed to delete user")
        raise HTTPException(status_code=500, detail=str(e))
