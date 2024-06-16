import season.models as models
from database import get_db
from typing import Annotated
from .schema import LocatedBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine2, AsyncSessionLocal
from .repository import LocatedRepository
from common import model_to_dict

router = APIRouter(tags=["located"])

@router.get("/located/", status_code=status.HTTP_200_OK, response_model=list[LocatedBase])
async def get_locateds(located_repository: LocatedRepository = Depends(LocatedRepository), db:AsyncSession = Depends(get_db)) -> list[LocatedBase]:
    locateds = await located_repository.get_located(db)
    locateds_list = [model_to_dict(located) for located in locateds]
    return [LocatedBase(**located_dict) for located_dict in locateds_list]

@router.get("/located/{located_id}", status_code=status.HTTP_200_OK, response_model=LocatedBase)
async def get_located_by_ids(located_id: int, located_repository: LocatedRepository = Depends(LocatedRepository), db:AsyncSession = Depends(get_db)) -> LocatedBase:
    located = await located_repository.get_located_by_id(db, located_id)
    if located is None:
        return None
    return LocatedBase(**model_to_dict(located))

@router.post("/located/", status_code=status.HTTP_201_CREATED, response_model=LocatedBase)
async def create_located(located: LocatedBase, located_repository: LocatedRepository = Depends(LocatedRepository), db:AsyncSession = Depends(get_db)) -> LocatedBase:
    id_code= located.Id_Users_adresses
    existing_code_postal = await get_located_by_ids(id_code,located_repository,db)
    if existing_code_postal is not None:
        return existing_code_postal
    else:
        new_located = await located_repository.create_located(db, located)
        located_dict = model_to_dict(new_located)
        return LocatedBase(**located_dict)

@router.put("/located/{located_id}", status_code=status.HTTP_200_OK, response_model=LocatedBase)
async def update_located(located_id: int, located: LocatedBase, located_repository: LocatedRepository = Depends(LocatedRepository), db:AsyncSession = Depends(get_db)) -> LocatedBase:
    updated_located = await located_repository.update_located(db, located_id, located)
    if updated_located is None:
        raise HTTPException(status_code=404, detail="located not found")
    located_dict = model_to_dict(updated_located)
    return LocatedBase(**located_dict)
