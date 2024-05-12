from pydantic import BaseModel

class LinedeBase(BaseModel):
    Id_Orders: int
    Id_Product: int
    qte: str

