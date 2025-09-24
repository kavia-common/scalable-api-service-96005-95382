from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """
    Standard error response for API endpoints.
    """
    detail: str
    code: str | None = None


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers for the FastAPI app.
    """

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse(status_code=400, content=ErrorResponse(detail=str(exc), code="VALUE_ERROR").model_dump())

    @app.exception_handler(PermissionError)
    async def permission_error_handler(request: Request, exc: PermissionError):
        return JSONResponse(status_code=403, content=ErrorResponse(detail=str(exc), code="FORBIDDEN").model_dump())

    @app.exception_handler(Exception)
    async def generic_error_handler(request: Request, exc: Exception):
        # Avoid leaking internals; log server-side details
        return JSONResponse(status_code=500, content=ErrorResponse(detail="Internal server error", code="SERVER_ERROR").model_dump())
