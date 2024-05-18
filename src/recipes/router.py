import recipes.models as models
from typing import Annotated
from .schema import RecipesBase
from fastapi import APIRouter, FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal
from .repository import RecipesRepository
from common import model_to_dict

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["recipes"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]



@router.get("/recipes/", status_code=status.HTTP_200_OK, response_model=list[RecipesBase])
async def get_recipes(recipes_repository: RecipesRepository = Depends(RecipesRepository),db: Session = Depends(get_db))-> list[RecipesBase]:
    recipes = await recipes_repository.get_Recipes(db)
    recipes_list = [model_to_dict(recipe) for recipe in recipes]
    return [RecipesBase(**recipes_dict) for recipes_dict in recipes_list]


@router.get("/recipes/{recipe}", response_model=RecipesBase)
async def get_recipes_value(recipe: int, recipes_repository: RecipesRepository = Depends(RecipesRepository), db: Session = Depends(get_db)) -> RecipesBase:
    value = await recipes_repository.get_Recipes_query(db, recipe)
    if value is None:
        raise HTTPException(status_code=404, detail="recipes not found or attribute not found")
    return RecipesBase(value=value)


@router.post("/recipes/", status_code=status.HTTP_201_CREATED, response_model=RecipesBase)
async def create_recipes(recipes: RecipesBase,recipes_repository: RecipesRepository = Depends(RecipesRepository), db: Session = Depends(get_db))-> RecipesBase:
    new_recipes = await recipes_repository.create_Recipes(db, recipes)
    recipes_dict = model_to_dict(new_recipes) 
    return RecipesBase(**recipes_dict)

@router.put("/recipes/{recipes_id}", status_code=status.HTTP_200_OK, response_model=RecipesBase)
async def update_recipes(recipes_id: int, recipes: RecipesBase,recipes_repository: RecipesRepository = Depends(RecipesRepository), db: Session = Depends(get_db))-> RecipesBase:
    updated_recipes = await recipes_repository.update_Recipes(db, recipes_id, recipes)
    print(updated_recipes)
    if updated_recipes is None:
        raise HTTPException(status_code=404, detail="recipes not found")
    recipes_dict = model_to_dict(updated_recipes) 
    return RecipesBase(**recipes_dict)

