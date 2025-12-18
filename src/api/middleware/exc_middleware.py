from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, status
from starlette.middleware.base import BaseHTTPMiddleware

from src.exceptions.service import ServiceError


class ExceptionHandlerMiddleware(BaseHTTPMiddleware): 
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> JSONResponse:
        try:
            response = await call_next(request)
            return response
        except ServiceError as exc:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"status": "Error", "message": str(exc)}
            )   
