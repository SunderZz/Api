from pydantic import BaseModel
from datetime import date

class UsersAdressesBase(BaseModel):
    Adresse: str
    Phone: str 
    Creation: date | None = None
    Modification: date | None = None
    Latitude: float |None = None
    Longitude: float |None = None
