from fastapi import Depends

from src.utils.unit_of_work import AbstractUnitOfWork


class BaseService: 
    def __init__(self, uow: AbstractUnitOfWork = Depends()) -> None: 
        self.uow: AbstractUnitOfWork = uow
