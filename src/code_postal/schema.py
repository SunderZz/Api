from pydantic import BaseModel

class CodePostalBase(BaseModel):
    code_postal: int

class CodePostalIdBase(BaseModel):
    Id_Code_Postal: int
