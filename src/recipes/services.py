from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import RecipesRepository
from .schema import RecipesBase, RecipesCreateBase
from common import model_to_dict
from products.router import get_product_id_by_name
from products.repository import ProductRepository
from found.router import create_found
from found.repository import FoundRepository
from found.schema import FoundBase


async def search_recipes_service(
    query: str, recipes_repository: RecipesRepository, db: AsyncSession
) -> list[RecipesBase] | RecipesBase | None:
    result = await recipes_repository.find_recipe_by_query(db, query)
    if not result:
        return None
    if isinstance(result, list):
        recipes_list = [model_to_dict(recipes) for recipes in result]
        return [RecipesBase(**recipes_dict) for recipes_dict in recipes_list]
    else:
        product_dict = model_to_dict(result)
        return RecipesBase(**product_dict)


async def get_recipes_service(
    recipes_repository: RecipesRepository, db: AsyncSession
) -> list[RecipesBase]:
    recipes = await recipes_repository.get_Recipes(db)
    recipes_list = [model_to_dict(recipe) for recipe in recipes]
    return [RecipesBase(**recipes_dict) for recipes_dict in recipes_list]


async def get_recipes_value_service(
    product: str, recipe: str, recipes_repository: RecipesRepository, db: AsyncSession
) -> list[RecipesBase] | RecipesBase | None:
    recipes_id = await recipes_repository.get_Recipes_query(db, recipe)
    if recipes_id is None:
        raise HTTPException(
            status_code=404, detail="recipes not found or attribute not found"
        )
    ingredients_list = recipes_id.ingredient
    if product in ingredients_list:
        recipes_instance = await search_recipes_service(product, recipes_repository, db)
        return recipes_instance


async def get_recipes_by_products_service(
    recipe: int, recipes_repository: RecipesRepository, db: AsyncSession
) -> RecipesBase:
    value = await recipes_repository.get_Recipes_query(db, recipe)
    if value is None:
        raise HTTPException(
            status_code=404, detail="recipes not found or attribute not found"
        )
    recipes_dict = model_to_dict(value)
    return RecipesBase(**recipes_dict)


async def create_recipes_service(
    recipes: RecipesCreateBase,
    products_repository: ProductRepository,
    found_repository: FoundRepository,
    recipes_repository: RecipesRepository,
    db: AsyncSession,
) -> RecipesBase:
    new_recipes = await recipes_repository.create_Recipes(db, recipes)
    if new_recipes.ingredient:
        cleaned_ingredient = new_recipes.ingredient.replace(",", "")
        ingredients_list = cleaned_ingredient.split()
        for ingredient_array in ingredients_list:
            ingredient = await get_product_id_by_name(
                ingredient_array, products_repository, db
            )
            for ingredient_obj in ingredient:
                await create_found(
                    FoundBase(
                        Id_Recipes=new_recipes.Id_Recipes,
                        Id_Product=ingredient_obj.Id_Product,
                    ),
                    found_repository,
                    db,
                )
    recipes_dict = model_to_dict(new_recipes)
    return RecipesBase(**recipes_dict)


async def update_recipes_service(
    recipes_id: int,
    recipes: RecipesCreateBase,
    recipes_repository: RecipesRepository,
    db: AsyncSession,
) -> RecipesBase:
    updated_recipes = await recipes_repository.update_Recipes(db, recipes_id, recipes)
    if updated_recipes is None:
        raise HTTPException(status_code=404, detail="recipes not found")
    recipes_dict = model_to_dict(updated_recipes)
    return RecipesBase(**recipes_dict)
