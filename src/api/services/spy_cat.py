from fastapi import Depends

from src.exceptions.service import SpyCatAlreadyExists, SpyCatNotFound, ValidateBreedError
from src.schemas.spy_cat import CreateSpyCatRequest, CreateSpyCatResponse, ListInfo, Info, \
                                DeleteSpyCatResponse, UpdateSpyCatRequest, UpdateSpyCatResponse
from src.api.services.commands.spy_cat import ValidateBreedCommand
from src.utils.http_client import HttpClient
from src.utils.service import BaseService
from src.utils.unit_of_work import AbstractUnitOfWork
from src.exceptions.repository import UniqueError
from src.utils.logger import log


class SpyCatService(BaseService): 
    def __init__(self, uow: AbstractUnitOfWork = Depends()) -> None:
        self.uow: AbstractUnitOfWork = uow
        self.http = HttpClient()

    @log
    async def select_all_spy_cats(self) -> ListInfo: 
        async with self.uow: 
            spy_cats = await self.uow.spy_cat_repo.select()
            return ListInfo.from_orm(spy_cats)

    @log 
    async def select_one_spy_cat(self, spy_cat_id: int) -> Info: 
        async with self.uow: 
            try:
                spy_cat = await self.uow.spy_cat_repo.select_one(spy_cat_id)
                return Info.from_orm(spy_cat)
            except AttributeError: 
                raise SpyCatNotFound(f"Spy cat with id={spy_cat_id} not found")

    @log
    async def create_spy_cat(self, payload: CreateSpyCatRequest) -> CreateSpyCatResponse: 
        # Validate breed
        breeds = await self.http.get_breeds_from_api()

        cmd = ValidateBreedCommand(payload.breed, breeds)
        res = await cmd.execute()

        if not res: 
            raise ValidateBreedError("Incorrect breed!")

        async with self.uow: 
            try:
                spy_cat_id = await self.uow.spy_cat_repo.create(payload.model_dump())
            except UniqueError: 
                raise SpyCatAlreadyExists(f"Spy Cat with name={payload.name} already exists")
            return CreateSpyCatResponse(entity_id=spy_cat_id)

    @log
    async def delete_spy_cat(self, spy_cat_id: int) -> DeleteSpyCatResponse: 
        async with self.uow: 
            entity_id = await self.uow.spy_cat_repo.delete(spy_cat_id)
            if not entity_id: 
                raise SpyCatNotFound(f"Spy cat with id={spy_cat_id} not found")
            return DeleteSpyCatResponse(entity_id=entity_id)

    @log
    async def update_spy_cat(self, spy_cat_id: int, payload: UpdateSpyCatRequest) -> UpdateSpyCatResponse: 
        # Validate breed
        if payload.breed is not None: 
            breeds = await self.http.get_breeds_from_api()

            cmd = ValidateBreedCommand(payload.breed, breeds)
            res = await cmd.execute()

            if not res: 
                raise ValidateBreedError("Incorrect breed!")

        async with self.uow: 
            entity_id = await self.uow.spy_cat_repo.update(
                spy_cat_id, payload.model_dump(exclude_none=True)
            )
            if entity_id is None: 
                raise SpyCatNotFound(f"Spy cat with id={spy_cat_id} not found")
            return UpdateSpyCatResponse(entity_id=entity_id)
