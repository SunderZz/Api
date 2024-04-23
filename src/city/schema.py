from pydantic import BaseModel

class CityBase(BaseModel):
    name: str
