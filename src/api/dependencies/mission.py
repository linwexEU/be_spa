from typing import Annotated

from fastapi import Depends

from src.utils.unit_of_work import UnitOfWork
from src.api.services.mission import MissionService


async def get_mission_service() -> MissionService:
    return MissionService(UnitOfWork())


MissionServiceDep = Annotated[MissionService, Depends(get_mission_service)]
