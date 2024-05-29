import products.models as models
from typing import Annotated
from .schema import ProductBase,ProductIdBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from database import engine2, AsyncSessionLocal
from .repository import ProductRepository
from common import model_to_dict
from is_on.repository import IsOnRepository
from is_on.router import create_is_on, update_is_on,get_is_on_by_id
from is_on.schema import IsOnBase

router = APIRouter(tags=["products"])


@router.get("/products/", status_code=status.HTTP_200_OK, response_model=list[ProductBase])
async def get_products(produit_repository: ProductRepository = Depends(ProductRepository),db:AsyncSession = Depends(get_db))-> list[ProductBase]:
    products = await produit_repository.get_product(db)
    products_list = [model_to_dict(product) for product in products]
    return [ProductBase(**product_dict) for product_dict in products_list]

@router.get("/products_discount/", status_code=status.HTTP_200_OK, response_model=list[ProductBase])
async def get_products_discount(produit_repository: ProductRepository = Depends(ProductRepository),db:AsyncSession = Depends(get_db))-> list[ProductBase]:
    products = await produit_repository.get_product_by_discount(db)
    products_list = [model_to_dict(product) for product in products]
    return [ProductBase(**product_dict) for product_dict in products_list]

@router.get("/products_by_name/{products}", response_model=ProductBase | list[ProductBase])
async def get_product_by_name(products_name: str, products_repository: ProductRepository = Depends(ProductRepository), db:AsyncSession = Depends(get_db)) -> list[ProductBase]|ProductBase|None:
    value = await products_repository.get_products_by_name(db, products_name)
    if value is None:
        raise HTTPException(status_code=404, detail="product not found or attribute not found")
    if isinstance(value, list):
        products_list = [model_to_dict(product) for product in value]
        return [ProductBase(**product_dict) for product_dict in products_list]
    else:
        product_dict = model_to_dict(value)
        return ProductBase(**product_dict)
    
@router.get("/products_id_by_name/{products}", response_model=ProductIdBase | list[ProductIdBase] |None)
async def get_product_id_by_name(products_name: str, products_repository: ProductRepository = Depends(ProductRepository), db:AsyncSession = Depends(get_db)) -> list[ProductIdBase]|ProductIdBase|None:
    value = await products_repository.get_product_id_by_name(db, products_name)
    if value is None:
        raise HTTPException(status_code=404, detail="product not found or attribute not found")
    if isinstance(value, list):
        products_list = [model_to_dict(product) for product in value]
        return [ProductIdBase(**product_dict) for product_dict in products_list]
    else:
        product_dict = model_to_dict(value)
        return ProductIdBase(**product_dict)
    
@router.get("/products_by_id/", response_model=ProductBase | list[ProductBase] |None)
async def get_product_by_ids(id: int, products_repository: ProductRepository = Depends(ProductRepository), db:AsyncSession = Depends(get_db)) -> list[ProductBase]|ProductBase|None:
    value = await products_repository.get_product_id(db, id)
    if value is None:
        raise HTTPException(status_code=404, detail="product not found or attribute not found")
    product_dict = model_to_dict(value)
    return ProductBase(**product_dict)

@router.get("/products/{products}/query", response_model=ProductIdBase)
async def get_product_value(products: int, products_repository: ProductRepository = Depends(ProductRepository), db:AsyncSession = Depends(get_db)) -> ProductIdBase:
    value = await products_repository.get_product_query(db, products)
    if value is None:
        raise HTTPException(status_code=404, detail="product not found or attribute not found")
    product_dict = model_to_dict(value)
    return ProductIdBase(**product_dict)

@router.get("/products/season", response_model=ProductBase |list[ProductBase])
async def get_product_value_by_season(is_on: int, products_repository: ProductRepository = Depends(ProductRepository),is_on_repository: IsOnRepository = Depends(IsOnRepository), db:AsyncSession = Depends(get_db)) -> ProductBase |list[ProductBase]:
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
        result = await get_product_by_ids(produit_id, products_repository, db)
        results.append(result)
    return results


@router.post("/products/", status_code=status.HTTP_201_CREATED, response_model=ProductIdBase)
async def create_products(season:int,product: ProductBase,is_on_repository: IsOnRepository = Depends(IsOnRepository),products_repository: ProductRepository = Depends(ProductRepository), db:AsyncSession = Depends(get_db))-> ProductIdBase:
    new_product = await products_repository.create_product(db, product)
    await create_is_on(IsOnBase(Id_Season=season,Id_Product=new_product.Id_Product),is_on_repository,db)
    product_dict = model_to_dict(new_product) 
    return ProductIdBase(**product_dict)

@router.put("/products/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductBase)
async def update_product(product_id: int, product: ProductBase,season:int|None = None,is_on_repository: IsOnRepository = Depends(IsOnRepository),product_repository: ProductRepository = Depends(ProductRepository), db:AsyncSession = Depends(get_db))-> ProductBase:
    updated_product = await product_repository.update_product(db, product_id, product)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="produit_image not found")
    await update_is_on(IsOnBase(Id_Product=updated_product.Id_Product,Id_Season=season),is_on_repository,db)
    produit_image_dict = model_to_dict(updated_product) 
    return ProductBase(**produit_image_dict)
    
