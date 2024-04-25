from pydantic import BaseModel, Field
from datetime import date

class UsersAdressesBase(BaseModel):
    Adresse: str
    Phone: str
    Creation: date
    Modification: date | None = None
    Latitude: float
    Longitude: float

class UsersAdressesInDB(UsersAdressesBase):
    Id_Users_adresses: int