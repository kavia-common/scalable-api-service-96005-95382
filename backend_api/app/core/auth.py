from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

security = HTTPBearer(auto_error=True)

# PUBLIC_INTERFACE
def get_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Validate Bearer token from the Authorization header against configured API_BEARER_TOKEN.
    Raises 401 if token is missing or invalid.
    """
    token: Optional[str] = credentials.credentials if credentials else None
    if not settings.is_auth_enabled:
        # If no token configured, deny by default for safety
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API authentication is not configured",
        )
    if not token or token != settings.API_BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing bearer token",
        )
    return token
