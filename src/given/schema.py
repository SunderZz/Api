from pydantic import BaseModel


class GivenBase(BaseModel):
    Id_Notice: int
    Id_Product: int
