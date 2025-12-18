__all__ = (
    "router",
)

from fastapi import APIRouter 

from src.api.routers.spy_cat import router as spy_cat_router
from src.api.routers.mission import router as mission_router

router = APIRouter()

router.include_router(spy_cat_router, prefix="/spy-cats", tags=["Spy Cats"])
router.include_router(mission_router, prefix="/missions", tags=["Missions"])
