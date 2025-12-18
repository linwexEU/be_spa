from src.api.services.commands.base import Command
from src.repositories.spy_cat import SpyCatRepository


class ValidateBreedCommand(Command): 
    def __init__(self, breed: str, breeds: list[str]) -> None: 
        self.breed = breed 
        self.breeds = breeds

    async def execute(self) -> bool: 
        L, R = 0, len(self.breeds) - 1
        while L <= R: 
            M = (L + R) // 2
            if self.breeds[M] == self.breed: 
                return True
            
            if self.breeds[M] < self.breed: 
                L = M + 1
            else: 
                R  = M - 1
        return False


class CheckSpyCatExistCommand(Command): 
    def __init__(self, spy_cat_id: int, repo: SpyCatRepository) -> None: 
        self.spy_cat_id = spy_cat_id
        self.repo = repo

    async def execute(self) -> bool: 
        spy_cat = await self.repo.select_one(self.spy_cat_id)
        print(spy_cat)
        if spy_cat is None: 
            return False 
        return True
