from pydantic import BaseModel


class PayBase(BaseModel):
    Id_Payments: int
    Id_Casual: int
    Date1: str
