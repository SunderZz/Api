from pydantic import BaseModel


class UnitBase(BaseModel):
    Kg: float | None = None
    Litre: int | None = None
    Unit: int | None = None
    Gramme: int | None = None


class UnitIdBase(BaseModel):
    Id_Unit: int
