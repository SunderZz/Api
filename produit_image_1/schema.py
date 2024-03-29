from pydantic import BaseModel

class ProduitImageBase(BaseModel):
    nom: str |None = None
    lien_image: str |None = None