from pydantic import BaseModel

class UserBase(BaseModel):
    first_name: str