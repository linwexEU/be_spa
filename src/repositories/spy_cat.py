from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select, update, delete, insert

from src.utils.repository import AbstractRepository
from src.models.models import SpyCat
from src.exceptions.repository import UniqueError


class SpyCatRepository(AbstractRepository): 
    _model = SpyCat

    def __init__(self, session: AsyncSession) -> None: 
        self._session = session

    async def create(self, payload: dict) -> int: 
        try:
            query = insert(self._model).values(**payload).returning(self._model.id)
            res = await self._session.execute(query) 
            return res.scalar()
        except IntegrityError as exc: 
            if exc.orig.pgcode == "23505": 
                raise UniqueError
            raise
        
    async def update(self, entity_id: int, payload: dict) -> int: 
        query =  update(self._model).where(self._model.id == entity_id).values(**payload).returning(self._model.id)
        res = await self._session.execute(query) 
        return res.scalar()
    
    async def delete(self, entity_id: int) -> int: 
        query = delete(self._model).where(self._model.id == entity_id).returning(self._model.id)
        res = await self._session.execute(query) 
        return res.scalar()
    
    async def select(self) -> list[SpyCat]: 
        query = select(self._model)
        res = await self._session.execute(query) 
        return res.scalars().all() 
    
    async def select_one(self, entity_id: int) -> Optional[SpyCat]: 
        query = select(self._model).where(self._model.id == entity_id)
        res = await self._session.execute(query) 
        return res.scalar()
