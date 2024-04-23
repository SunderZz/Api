from pydantic import BaseModel

class TvaBase(BaseModel):
    name: str
    rate: int