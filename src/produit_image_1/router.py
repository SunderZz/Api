import produit_image_1.models as models
from typing import Annotated
from .schema import ProduitImageBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from database import engine2, AsyncSessionLocal
from .repository import ProduitImageRepository
from common import model_to_dict

router = APIRouter(tags=["produit_image"])


@router.get("/produit_image/", status_code=status.HTTP_200_OK, response_model=list[ProduitImageBase])
async def get_produit_images(produit_image_repository: ProduitImageRepository = Depends(ProduitImageRepository),db:AsyncSession = Depends(get_db))-> list[ProduitImageBase]:
    produit_images = await produit_image_repository.get_produit_image(db)
    produit_image_list = [model_to_dict(produit_image) for produit_image in produit_images]
    return [ProduitImageBase(**produit_image_dict) for produit_image_dict in produit_image_list]


@router.get("/produit_image/{produit_image}", response_model=ProduitImageBase)
async def get_produit_image_value(produit_image: str, produit_image_repository: ProduitImageRepository = Depends(ProduitImageRepository), db:AsyncSession = Depends(get_db)) -> ProduitImageBase:
    value = await produit_image_repository.get_produit_image_query(db, produit_image)
    if value is None:
        raise HTTPException(status_code=404, detail="produit_image not found or attribute not found")
    return ProduitImageBase(value=value)


@router.post("/produit_image/", status_code=status.HTTP_201_CREATED, response_model=ProduitImageBase)
async def create_produit_image(produit_image: ProduitImageBase,produit_image_repository: ProduitImageRepository = Depends(ProduitImageRepository), db:AsyncSession = Depends(get_db))-> ProduitImageBase:
    new_produit_image = await produit_image_repository.create_produit_image(db, produit_image)
    produit_image_dict = model_to_dict(new_produit_image) 
    return ProduitImageBase(**produit_image_dict)

@router.put("/produit_image/{produit_image_id}", status_code=status.HTTP_200_OK, response_model=ProduitImageBase)
async def update_produit_image(produit_image_id: int, produit_image: ProduitImageBase,produit_image_repository: ProduitImageRepository = Depends(ProduitImageRepository), db:AsyncSession = Depends(get_db))-> ProduitImageBase:
    updated_produit_image = await produit_image_repository.update_Produit_Image(db, produit_image_id, produit_image)
    if updated_produit_image is None:
        raise HTTPException(status_code=404, detail="produit_image not found")
    produit_image_dict = model_to_dict(updated_produit_image) 
    return ProduitImageBase(**produit_image_dict)