from pydantic import BaseModel


class ProducersBase(BaseModel):
    Document: str
    description: str | None = None
    Id_Users: int
    Id_Producers: int


class ProducersCreateBase(BaseModel):
    Document: str
    description: str | None = None
    Id_Users: int


class ProducersModifyBase(BaseModel):
    Document: str | None = None
    description: str | None = None
    Id_Users: int | None = None
