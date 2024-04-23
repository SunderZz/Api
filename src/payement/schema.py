from datetime import date
from pydantic import BaseModel

class PaymentBase(BaseModel):
    payment_date: date
    amount: int
    bills: str
    status: bool
    id_orders: int