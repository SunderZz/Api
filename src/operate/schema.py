from datetime import date
from pydantic import BaseModel


class OperateBase(BaseModel):
    Id_Admin: int
    Id_Casual: int
    Date_operate: date
