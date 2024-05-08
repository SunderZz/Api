import products.models as models
from typing import Annotated
from .schema import ProductBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal
from .repository import ProductRepository
from common import model_to_dict

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["products"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]

@router.get("/products/", status_code=status.HTTP_200_OK, response_model=list[ProductBase])
async def get_products(produit_repository: ProductRepository = Depends(ProductRepository),db: Session = Depends(get_db))-> list[ProductBase]:
    products = await produit_repository.get_product(db)
    products_list = [model_to_dict(product) for product in products]
    return [ProductBase(**product_dict) for product_dict in products_list]

@router.get("/products_by_name/{products}", response_model=ProductBase | list[ProductBase])
async def get_product_by_name(products_name: str, products_repository: ProductRepository = Depends(ProductRepository), db: Session = Depends(get_db)) -> list[ProductBase]|ProductBase|None:
    value = await products_repository.get_products_by_name(db, products_name)
    print(len(value))
    if value is None:
        raise HTTPException(status_code=404, detail="product not found or attribute not found")
    if isinstance(value, list):
        products_list = [model_to_dict(product) for product in value]
        return [ProductBase(**product_dict) for product_dict in products_list]
    else:
        product_dict = model_to_dict(value)
        return ProductBase(**product_dict)

@router.get("/products/{products}", response_model=ProductBase)
async def get_product_value(products: str, products_repository: ProductRepository = Depends(ProductRepository), db: Session = Depends(get_db)) -> ProductBase:
    value = await products_repository.get_product_query(db, products)
    if value is None:
        raise HTTPException(status_code=404, detail="product not found or attribute not found")
    product_dict = model_to_dict(value)
        
    return ProductBase(**product_dict)



@router.post("/products/", status_code=status.HTTP_201_CREATED, response_model=ProductBase)
async def create_product(product: ProductBase,products_repository: ProductRepository = Depends(ProductRepository), db: Session = Depends(get_db))-> ProductBase:
    new_product = await products_repository.create_product(db, product)
    product_dict = model_to_dict(new_product) 
    return ProductBase(**product_dict)

@router.put("/products/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductBase)
async def update_product(product_id: int, product: ProductBase,product_repository: ProductRepository = Depends(ProductRepository), db: Session = Depends(get_db))-> ProductBase:
    updated_product = await product_repository.update_product(db, product_id, product)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="produit_image not found")
    produit_image_dict = model_to_dict(updated_product) 
    return ProductBase(**produit_image_dict)
    