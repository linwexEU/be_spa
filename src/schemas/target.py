from typing import Optional

from pydantic import BaseModel

from src.schemas.base import Response
from src.models.models import Target
from src.models.enums import State


class CreateTargetRequest(BaseModel): 
    name: str
    country: str
    notes: Optional[str] = None


class UpdateTargetRequest(BaseModel): 
    notes: Optional[str] = None
    state: Optional[State] = None


class Info(BaseModel): 
    name: str
    country: str
    notes: Optional[str]
    state: State

    @staticmethod
    def from_orm(target: Target) -> "Info": 
        return Info(
            name=target.name,
            country=target.country, 
            notes=target.notes, 
            state=target.state
        )
