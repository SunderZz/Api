from pydantic import BaseModel


class IsOnBase(BaseModel):
    Id_Season: int
    Id_Product: int
