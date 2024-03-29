from pydantic import BaseModel

class CodePostalBase(BaseModel):
    code_postal: int
