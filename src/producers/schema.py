from pydantic import BaseModel

class ProducersBase(BaseModel):
    Document: str
    description: str |None = None
    Id_Users: int