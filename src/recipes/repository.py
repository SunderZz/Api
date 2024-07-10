from sqlalchemy.ext.asyncio import AsyncSession
from .models import Recipes
from sqlalchemy.future import select


class RecipesRepository:
    async def get_Recipes(self, db: AsyncSession) -> list[Recipes]:
        result = await db.execute(select(Recipes))
        return result.scalars().all()

    async def get_Recipes_query(self, db: AsyncSession, id: int) -> Recipes:
        result = await db.execute(select(Recipes).filter(Recipes.Id_Recipes == id))
        return result.scalar_one_or_none()

    async def create_Recipes(self, db: AsyncSession, recipes: Recipes) -> Recipes:
        db_recipes = Recipes(**recipes.dict())
        db.add(db_recipes)
        await db.commit()
        await db.refresh(db_recipes)
        return db_recipes

    async def update_Recipes(
        self, db: AsyncSession, recipes_id: int, recipes_data: Recipes
    ) -> Recipes:
        result = await db.execute(
            select(Recipes).filter(Recipes.Id_Recipes == recipes_id)
        )
        db_recipes = result.scalar_one_or_none()
        if db_recipes is None:
            return None
        for key, value in recipes_data.__dict__.items():
            if hasattr(db_recipes, key) and value is not None:
                setattr(db_recipes, key, value)
        await db.commit()
        return db_recipes

    async def find_recipe_by_query(
        self, db: AsyncSession, query: str
    ) -> list[Recipes] | None:
        all_recipes = await self.get_Recipes(db)
        matching_recipes = []

        for recipe in all_recipes:
            ingredients_list = [
                ingredient.strip().lower()
                for ingredient in recipe.ingredient.split(".")
            ]
            if query.lower() in ingredients_list:
                matching_recipes.append(recipe)

        return matching_recipes if matching_recipes else None
