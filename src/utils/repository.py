from abc import abstractmethod, ABC
from typing import TypeVar, Generic

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import Base

DbModel = TypeVar("DM", bound=Base)


class AbstractRepository(ABC, Generic[DbModel]): 
    _model: type[Base] 

    @abstractmethod
    def __init__(self, session: AsyncSession) -> None: 
        ...

    @abstractmethod
    async def create(self, payload: dict) -> int: 
        ...

    @abstractmethod
    async def update(self, entity_id: int, payload: dict) -> int: 
        ...

    @abstractmethod
    async def delete(self, entity_id: int) -> int: 
        ... 

    @abstractmethod
    async def select(self) -> list[DbModel]: 
        ... 

    @abstractmethod
    async def select_one(self, entity_id: int) -> DbModel: 
        ...
    