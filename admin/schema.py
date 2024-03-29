from pydantic import BaseModel

class AdminBase(BaseModel):
    id_users: int