from pydantic import BaseModel

class Casual5Base(BaseModel):
    nom: str |None = None