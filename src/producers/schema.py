from pydantic import BaseModel

class ProducersBase(BaseModel):
    document: str
    description: str |None = None
    id_users: int