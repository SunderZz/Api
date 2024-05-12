from datetime import date
from pydantic import BaseModel

class CarryOnBase(BaseModel):
    Id_Producers: int
    Id_Admin: int
    date_carry: date
