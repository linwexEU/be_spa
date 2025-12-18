import os

from dotenv import find_dotenv, load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(current_dir)

load_dotenv(find_dotenv(".env"))


class Settings: 
    @property
    def DB_HOST(self) -> str: 
        return os.environ.get("DB_HOST") 

    @property
    def DB_PORT(self) -> int: 
        return int(os.environ.get("DB_PORT"))
    
    @property
    def DB_USER(self) -> str: 
        return os.environ.get("DB_USER")
    
    @property
    def DB_PASS(self) -> str: 
        return os.environ.get("DB_PASS")
    
    @property
    def DB_NAME(self) -> str: 
        return os.environ.get("DB_NAME")
    
    @property 
    def DATABASE_URL(self) -> str: 
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def BREED_API_URL(self) -> str: 
        return "https://api.thecatapi.com/v1/breeds"
    

settings = Settings()
