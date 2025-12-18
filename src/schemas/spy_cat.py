from typing import Optional

from pydantic import BaseModel

from src.schemas.base import Response
from src.models.models import SpyCat


class CreateSpyCatRequest(BaseModel): 
    name: str
    years_of_experience: int
    breed: str
    salary: float


class CreateSpyCatResponse(Response): 
    pass


class DeleteSpyCatResponse(Response): 
    pass 


class UpdateSpyCatRequest(BaseModel): 
    name: Optional[str] = None 
    years_of_experience: Optional[int] = None
    breed: Optional[str] = None
    salary: Optional[float] = None


class UpdateSpyCatResponse(Response): 
    pass 


class Info(BaseModel): 
    id: int
    name: str
    years_of_experience: int
    breed: str
    salary: float

    @staticmethod
    def from_orm(spy_cat: SpyCat) -> "Info": 
        return Info(
            id=spy_cat.id,
            name=spy_cat.name, 
            years_of_experience=spy_cat.years_of_experience, 
            breed=spy_cat.breed, 
            salary=spy_cat.salary
        )


class ListInfo(BaseModel): 
    data: list[Info]

    @staticmethod 
    def from_orm(spy_cats: list[SpyCat]) -> "ListInfo": 
        return ListInfo(data=[Info.from_orm(spy_cat) for spy_cat in spy_cats])
