from pydantic import BaseModel
from datetime import date


class ManageBase(BaseModel):
    Id_Admin: int
    Id_Product: int
    Date_manage: date
