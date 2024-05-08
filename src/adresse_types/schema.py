from pydantic import BaseModel

class AdresseTypeBase(BaseModel):
    Shipment_Adresse: str |None = None
    Adresse_Bills: str |None = None
    Id_Users_adresses: int
    Id_Users: int