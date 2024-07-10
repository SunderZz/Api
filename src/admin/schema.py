from pydantic import BaseModel


class AdminBase(BaseModel):
    Id_Admin: int


class AdminCreateBase(BaseModel):
    Id_Users: int
