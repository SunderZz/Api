from datetime import date
from pydantic import BaseModel

class PaymentBase(BaseModel):
    Payment_date: date
    Amount: int
    Bills: str
    Status: bool
    Id_Orders: int