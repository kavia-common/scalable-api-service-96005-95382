from fastapi import APIRouter, Depends, Path, Query
from app.core.auth import get_bearer_token
from app.models.schemas import UserCreate, UserUpdate
from app.services.grafana_client import GrafanaClient

router = APIRouter(prefix="/users", tags=["Users"])


def _client() -> GrafanaClient:
    return GrafanaClient()


@router.get("", summary="Search users")
async def search_users(query: str | None = Query(None, description="Search query"), page: int = 1, per_page: int = 25, _: str = Depends(get_bearer_token)):
    """Search Grafana users."""
    params = {"query": query, "page": page, "perpage": per_page}
    return await _client().get("/api/users/search", params=params)


@router.get("/{id}", summary="Get user by ID")
async def get_user(id: int = Path(..., description="User ID"), _: str = Depends(get_bearer_token)):
    """Get Grafana user by ID."""
    return await _client().get(f"/api/users/{id}")


@router.post("", summary="Create user")
async def create_user(payload: UserCreate, _: str = Depends(get_bearer_token)):
    """Create Grafana user."""
    return await _client().post("/api/admin/users", payload.model_dump(exclude_none=True))


@router.put("/{id}", summary="Update user")
async def update_user(id: int, payload: UserUpdate, _: str = Depends(get_bearer_token)):
    """Update Grafana user profile fields."""
    return await _client().put(f"/api/users/{id}", payload.model_dump(exclude_none=True))


@router.delete("/{id}", summary="Delete user")
async def delete_user(id: int, _: str = Depends(get_bearer_token)):
    """Delete Grafana user by ID."""
    return await _client().delete(f"/api/admin/users/{id}")
