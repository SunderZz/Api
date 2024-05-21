from datetime import date
from pydantic import BaseModel

class ProductBase(BaseModel):
    Name: str
    Description: str |None = None
    Price_ht: float
    Active: bool
    Date_activation: date |None = None
    Date_stop: date |None = None
    Discount: float |None = None
    Id_tva: int

class ProductIdBase(BaseModel):
    Id_Product : int
