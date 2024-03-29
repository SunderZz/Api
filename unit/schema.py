from pydantic import BaseModel

class UnitBase(BaseModel):
    kg: float |None = None
    litre: int |None = None
    unit: int |None = None
    gramme: int |None = None