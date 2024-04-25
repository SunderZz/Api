from pydantic import BaseModel
from datetime import date

class UsersAdressesBase(BaseModel):
    Adresse: str
    Phone: str
    Creation: date
    Modification: date | None = None
    Latitude: float
    Longitude: float
