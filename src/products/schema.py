from datetime import date
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str |None = None
    price_ht: float
    active: bool
    date_activation: date |None = None
    date_stop: date |None = None
    discount: float |None = None
    id_tva: int