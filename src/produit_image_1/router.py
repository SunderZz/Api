import produit_image_1.models as models
from typing import Annotated
from .schema import ProduitImageBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import main as get_db
from database import engine, SessionLocal


def get_db():
    db = SessionLocal
    try: 
        yield db
    finally:
        db.close_all()

router = APIRouter(tags=["image"])

models.Base.metadata.create_all(bind=engine)

db_dependency= Annotated[Session, Depends(get_db)]




@router.get("/produit_image/", status_code= status.HTTP_200_OK)
async def get_produit_image(db: db_dependency):
    produit_image= db.query(models.Produit_Image_1).all()
    return {"produit_image":produit_image}

@router.post("/produit_image/", status_code= status.HTTP_201_CREATED)
async def create_user(produit_image:ProduitImageBase, db: db_dependency):
    db_user= models(**produit_image.model_dump())
    db.add(db_user)
    db.commit()

#get image
#get image based on id user
#put image
#post image
#delete image