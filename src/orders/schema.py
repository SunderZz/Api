from datetime import date
from pydantic import BaseModel

class OrdersBase(BaseModel):
    Command_Date: date
    Status: bool
    Preference_Ship: str
    Ship_Date: date |None = None
    Id_Casual: int

class OrdersIdBase(BaseModel):
    Id_Orders:int

