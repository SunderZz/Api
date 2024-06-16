from pydantic import BaseModel

class TvaBase(BaseModel):
    Name: str
    Rate: int
    Id_Tva: int

class TvaCalculationResult(BaseModel):
    value: float