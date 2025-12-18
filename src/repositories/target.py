from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select, update, delete, insert

from src.utils.repository import AbstractRepository
from src.models.models import Target


class TargetRepository(AbstractRepository): 
    _model = Target

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
    
    async def delete(self, entity_id: int) -> int: 
        query = delete(self._model).where(self._model.id == entity_id).returning(self._model.id)
        res = await self._session.execute(query) 
        return res.scalar()
    
    async def select(self) -> list[Target]: 
        query = select(self._model)
        res = await self._session.execute(query) 
        return res.scalars().all() 
    
    async def select_one(self, entity_id: int) -> Optional[Target]: 
        query = select(self._model).where(self._model.id == entity_id)
        res = await self._session.execute(query) 
        return res.scalar()
