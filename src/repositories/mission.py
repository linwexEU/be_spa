from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete, insert

from src.models.enums import State
from src.utils.repository import AbstractRepository
from src.models.models import Mission


class MissionRepository(AbstractRepository): 
    _model = Mission

    def __init__(self, session: AsyncSession) -> None: 
        self._session = session

    async def create(self, payload: dict) -> int: 
        query = insert(self._model).values(**payload).returning(self._model.id)
        res = await self._session.execute(query) 
        return res.scalar()
    
    async def update(self, entity_id: int, payload: dict) -> int: 
        query =  update(self._model).where(self._model.id == entity_id).values(**payload).returning(self._model.id)
        res = await self._session.execute(query) 
        return res.scalar()
    
    async def assign(self, entity_id: int, spy_cat_id: int) -> int: 
        query =  update(self._model).where(self._model.id == entity_id).values(spy_cat=spy_cat_id).returning(self._model.id)
        res = await self._session.execute(query) 
        return res.scalar()
    
    async def mark_as_completed(self, entity_id: int) -> int: 
        query =  update(self._model).where(self._model.id == entity_id).values(state=State.Completed).returning(self._model.id)
        res = await self._session.execute(query) 
        return res.scalar()
    
    async def delete(self, entity_id: int) -> int: 
        query = delete(self._model).where(self._model.id == entity_id).returning(self._model.id)
        res = await self._session.execute(query) 
        return res.scalar()
    
    async def select(self) -> list[Mission]: 
        query = select(self._model).options(
            selectinload(self._model.fr_spy_cat), 
            selectinload(self._model.fr_target)
        )
        res = await self._session.execute(query) 
        return res.scalars().all() 
    
    async def select_one(self, entity_id: int) -> Optional[Mission]: 
        query = select(self._model).where(self._model.id == entity_id).options(
            selectinload(self._model.fr_spy_cat), 
            selectinload(self._model.fr_target)
        )
        res = await self._session.execute(query) 
        return res.scalar()
