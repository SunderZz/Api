from pydantic import BaseModel


class RedactBase(BaseModel):
    Id_Recipes: int
    Id_Admin: int
