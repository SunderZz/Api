from pydantic import BaseModel


class UnitBase(BaseModel):
    Kg: float | None = None
    Litre: float | None = None
    Unit: int | None = None
    Gramme: float | None = None


class UnitIdBase(BaseModel):
    Id_Unit: int
