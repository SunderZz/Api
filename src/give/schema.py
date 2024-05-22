from pydantic import BaseModel
from datetime import date

class GiveBase(BaseModel):
    Id_Producers: int
    Id_Unit: int
    Id_Product: int
    Quantity: int
    Given_Date: date

class GiveCalcBase(BaseModel):
    Id_Product: int
    Quantity: int
    Given_Date: date


