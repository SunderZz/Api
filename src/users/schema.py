from pydantic import BaseModel

class UserBase(BaseModel):
    F_Name: str
    name : str
    mail: str
    password: str
    