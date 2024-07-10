from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from .repository import FoundRepository
from .schema import FoundBase
from common import model_to_dict

async def get_founds_service(found_repository: FoundRepository, db: AsyncSession) -> list[FoundBase]:
    founds = await found_repository.get_found(db)
    founds_list = [model_to_dict(found) for found in founds]
    return [FoundBase(**found_dict) for found_dict in founds_list]

async def get_found_by_id_service(found_id: int, found_repository: FoundRepository, db: AsyncSession) -> FoundBase:
    found = await found_repository.get_found_by_id(db, found_id)
    if found is None:
        raise HTTPException(status_code=404, detail="found not found")
    return FoundBase(**model_to_dict(found))

async def create_found_service(found: FoundBase, found_repository: FoundRepository, db: AsyncSession) -> FoundBase:
    new_found = await found_repository.create_found(db, found)
    return FoundBase(**model_to_dict(new_found))

async def update_found_service(found_id: int, found: FoundBase, found_repository: FoundRepository, db: AsyncSession) -> FoundBase:
    updated_found = await found_repository.update_found(db, found_id, found)
    if updated_found is None:
        raise HTTPException(status_code=404, detail="found not found")
    return FoundBase(**model_to_dict(updated_found))
