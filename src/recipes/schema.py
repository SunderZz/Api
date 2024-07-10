from pydantic import BaseModel


class RecipesBase(BaseModel):
    description: str | None = None
    Title: str | None = None
    Recipe: str | None = None
    ingredient: str | None = None
    Id_Recipes: int


class RecipesCreateBase(BaseModel):
    description: str | None = None
    Title: str | None = None
    Recipe: str | None = None
    ingredient: str | None = None
