import products.models as models
from typing import Annotated
from .schema import ProductBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["products"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]


@router.get("/products/", status_code= status.HTTP_201_CREATED)
async def get_products(db: db_dependency):
    products= db.query(models.Product).all()
    return {"products":products}

# @router.get("/products/", status_code= status.HTTP_201_CREATED)
# async def get_users(db: db_dependency):
#     products= db.query(models.Product).all()
#     return {"products":products}

# @router.put("/products/", status_code= status.HTTP_201_CREATED)
# async def modify_cart(db: db_dependency):
#     products= db.query(models.Product).all()
#     return {"products":products}

# @router.get("/products/", status_code= status.HTTP_201_CREATED)
# async def get_products_by(db: db_dependency):
#     products= db.query(models.Product).all()
#     return {"products":products}
# @router.get("/products/", status_code= status.HTTP_201_CREATED)
# async def get_users(db: db_dependency):
#     products= db.query(models.Product).all()
#     return {"products":products}
# @router.get("/products/", status_code= status.HTTP_201_CREATED)
# async def get_users(db: db_dependency):
#     products= db.query(models.Product).all()
#     return {"products":products}
# @router.get("/products/", status_code= status.HTTP_201_CREATED)
# async def get_users(db: db_dependency):
#     products= db.query(models.Product).all()
#     return {"products":products}
# @router.get("/products/", status_code= status.HTTP_201_CREATED)
# async def get_users(db: db_dependency):
#     products= db.query(models.Product).all()
#     return {"products":products}
# @router.get("/products/", status_code= status.HTTP_201_CREATED)
# async def get_users(db: db_dependency):
#     products= db.query(models.Product).all()
#     return {"products":products}

    
# Router for Product:
# get all products
# GET-description:"Retrieve all Product base on criteria"
# POST - description:"create a page for a product"
# PUT - description:" Modify the state of the product"
