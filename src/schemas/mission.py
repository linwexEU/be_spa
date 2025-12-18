from typing import Optional

from pydantic import BaseModel

from src.schemas.base import Response
from src.models.models import Mission
from src.models.enums import State
from src.schemas.target import CreateTargetRequest, UpdateTargetRequest
from src.schemas.spy_cat import Info as SpyCatInfo
from src.schemas.target import Info as TargetInfo


class CreateMissionRequest(BaseModel): 
    spy_cat: Optional[int] = None 
    target: CreateTargetRequest


class SMission(BaseModel): 
    spy_cat: Optional[int] = None
    target: int


class CreateMissionResponse(Response): 
    pass 


class DeleteMissionResponse(Response): 
    pass 


class AssignMissionResponse(Response): 
    pass 


class UpdateMissionRequest(BaseModel):
    target: Optional[UpdateTargetRequest] = None


class UpdateMissionResponse(Response): 
    pass


class Info(BaseModel): 
    id: int
    spy_cat: Optional[SpyCatInfo]
    target: TargetInfo
    state: State

    @staticmethod
    def from_orm(mission: Mission) -> "Info": 
        return Info(
            id=mission.id,
            spy_cat=SpyCatInfo.from_orm(mission.fr_spy_cat) if mission.fr_spy_cat else None,
            target=TargetInfo.from_orm(mission.fr_target), 
            state=mission.state
        )
    

class ListInfo(BaseModel): 
    data: list[Info]

    @staticmethod
    def from_orm(missions: list[Mission]) -> "ListInfo": 
        return ListInfo(data=[Info.from_orm(mission) for mission in missions])
