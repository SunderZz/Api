from pydantic import BaseModel

class UserBase(BaseModel):
    F_Name: str
    Name : str
    Mail: str
    Password: str
    active: bool