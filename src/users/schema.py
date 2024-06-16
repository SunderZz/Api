from pydantic import BaseModel, Field

class UserBase(BaseModel):
    Id_Users: int
    F_Name: str
    Name: str
    Mail: str
    active: bool
    token: str | None = None

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    F_Name: str
    Name: str
    Mail: str
    Password: str
    active: bool = Field(default=True)

class UserModify(BaseModel):
    F_Name: str | None = None
    Name: str | None = None
    Mail: str | None = None
    Password: str
    active: bool = Field(default=True)

class LogoutRequest(BaseModel):
    user_id: int