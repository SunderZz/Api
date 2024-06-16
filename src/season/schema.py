from pydantic import BaseModel

class SeasonBase(BaseModel):
    Name: str
    
class SeasonRetrieveBase(BaseModel):
    Name: str
    Id_Season: int
    
    class Config:
        orm_mode = True