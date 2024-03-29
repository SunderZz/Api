from pydantic import BaseModel

class ProduitImage1Base(BaseModel):
    nom: str |None = None
    lien_image: str |None = None