from pydantic import BaseModel

class TvaBase(BaseModel):
    Name: str
    Rate: int

class TvaCalculationResult(BaseModel):
    value: float