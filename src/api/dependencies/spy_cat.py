from typing import Annotated

from fastapi import Depends

from src.utils.unit_of_work import UnitOfWork
from src.api.services.spy_cat import SpyCatService


async def get_spy_cat_service() -> SpyCatService:
    return SpyCatService(UnitOfWork())


SpyCatServiceDep = Annotated[SpyCatService, Depends(get_spy_cat_service)]
