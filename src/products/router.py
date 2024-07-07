import products.models as models
from .schema import ProductBase, ProductIdBase, ProductRetrievedBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from database import engine2, AsyncSessionLocal
from .repository import ProductRepository
from .services import (
    get_products_service,
    get_products_discount_service,
    get_product_by_name_service,
    get_product_id_by_name_service,
    get_product_by_ids_service,
    get_product_value_by_season_service,
    create_products_service,
    update_product_service,
)
from is_on.repository import IsOnRepository

router = APIRouter(tags=["products"])


@router.get(
    "/products/",
    status_code=status.HTTP_200_OK,
    response_model=list[ProductRetrievedBase],
)
async def get_products(
    produit_repository: ProductRepository = Depends(ProductRepository),
    db: AsyncSession = Depends(get_db),
) -> list[ProductRetrievedBase]:
    return await get_products_service(produit_repository, db)


@router.get(
    "/products_discount/",
    status_code=status.HTTP_200_OK,
    response_model=list[ProductRetrievedBase],
)
async def get_products_discount(
    produit_repository: ProductRepository = Depends(ProductRepository),
    db: AsyncSession = Depends(get_db),
) -> list[ProductRetrievedBase]:
    return await get_products_discount_service(produit_repository, db)


@router.get(
    "/products_by_name/{products}", response_model=ProductBase | list[ProductBase]
)
async def get_product_by_name(
    products_name: str,
    products_repository: ProductRepository = Depends(ProductRepository),
    db: AsyncSession = Depends(get_db),
) -> list[ProductBase] | ProductBase | None:
    return await get_product_by_name_service(products_name, products_repository, db)


@router.get(
    "/products_id_by_name/{products}",
    response_model=ProductIdBase | list[ProductIdBase] | None,
)
async def get_product_id_by_name(
    products_name: str,
    products_repository: ProductRepository = Depends(ProductRepository),
    db: AsyncSession = Depends(get_db),
) -> list[ProductIdBase] | ProductIdBase | None:
    return await get_product_id_by_name_service(products_name, products_repository, db)


@router.get(
    "/products_by_id/",
    response_model=ProductRetrievedBase | list[ProductRetrievedBase] | None,
)
async def get_product_by_ids(
    id: int,
    products_repository: ProductRepository = Depends(ProductRepository),
    db: AsyncSession = Depends(get_db),
) -> list[ProductRetrievedBase] | ProductRetrievedBase | None:
    return await get_product_by_ids_service(id, products_repository, db)


@router.get(
    "/products/season",
    description="retrieve product by season",
    response_model=ProductRetrievedBase | list[ProductRetrievedBase],
)
async def get_product_value_by_season(
    is_on: int,
    products_repository: ProductRepository = Depends(ProductRepository),
    is_on_repository: IsOnRepository = Depends(IsOnRepository),
    db: AsyncSession = Depends(get_db),
) -> ProductRetrievedBase | list[ProductRetrievedBase]:
    return await get_product_value_by_season_service(
        is_on, products_repository, is_on_repository, db
    )


@router.post(
    "/products/", status_code=status.HTTP_201_CREATED, response_model=ProductIdBase
)
async def create_products(
    season: int,
    product: ProductBase,
    is_on_repository: IsOnRepository = Depends(IsOnRepository),
    products_repository: ProductRepository = Depends(ProductRepository),
    db: AsyncSession = Depends(get_db),
) -> ProductIdBase:
    return await create_products_service(
        season, product, is_on_repository, products_repository, db
    )


@router.put(
    "/products/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductBase
)
async def update_product(
    product_id: int,
    product: ProductBase,
    season: int | None = None,
    is_on_repository: IsOnRepository = Depends(IsOnRepository),
    product_repository: ProductRepository = Depends(ProductRepository),
    db: AsyncSession = Depends(get_db),
) -> ProductBase:
    return await update_product_service(
        product_id, product, season, is_on_repository, product_repository, db
    )
