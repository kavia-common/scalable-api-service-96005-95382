import hmac
import logging

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..utils.config import settings

logger = logging.getLogger(__name__)
bearer_scheme = HTTPBearer(auto_error=True)


def _secure_compare(a: str, b: str) -> bool:
    # Constant-time comparison
    return hmac.compare_digest(a.encode(), b.encode())


# PUBLIC_INTERFACE
def verify_bearer_token(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)) -> HTTPAuthorizationCredentials:
    """
    Validates incoming Bearer token against TOKEN_SECRET.
    Returns the credentials if valid; raises 401 otherwise.
    """
    if not settings.TOKEN_SECRET:
        logger.error("TOKEN_SECRET not configured")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server auth not configured")

    token = credentials.credentials
    if not token or not _secure_compare(token, settings.TOKEN_SECRET):
        logger.warning("Invalid bearer token provided")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")

    return credentials
