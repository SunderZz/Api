from pydantic import BaseModel


class CustomersBase(BaseModel):
    Id_Casual: int


class CustomersUserBase(BaseModel):
    Id_Users: int
