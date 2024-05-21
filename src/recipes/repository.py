from sqlalchemy.orm import Session
from .models import Recipes

class RecipesRepository:
    async def get_Recipes(self, db: Session)->Recipes:
        return db.query(Recipes).all()
    
    async def get_Recipes_query(self,db: Session, ingredient: int)->Recipes:
        return db.query(Recipes).filter(Recipes.ingredient == ingredient).first()
    
    async def create_Recipes(self, db: Session, recipes: Recipes)->Recipes:
        db_recipes = Recipes(**recipes.dict())
        db.add(db_recipes)
        db.commit()
        db.refresh(db_recipes)
        return db_recipes

    async def update_Recipes(self, db: Session,recipes_id: int, recipes_data: Recipes)->Recipes:
        db_recipes = db.query(Recipes).filter(Recipes.Id_Recipes == recipes_id).first()
        if db_recipes is None:
            return None
        for key, value in recipes_data.__dict__.items():
            if hasattr(db_recipes, key) and value is not None:
                setattr(db_recipes, key, value)
        db.commit()
        return db_recipes   
    
    async def find_recipe_by_query(self, db: Session, query: str) -> list[Recipes] | None:
        all_recipes = await self.get_Recipes(db)
        matching_recipes = []
        
        for recipe in all_recipes:
            ingredients_list = recipe.ingredient.split()
            if query.lower() in [ingredient.lower() for ingredient in ingredients_list]:
                matching_recipes.append(recipe)
        
        return matching_recipes if matching_recipes else None