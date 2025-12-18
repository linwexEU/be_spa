from pydantic import BaseModel


class Response(BaseModel): 
    entity_id: int
