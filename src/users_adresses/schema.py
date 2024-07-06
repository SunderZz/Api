from pydantic import BaseModel
from datetime import date


class UsersAdressesBase(BaseModel):
    Adresse: str
    Phone: int
    Creation: date
    Modification: date | None = None
    Latitude: float | None = None
    Longitude: float | None = None


class UsersAdressesModifyBase(BaseModel):
    Adresse: str
    Phone: int
    Modification: date


class UsersCreateAdressesBase(BaseModel):
    Id_Users_adresses: int
    Adresse: str
    Phone: int
    Creation: date | None = None
    Modification: date | None = None
