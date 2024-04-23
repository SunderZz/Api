from datetime import date
from pydantic import BaseModel

class OrdersBase(BaseModel):
    command_date: date
    status: bool
    preference_ship: str
    ship_date: date |None = None
    id_casual: int