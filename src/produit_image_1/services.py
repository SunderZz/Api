import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, UploadFile
from .repository import ProduitImageRepository
from .schema import ProduitImageBase
from common import model_to_dict
import hashlib
import os


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
) -> ProduitImageBase | None:
    value = await produit_image_repository.get_produit_image_query(db, produit_image)
    if value is None:
        return None
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


async def save_image_to_server(file: UploadFile, produit_id: int) -> str:
    try:
        contents = await file.read()
        hash_object = hashlib.sha256(f"{produit_id}_{file.filename}".encode())
        unique_hash = hash_object.hexdigest()
        # remplacer par le chemin serveur
        file_path = f"images/{unique_hash}.jpg"

        with open(file_path, "wb") as f:
            f.write(contents)
        # remplacer par le chemin web
        return f"http://example.com/{file_path}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



async def get_image_from_hash(
    produit_image_repository: ProduitImageRepository,
    db: AsyncSession,
    produit_image_id: int,
) -> str | None:
    produit_image = await produit_image_repository.get_produit_image_query(
        db, produit_image_id
    )
    if produit_image is None:
        return None

    file_path = f"images/{produit_image.lien_image.split('/')[-1]}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image file not found on server")

    return file_path


async def replace_image_service(
    produit_image_id: int,
    file: UploadFile,
    produit_image_repository: ProduitImageRepository,
    db: AsyncSession,
) -> ProduitImageBase:
    # Vérifier si l'image existe
    existing_produit_image = await produit_image_repository.get_produit_image_query(
        db, produit_image_id
    )
    if existing_produit_image is None:
        raise HTTPException(status_code=404, detail="produit_image not found")

    # Supprimer l'ancienne image du serveur
    old_file_path = f"images/{existing_produit_image.lien_image.split('/')[-1]}"
    if os.path.exists(old_file_path):
        os.remove(old_file_path)

    # Sauvegarder la nouvelle image sur le serveur
    new_file_url = await save_image_to_server(file, produit_image_id)

    # Mettre à jour l'URL de l'image en base de données
    existing_produit_image.lien_image = new_file_url
    await db.commit()
    await db.refresh(existing_produit_image)

    return ProduitImageBase(**model_to_dict(existing_produit_image))
