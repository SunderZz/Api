from pydantic import BaseModel


class ProduitImageBase(BaseModel):
    Nom: str | None = None
    lien_image: str | None = None
