from datetime import date
from pydantic import BaseModel


class OrdersBase(BaseModel):
    Command_Date: date | None = None
    Status: bool | None = None
    Preference_Ship: str | None = None
    Ship_Date: date | None = None
    Id_Casual: int

class OrdersForBillsBase(BaseModel):
    Command_Date: date | None = None
    Status: bool | None = None
    Preference_Ship: str | None = None
    Ship_Date: date | None = None
    Id_Orders: int


class OrdersIdBase(BaseModel):
    Id_Orders: int
