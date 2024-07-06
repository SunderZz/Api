from pydantic import BaseModel


class LocatedBase(BaseModel):
    Id_Users_adresses: int
    Id_Code_Postal: int
