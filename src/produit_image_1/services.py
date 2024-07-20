from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import ProduitImageRepository
from .schema import ProduitImageBase
from common import model_to_dict
import hashlib

async def create_produit_image_service(
    produit_image: ProduitImageBase,
    produit_image_repository: ProduitImageRepository,
    db: AsyncSession
) -> ProduitImageBase:
    new_produit_image = await produit_image_repository.create_produit_image(db, produit_image)
    return ProduitImageBase(**model_to_dict(new_produit_image))

async def get_produit_image_by_id_and_field_service(
    hashed_key: str,
    produit_image_repository: ProduitImageRepository,
    db: AsyncSession
) -> ProduitImageBase | None:
    produit_image = await produit_image_repository.get_produit_image_by_link(db, hashed_key)
    if produit_image is None:
        raise HTTPException(status_code=404, detail="Produit Image not found")
    return ProduitImageBase(**model_to_dict(produit_image))
