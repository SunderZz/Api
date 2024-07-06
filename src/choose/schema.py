from pydantic import BaseModel


class ChooseBase(BaseModel):
    Id_Product: int
    Id_Casual: int
