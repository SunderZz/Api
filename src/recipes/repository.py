from sqlalchemy.orm import Session
from .models import Recipes

class RecipesRepository:
    async def get_Recipes(self, db: Session)->Recipes:
        return db.query(Recipes).all()
    
    async def get_Recipes_query(self, db: Session, query: str)->Recipes:
            recipes = db.query(recipes).first()
            if recipes is None:
                return None
            return getattr(recipes, query, None)
    
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