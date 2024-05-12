from pydantic import BaseModel

class ManageBase(BaseModel):
    Id_Admin: int
    Id_Product: int
    Date_manage: str
