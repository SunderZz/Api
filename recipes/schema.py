from pydantic import BaseModel

class RecipesBase(BaseModel):
    description: str |None = None
    title: str |None = None
    recipe: str |None = None
    ingredient: str |None = None