from pydantic import BaseModel


class CityBase(BaseModel):
    Name: str


class CityIdBase(BaseModel):
    Id_City: int
