import recipes.models as models
from .schema import RecipesBase,RecipesCreateBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .repository import RecipesRepository
from .services import (
    search_recipes_service,
    get_recipes_service,
    get_recipes_value_service,
    get_recipes_by_products_service,
    create_recipes_service,
    update_recipes_service
)
from products.repository import ProductRepository
from found.repository import FoundRepository

router = APIRouter(tags=["recipes"])

@router.get(
    "/recipes/search",
    status_code=status.HTTP_200_OK,
    response_model=list[RecipesBase] | RecipesBase | None,
)
async def search_recipes(
    query: str,
    recipes_repository: RecipesRepository = Depends(RecipesRepository),
    db: AsyncSession = Depends(get_db),
) -> list[RecipesBase] | RecipesBase | None:
    return await search_recipes_service(query, recipes_repository, db)

@router.get(
    "/recipes/", status_code=status.HTTP_200_OK, response_model=list[RecipesBase]
)
async def get_recipes(
    recipes_repository: RecipesRepository = Depends(RecipesRepository),
    db: AsyncSession = Depends(get_db),
) -> list[RecipesBase]:
    return await get_recipes_service(recipes_repository, db)

@router.get("/recipes/{recipe}", response_model=list[RecipesBase] | RecipesBase | None)
async def get_recipes_value(
    product: str,
    recipe: str,
    recipes_repository: RecipesRepository = Depends(RecipesRepository),
    db: AsyncSession = Depends(get_db),
) -> list[RecipesBase] | RecipesBase | None:
    return await get_recipes_value_service(product, recipe, recipes_repository, db)

@router.get("/recipes_id", response_model=RecipesBase)
async def get_recipes_by_id(
    recipe: int,
    recipes_repository: RecipesRepository = Depends(RecipesRepository),
    db: AsyncSession = Depends(get_db),
) -> RecipesBase:
    return await get_recipes_by_products_service(recipe, recipes_repository, db)

@router.post(
    "/recipes/", status_code=status.HTTP_201_CREATED, response_model=RecipesBase
)
async def create_recipes(
    recipes: RecipesCreateBase,
    products_repository: ProductRepository = Depends(ProductRepository),
    found_repository: FoundRepository = Depends(FoundRepository),
    recipes_repository: RecipesRepository = Depends(RecipesRepository),
    db: AsyncSession = Depends(get_db),
) -> RecipesBase:
    return await create_recipes_service(recipes, products_repository, found_repository, recipes_repository, db)

@router.put(
    "/recipes/{recipes_id}", status_code=status.HTTP_200_OK, response_model=RecipesBase
)
async def update_recipes(
    recipes_id: int,
    recipes: RecipesCreateBase,
    recipes_repository: RecipesRepository = Depends(RecipesRepository),
    db: AsyncSession = Depends(get_db),
) -> RecipesBase:
    return await update_recipes_service(recipes_id, recipes, recipes_repository, db)
