import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import ProduitImageRepository
from .schema import ProduitImageBase
from common import model_to_dict


async def get_produit_images_service(
    produit_image_repository: ProduitImageRepository, db: AsyncSession
) -> list[ProduitImageBase]:
    produit_images = await produit_image_repository.get_produit_image(db)
    produit_image_list = [
        model_to_dict(produit_image) for produit_image in produit_images
    ]
    return [
        ProduitImageBase(**produit_image_dict)
        for produit_image_dict in produit_image_list
    ]


async def get_produit_image_value_service(
    produit_image: str,
    produit_image_repository: ProduitImageRepository,
    db: AsyncSession,
) -> ProduitImageBase:
    value = await produit_image_repository.get_produit_image_query(db, produit_image)
    if value is None:
        raise HTTPException(
            status_code=404, detail="produit_image not found or attribute not found"
        )
    return ProduitImageBase(**model_to_dict(value))


async def create_produit_image_service(
    produit_image: ProduitImageBase,
    produit_image_repository: ProduitImageRepository,
    db: AsyncSession,
) -> ProduitImageBase:
    unique_id = uuid.uuid4()
    lien_image = f"http://example.com/images/{produit_image.Nom}_{unique_id}.jpg"

    produit_image.lien_image = lien_image
    new_produit_image = await produit_image_repository.create_produit_image(
        db, produit_image
    )
    return ProduitImageBase(**model_to_dict(new_produit_image))


async def update_produit_image_service(
    produit_image_id: int,
    produit_image: ProduitImageBase,
    produit_image_repository: ProduitImageRepository,
    db: AsyncSession,
) -> ProduitImageBase:
    unique_id = uuid.uuid4()
    lien_image = f"http://example.com/images/{produit_image.Nom}_{unique_id}.jpg"

    produit_image.lien_image = lien_image
    updated_produit_image = await produit_image_repository.update_Produit_Image(
        db, produit_image_id, produit_image
    )
    if updated_produit_image is None:
        raise HTTPException(status_code=404, detail="produit_image not found")
    return ProduitImageBase(**model_to_dict(updated_produit_image))
