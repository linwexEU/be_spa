from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.middleware.exc_middleware import ExceptionHandlerMiddleware
from src.api import router 
from src.utils.logger import configure_logging


@asynccontextmanager 
async def lifespan(app: FastAPI): 
    configure_logging()
    yield


def create_app() -> FastAPI: 
    app = FastAPI(lifespan=lifespan, title="Spy Cat Agency") 

    # Include middlewares
    app.add_middleware(ExceptionHandlerMiddleware)
    
    # Include routers
    app.include_router(router) 

    return app


app = create_app() 
