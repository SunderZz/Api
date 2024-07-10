from .schema import ProduitImageBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .repository import ProduitImageRepository
from .services import (
    get_produit_images_service,
    get_produit_image_value_service,
    create_produit_image_service,
    update_produit_image_service,
)

router = APIRouter(tags=["produit_image"])


@router.get(
    "/produit_image/",
    status_code=status.HTTP_200_OK,
    response_model=list[ProduitImageBase],
)
async def get_produit_images(
    produit_image_repository: ProduitImageRepository = Depends(ProduitImageRepository),
    db: AsyncSession = Depends(get_db),
) -> list[ProduitImageBase]:
    return await get_produit_images_service(produit_image_repository, db)


@router.get("/produit_image/{produit_image}", response_model=ProduitImageBase)
async def get_produit_image_value(
    produit_image: str,
    produit_image_repository: ProduitImageRepository = Depends(ProduitImageRepository),
    db: AsyncSession = Depends(get_db),
) -> ProduitImageBase:
    return await get_produit_image_value_service(
        produit_image, produit_image_repository, db
    )


@router.post(
    "/produit_image/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProduitImageBase,
)
async def create_produit_image(
    produit_image: ProduitImageBase,
    produit_image_repository: ProduitImageRepository = Depends(ProduitImageRepository),
    db: AsyncSession = Depends(get_db),
) -> ProduitImageBase:
    return await create_produit_image_service(
        produit_image, produit_image_repository, db
    )


@router.put(
    "/produit_image/{produit_image_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProduitImageBase,
)
async def update_produit_image(
    produit_image_id: int,
    produit_image: ProduitImageBase,
    produit_image_repository: ProduitImageRepository = Depends(ProduitImageRepository),
    db: AsyncSession = Depends(get_db),
) -> ProduitImageBase:
    return await update_produit_image_service(
        produit_image_id, produit_image, produit_image_repository, db
    )
