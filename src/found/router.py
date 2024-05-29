import season.models as models
from database import get_db
from typing import Annotated
from .schema import FoundBase
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine2, AsyncSessionLocal
from .repository import FoundRepository
from common import model_to_dict

router = APIRouter(tags=["found"])

@router.get("/found/", status_code=status.HTTP_200_OK, response_model=list[FoundBase])
async def get_founds(found_repository: FoundRepository = Depends(FoundRepository), db:AsyncSession = Depends(get_db)) -> list[FoundBase]:
    founds = await found_repository.get_found(db)
    founds_list = [model_to_dict(found) for found in founds]
    return [FoundBase(**found_dict) for found_dict in founds_list]

@router.get("/found/{found_id}", status_code=status.HTTP_200_OK, response_model=FoundBase)
async def get_found_by_id(found_id: int, found_repository: FoundRepository = Depends(FoundRepository), db:AsyncSession = Depends(get_db)) -> FoundBase:
    found = await found_repository.get_found_by_id(db, found_id)
    if found is None:
        raise HTTPException(status_code=404, detail="found not found")
    return FoundBase(**model_to_dict(found))

@router.post("/found/", status_code=status.HTTP_201_CREATED, response_model=FoundBase)
async def create_found(found: FoundBase, found_repository: FoundRepository = Depends(FoundRepository), db:AsyncSession = Depends(get_db)) -> FoundBase:
    new_found = await found_repository.create_found(db, found)
    found_dict = model_to_dict(new_found)
    return FoundBase(**found_dict)

@router.put("/found/{found_id}", status_code=status.HTTP_200_OK, response_model=FoundBase)
async def update_found(found_id: int, found: FoundBase, found_repository: FoundRepository = Depends(FoundRepository), db:AsyncSession = Depends(get_db)) -> FoundBase:
    updated_found = await found_repository.update_found(db, found_id, found)
    if updated_found is None:
        raise HTTPException(status_code=404, detail="found not found")
    found_dict = model_to_dict(updated_found)
    return FoundBase(**found_dict)
