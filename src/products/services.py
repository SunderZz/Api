from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from datetime import datetime
from .repository import ProductRepository
from .schema import ProductBase, ProductIdBase, ProductRetrievedBase
from common import model_to_dict
from is_on.repository import IsOnRepository
from is_on.router import create_is_on, update_is_on, get_is_on_by_id
from is_on.schema import IsOnBase
from give.router import update_give
from give.schema import GiveCalcBase
from give.repository import GiveRepository


async def get_products_service(
    produit_repository: ProductRepository, db: AsyncSession
) -> list[ProductRetrievedBase]:
    products = await produit_repository.get_product(db)
    products_list = [model_to_dict(product) for product in products]
    return [ProductRetrievedBase(**product_dict) for product_dict in products_list]


async def get_products_discount_service(
    produit_repository: ProductRepository, db: AsyncSession
) -> list[ProductRetrievedBase]:
    products = await produit_repository.get_product_by_discount(db)
    products_list = [model_to_dict(product) for product in products]
    return [ProductRetrievedBase(**product_dict) for product_dict in products_list]


async def get_product_by_name_service(
    products_name: str, products_repository: ProductRepository, db: AsyncSession
) -> list[ProductBase] | ProductBase | None:
    value = await products_repository.get_products_by_name(db, products_name)
    if value is None:
        raise HTTPException(
            status_code=404, detail="product not found or attribute not found"
        )
    if isinstance(value, list):
        products_list = [model_to_dict(product) for product in value]
        return [ProductBase(**product_dict) for product_dict in products_list]
    else:
        product_dict = model_to_dict(value)
        return ProductBase(**product_dict)


async def get_product_id_by_name_service(
    products_name: str, products_repository: ProductRepository, db: AsyncSession
) -> list[ProductIdBase] | ProductIdBase | None:
    value = await products_repository.get_product_id_by_name(db, products_name)
    if value is None:
        raise HTTPException(
            status_code=404, detail="product not found or attribute not found"
        )
    if isinstance(value, list):
        products_list = [model_to_dict(product) for product in value]
        return [ProductIdBase(**product_dict) for product_dict in products_list]
    else:
        product_dict = model_to_dict(value)
        return ProductIdBase(**product_dict)


async def get_product_by_ids_service(
    id: int, products_repository: ProductRepository, db: AsyncSession
) -> ProductRetrievedBase:
    value = await products_repository.get_product_id(db, id)
    if value is None:
        raise HTTPException(
            status_code=404, detail="product not found or attribute not found"
        )
    product_dict = model_to_dict(value)
    return ProductRetrievedBase(**product_dict)


async def get_product_value_by_season_service(
    is_on: int,
    products_repository: ProductRepository,
    is_on_repository: IsOnRepository,
    db: AsyncSession,
) -> list[ProductRetrievedBase]:
    value = await products_repository.get_product(db)
    product_in_season_ids = []
    for product in value:
        seasons = await get_is_on_by_id(is_on, is_on_repository, db)
        if isinstance(seasons, list):
            for season in seasons:
                if product.Id_Product == season.Id_Product:
                    product_in_season_ids.append(product.Id_Product)
        else:
            if product.Id_Product == seasons.Id_Product:
                product_in_season_ids.append(product.Id_Product)
    results = []
    for produit_id in product_in_season_ids:
        result = await get_product_by_ids_service(produit_id, products_repository, db)
        results.append(result)
    return results


async def create_products_service(
    season: int,
    product: ProductBase,
    is_on_repository: IsOnRepository,
    products_repository: ProductRepository,
    db: AsyncSession,
) -> ProductIdBase:
    new_product = await products_repository.create_product(db, product)
    await create_is_on(
        IsOnBase(Id_Season=season, Id_Product=new_product.Id_Product),
        is_on_repository,
        db,
    )
    product_dict = model_to_dict(new_product)
    return ProductIdBase(**product_dict)


async def update_product_service(
    product_id: int,
    product: ProductBase,
    quantity: int,
    season: int | None,
    is_on_repository: IsOnRepository,
    give_repository: GiveRepository,
    product_repository: ProductRepository,
    db: AsyncSession,
) -> ProductBase:
    Timestamp = datetime.now().isoformat()
    given_date_exact = datetime.strptime(Timestamp, "%Y-%m-%dT%H:%M:%S.%f").date()
    updated_product = await product_repository.update_product(db, product_id, product)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="produit_image not found")
    await update_is_on(
        product_id,
        IsOnBase(Id_Product=updated_product.Id_Product, Id_Season=season),
        is_on_repository,
        db,
    )
    await update_give(
        product_id,
        GiveCalcBase(
            Id_Product=product_id, Quantity=quantity, Given_Date=given_date_exact
        ),
        give_repository,
        db,
    )
    produit_image_dict = model_to_dict(updated_product)
    return ProductBase(**produit_image_dict)
