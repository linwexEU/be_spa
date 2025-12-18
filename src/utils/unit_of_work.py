from abc import ABC, abstractmethod
from typing import Any

from src.utils.repository import AbstractRepository
from src.db.base import async_session_factory
from src.repositories import MissionRepository, SpyCatRepository, TargetRepository


class AbstractUnitOfWork(ABC): 
    spy_cat_repo: AbstractRepository
    target_repo: AbstractRepository
    mission_repo: AbstractRepository

    @abstractmethod
    async def commit(self) -> None: ... 

    @abstractmethod
    async def rollback(self) -> None: ...

    @abstractmethod
    async def __aenter__(self) -> "AbstractUnitOfWork": ...

    @abstractmethod
    async def __aexit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None: ...


class UnitOfWork(AbstractUnitOfWork): 
    def __init__(self) -> None: 
        self.session = async_session_factory()

    async def commit(self) -> None: 
        await self.session.commit()

    async def rollback(self) -> None: 
        await self.session.rollback()

    async def __aenter__(self) -> "UnitOfWork": 
        self.spy_cat_repo = SpyCatRepository(self.session) 
        self.target_repo = TargetRepository(self.session)
        self.mission_repo = MissionRepository(self.session)
        return self
    
    async def __aexit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        if exc_type is None:
            await self.commit()
        else: 
            await self.rollback()
        await self.session.close()
