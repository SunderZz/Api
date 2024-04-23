from pydantic import BaseModel

class AdresseTypeBase(BaseModel):
    shipment_adresse: str |None = None
    adresse_bills: str |None = None
    id_users_adresses: int
    id_users: int