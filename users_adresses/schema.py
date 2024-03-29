from pydantic import BaseModel
from datetime import date

class UsersAdressesBase(BaseModel):
    adresse: str
    phone: int
    creation: date
    modification: date |None = None
    latitude: float
    longitude: float