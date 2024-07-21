import ftplib
from fastapi import APIRouter, Depends, Form, status, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .schema import ProduitImageBase
from .repository import ProduitImageRepository
from .services import (
    create_produit_image_service,
    get_produit_image_by_id_and_field_service,
)
import os
import hashlib
from ftplib import FTP
from dotenv import load_dotenv
import tempfile
from fastapi.responses import FileResponse

load_dotenv()

router = APIRouter(tags=["produit_image"])

FTP_HOST = os.getenv("FTP_HOST")
FTP_USER = os.getenv("FTP_USER")
FTP_PASS = os.getenv("FTP_PASS")
FTP_UPLOAD_FOLDER = os.getenv("FTP_UPLOAD_FOLDER")

def hash_key(product_id: str, field_name: str) -> str:
    hash_object = hashlib.sha256(f"{product_id}_{field_name}".encode())
    return hash_object.hexdigest()

def hash_link(link: str) -> str:
    hash_object = hashlib.sha256(link.encode())
    return hash_object.hexdigest()

@router.post("/produit_image/", status_code=status.HTTP_201_CREATED, response_model=ProduitImageBase)
async def upload_file(
    product_id: str = Form(...),
    field_name: str = Form(...),
    nom: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    produit_image_repository: ProduitImageRepository = Depends(ProduitImageRepository)
) -> ProduitImageBase:
    hashed_key = hash_key(product_id, field_name)
    hashed_filename = hashed_key + ".jpg"
    link = f"/images/{hashed_filename}"
    hashed_link_value = hash_link(link)

    temp_dir = tempfile.gettempdir()
    file_location = os.path.join(temp_dir, hashed_filename)
    
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    
    with FTP(FTP_HOST) as ftp:
        ftp.login(user=FTP_USER, passwd=FTP_PASS)
        ftp.cwd(FTP_UPLOAD_FOLDER)
        
        with open(file_location, "rb") as f:
            ftp.storbinary(f"STOR {hashed_filename}", f)
    
    os.remove(file_location)

    produit_image_data = ProduitImageBase(Nom=nom, lien_image=hashed_filename)
    new_produit_image = await create_produit_image_service(produit_image_data, produit_image_repository, db)

    return new_produit_image

@router.get("/produit_image/", status_code=status.HTTP_200_OK)
async def get_image(
    produit_image_id: int,
    field_name: str,
    db: AsyncSession = Depends(get_db),
    produit_image_repository: ProduitImageRepository = Depends(ProduitImageRepository)
):
    hashed_key = hash_key(produit_image_id, field_name)
    hashed_filename = hashed_key + ".jpg"
    produit_image = await get_produit_image_by_id_and_field_service(hashed_filename, produit_image_repository, db)
    
    if not produit_image:
        raise HTTPException(status_code=404, detail="File not found")

    temp_dir = tempfile.gettempdir()
    local_file_path = os.path.join(temp_dir, hashed_filename)

    with FTP(FTP_HOST) as ftp:
        ftp.login(user=FTP_USER, passwd=FTP_PASS)
        ftp.cwd(FTP_UPLOAD_FOLDER)
        
        with open(local_file_path, "wb") as f:
            try:
                ftp.retrbinary(f"RETR {hashed_filename}", f.write)
            except ftplib.error_perm:
                raise HTTPException(status_code=404, detail="File not found on FTP server")

    if not os.path.exists(local_file_path):
        raise HTTPException(status_code=404, detail="File not found locally")

    return FileResponse(local_file_path)
