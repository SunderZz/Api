from pydantic import BaseModel
from datetime import date


class PayBase(BaseModel):
    Id_Payments: int
    Id_Casual: int
    Date1: date
