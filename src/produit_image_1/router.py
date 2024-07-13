from .schema import ProduitImageBase
from fastapi import APIRouter, Depends, status, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .repository import ProduitImageRepository
from .services import (
    get_produit_images_service,
    get_produit_image_value_service,
    create_produit_image_service,
    update_produit_image_service,
    save_image_to_server,
    get_image_from_hash,
    replace_image_service,
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


@router.get("/produit_image/{produit_image}", response_model=ProduitImageBase | None)
async def get_produit_image_value(
    produit_image: str,
    produit_image_repository: ProduitImageRepository = Depends(ProduitImageRepository),
    db: AsyncSession = Depends(get_db),
) -> ProduitImageBase | None:
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


@router.post("/produit_image/upload/{produit_id}", status_code=status.HTTP_201_CREATED)
async def upload_produit_image(
    produit_id: int,
    file: UploadFile = File(...),
    produit_image_repository: ProduitImageRepository = Depends(ProduitImageRepository),
    db: AsyncSession = Depends(get_db),
) -> ProduitImageBase:
    file_url = await save_image_to_server(file, produit_id)

    produit_image_data = ProduitImageBase(Nom=file.filename, lien_image=file_url)
    new_produit_image = await create_produit_image_service(
        produit_image_data, produit_image_repository, db
    )
    return new_produit_image


@router.get("/produit_image/download/{produit_image_id}", response_class=FileResponse)
async def download_produit_image(
    produit_image_id: int,
    produit_image_repository: ProduitImageRepository = Depends(ProduitImageRepository),
    db: AsyncSession = Depends(get_db),
) -> FileResponse:
    file_path = await get_image_from_hash(
        produit_image_repository, db, produit_image_id
    )
    if file_path is None:
        return None
    return FileResponse(file_path)


@router.put(
    "/produit_image/replace/{produit_image_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProduitImageBase,
)
async def replace_produit_image(
    produit_image_id: int,
    file: UploadFile = File(...),
    produit_image_repository: ProduitImageRepository = Depends(ProduitImageRepository),
    db: AsyncSession = Depends(get_db),
) -> ProduitImageBase:
    return await replace_image_service(
        produit_image_id, file, produit_image_repository, db
    )
